import requests
from flask import Flask, jsonify, make_response, request, abort
import configparser
from lxml import html
from zeep import Client, helpers

app = Flask(__name__)

allegro_url = 'https://webapi.allegro.pl.webapisandbox.pl/service.php?wsdl'


class ServerException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ServerException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/items', methods=['GET'])
def get_items():
    if 'keyword' in request.values:
        keyword = request.values['keyword']
    seller = ''
    if 'seller' in request.values:
        seller = request.values['seller']

    shop = request.values['shop']
    if shop == 'ebay.de':
        result = get_items_ebay(keyword, seller)
    elif shop == 'allegro.pl':
        result = get_items_allegro(keyword, seller)
    else:
        raise ServerException('Shop ({}) not available'.format(shop))
    return jsonify(result)


def get_items_allegro(keyword, seller):
    client = Client(allegro_url)

    factory = client.type_factory('ns0')

    arr = factory.ArrayOfString(keyword)
    options = factory.FilterOptionsType('search', arr)
    filters = factory.ArrayOfFilteroptionstype(options)

    result = client.service.doGetItemsList(Config.ALLEGRO_APP_NAME, 1, filters)
    data = helpers.serialize_object(result)['itemsList']
    if not data:
        return []

    parsed = []
    for el in data['item']:
        photos = el.get('photosInfo')
        photos = photos.get('item')[0].get('photoUrl') if photos else ''

        parsed.append(build_item(
            el.get('itemId'),
            el.get('itemTitle'),
            el.get('sellerInfo').get('userLogin'),
            el.get('priceInfo').get('item')[0].get('priceValue'),
            'PLN',
            photos,
            el.get('itemId'),
            el.get('sellerInfo').get('countryId'),
            el.get('sellerInfo').get('countryId')
        ))

    return parsed


def get_items_ebay(keyword, seller):
    url = 'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' \
          '?OPERATION-NAME=findItemsAdvanced' \
          '&SECURITY-APPNAME=' + Config.EBAY_APP_NAME + \
          '&RESPONSE-DATA-FORMAT=JSON' \
          '&REST-PAYLOAD' \
          '&outputSelector(0)=SellerInfo' \
          '&paginationInput.entriesPerPage=10'

    if keyword:
        url += '&keywords=' + keyword
    if seller:
        url += '&itemFilter(0).name=Seller&itemFilter(0).value=' + seller

    r = requests.get(url)
    data = r.json()['findItemsAdvancedResponse'][0]['searchResult'][0]
    data = data['item'] if 'item' in data else []

    parsed = []
    for el in data:
        parsed.append(build_item(
            el.get('itemId')[0],
            el.get('title')[0],
            el.get('sellerInfo', {})[0].get('sellerUserName')[0],
            el.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('__value__'),
            el.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('@currencyId'),
            el.get('galleryURL'),
            el.get('viewItemURL')[0],
            el.get('country')[0],
            el.get('location')[0]
        ))

    return parsed


def build_item(id, title, seller, price, currency, gallery_url, view_url, country, location):
    return {
        'itemId': id,
        'title': title,
        'seller': seller,
        'price': price,
        'currency': currency,
        'galleryURL': gallery_url,
        'viewItemURL': view_url,
        'info': {
            'country': country,
            'location': location
        }
    }


@app.route('/getLinks', methods=['GET'])
def get_links():
    url = request.values['itemUrl']

    page = requests.get(url)
    tree = html.fromstring(page.content)
    cart_href = tree.xpath("//a[@id='isCartBtn_btn']/@href")
    buy_href = tree.xpath("//a[@id='binBtn_btn' and @role='button']/@href")

    result = {
        'cart': cart_href[0] if cart_href else url,
        'buy': buy_href[0] if buy_href else url
    }

    response = jsonify(result)
    return response


@app.route('/promos', methods=['GET'])
def get_promos():
    result = {'promos': [
        {
            'keywords': ['playstation 4', 'xbox 360'],
            'imageUrl': 'assets/consoles.jpg'
        },
        {
            'keywords': ['iphone 5', 'samsung galaxy 2'],
            'imageUrl': 'assets/phones.jpg'
        },
        {
            'keywords': ['necklace', 'earrings'],
            'imageUrl': 'assets/jewellery.jpg'
        },
        {
            'keywords': ['lego', 'plush'],
            'imageUrl': 'assets/toys.jpg'
        },
        {
            'keywords': ['games', 'music'],
            'imageUrl': 'assets/games.jpg'
        },
        {
            'keywords': ['shirt', 'socks'],
            'imageUrl': 'assets/wardrobe.jpg'
        }
    ]}
    response = jsonify(result)
    return response


class Config:
    @staticmethod
    def load():
        cfg = configparser.ConfigParser()
        cfg.sections()
        cfg.read('server.ini')
        Config.EBAY_APP_NAME = cfg['DEFAULT']['EBAY_APP_NAME']
        Config.ALLEGRO_APP_NAME = cfg['DEFAULT']['ALLEGRO_APP_NAME']


if __name__ == '__main__':
    print('\n*** SERVER STARTED ***\n')
    Config.load()
    app.run(debug=True)
