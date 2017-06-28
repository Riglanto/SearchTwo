import falcon
import json
import requests
import sys
import configparser

class ItemsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        # raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Missing keyword')
        url = 'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' \
              '?OPERATION-NAME=findItemsAdvanced' \
              '&SECURITY-APPNAME=' + Config.getAppName() + \
              '&RESPONSE-DATA-FORMAT=JSON' \
              '&REST-PAYLOAD' \
              '&outputSelector(0)=SellerInfo' \
              '&paginationInput.entriesPerPage=10'

        if req.get_param("keyword"):
            url += '&keywords=' + req.get_param("keyword")
        if req.get_param("seller"):
            url += '&itemFilter(0).name=Seller&itemFilter(0).value=' + req.get_param("seller")
        print(url)
        try:
            r = requests.get(url)
            data = r.json()['findItemsAdvancedResponse'][0]['searchResult'][0]['item']
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

            resp.body = json.dumps(parsed)

        except KeyError as e:
            print('KeyError - reason "%s"' % str(e))
            raise falcon.HTTPError(falcon.HTTP_404, 'KeyError', 'No results')


class CorsMiddleware(object):
    def process_request(self, request, res):
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'GET')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With')

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

Config.load()

app = application = falcon.API(middleware=[CorsMiddleware()])
items = ItemsResource()
app.add_route('/items', items)

# Windows WSGI support, otherwise gunicorn server:api
if len(sys.argv) > 1 and sys.argv[1] == 'local':
    from waitress import serve

    serve(application, host='127.0.0.1', port=5555)
