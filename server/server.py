import requests
from flask import Flask, jsonify, make_response, request
import configparser

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
            'itemId': element.get('itemId'),
            'title': element.get('title'),
            'seller': element.get('sellerInfo', {})[0].get('sellerUserName'),
            'price': element.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('__value__'),
            'currency': element.get('sellingStatus', {})[0].get('currentPrice', {})[0].get('@currencyId'),
            'galleryURL': element.get('galleryURL'),
        })

    response = jsonify(parsed)
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
