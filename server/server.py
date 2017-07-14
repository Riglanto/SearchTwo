import requests
from flask import Flask, jsonify, make_response, request
import configparser
from lxml import html

app = Flask(__name__)


@app.route('/items', methods=['GET'])
def get_tasks():
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
    response.headers.add('Access-Control-Allow-Origin', '*')
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
    response.headers.add('Access-Control-Allow-Origin', '*')
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
