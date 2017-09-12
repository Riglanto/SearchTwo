import unittest
import server
import json


class ServerTest(unittest.TestCase):
    keyword_zero = 'qqqqqqqqqq'

    def setUp(self):
        server.app.debug = True
        server.app.testing = True
        self.app = server.app.test_client()

    def test_get_items_ebay(self):
        keyword = 'iphone'
        for country in ['us', 'gb', 'de']:
            response = self.app.get('/items?keyword={}&shop=ebay.{}'.format(keyword, country))
            data = json.loads(response.data)

            self.assertEqual(len(data), 10, 'No {} found in ebay.{}'.format(keyword, country))
            first = data[0]
            self.assertIn('itemId', first)
            self.assertIn('title', first)
            self.assertIn('seller', first)
            self.assertIn('price', first)
            self.assertIn('currency', first)
            self.assertIn('galleryURL', first)
            self.assertIn('viewItemURL', first)

    def test_get_zero_items_ebay(self):
        response = self.app.get('/items?keyword={}&shop=ebay.de'.format(self.keyword_zero))
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_get_items_allegro(self):
        response = self.app.get('/items?keyword=obuwie&shop=allegro.pl')
        data = json.loads(response.data)

        self.assertEqual(len(data), 12)
        first = data[0]
        self.assertIn('itemId', first)
        self.assertIn('title', first)
        self.assertIn('seller', first)
        self.assertIn('price', first)
        self.assertIn('currency', first)
        self.assertIn('galleryURL', first)
        self.assertIn('viewItemURL', first)

    def test_get_zero_items_allegro(self):
        response = self.app.get('/items?keyword={}&shop=allegro.pl'.format(self.keyword_zero))
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_get_links(self):
        test_url = 'http://www.ebay.com/itm/Google-Home-Chromecast-Video-2nd-Gen-1080p-Bundle-for-99-99-/222571438996'
        response = self.app.get('/getLinks?itemUrl={0}'.format(test_url))

        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertRegex(data['cart'], '^https?:\/\/')
        self.assertRegex(data['buy'], '^https?:\/\/')

    def test_get_promos(self):
        response = self.app.get('/promos')
        data = json.loads(response.data)

        self.assertEqual(len(data['promos']), 6)
        for el in data['promos']:
            self.assertEqual(len(el['keywords']), 2)
            self.assertIn('imageUrl', el)

    def test_incorrect_shop(self):
        shop = 'google.com'
        response = self.app.get('/items?shop=' + shop)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Shop ({}) not available'.format(shop.split('.')[0]))


if __name__ == '__main__':
    unittest.main()
