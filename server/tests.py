import unittest
import server
import json


class ServerTest(unittest.TestCase):
    def setUp(self):
        server.app.debug = True
        server.app.testing = True
        self.app = server.app.test_client()
        server.Config.load()

    def test_get_items(self):
        response = self.app.get('/items?keyword=batman&shop=ebay.de')
        data = json.loads(response.data)

        self.assertEqual(len(data), 10)
        first = data[0]
        self.assertIn('itemId', first)
        self.assertIn('title', first)
        self.assertIn('seller', first)
        self.assertIn('price', first)
        self.assertIn('currency', first)
        self.assertIn('galleryURL', first)
        self.assertIn('viewItemURL', first)

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
        self.assertEqual(data['message'], 'Shop ({}) not available'.format(shop))


if __name__ == '__main__':
    unittest.main()
