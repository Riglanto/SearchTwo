import requests
from flask import Flask, jsonify, make_response, request, abort
import configparser
from lxml import html

app = Flask(__name__)


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
def get_tasks():
    shop = request.values['shop']
    if shop != 'ebay.de':
        raise ServerException('Shop not available', status_code=204)
    url = 'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' \
          '?OPERATION-NAME=findItemsAdvanced' \
          '&SECURITY-APPNAME=' + Config.getAppName() + \
          '&RESPONSE-DATA-FORMAT=JSON' \
          '&REST-PAYLOAD' \
          '&outputSelector(0)=SellerInfo' \
          '&paginationInput.entriesPerPage=10'

    if 'keyword' in request.values:
        url += '&keywords=' + request.values['keyword']
    if 'seller' in request.values:
        url += '&itemFilter(0).name=Seller&itemFilter(0).value=' + request.values['seller']
    r = requests.get(url)
    data = r.json()['findItemsAdvancedResponse'][0]['searchResult'][0]
    data = data['item'] if 'item' in data else []
    parsed = []
    for element in data:
        parsed.append({
            'itemId': element.get('itemId')[0],
            'title': element.get('title')[0],
            'seller': element.get('sellerInfo', {})[0].get('sellerUserName')[0],
            'price': element.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('__value__'),
            'currency': element.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('@currencyId'),
            'galleryURL': element.get('galleryURL'),
            'viewItemURL': element.get('viewItemURL')[0],
        })

    response = jsonify(parsed)
    return response


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
    @classmethod
    def load(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read('server.ini')
        self.AppName = config['DEFAULT']['AppName']

    @classmethod
    def getAppName(self):
        return self.AppName


if __name__ == '__main__':
    print('\n*** SERVER STARTED ***\n')
    Config.load()
    app.run(debug=True)
