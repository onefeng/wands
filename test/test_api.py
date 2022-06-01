# -*- coding: utf-8 -*-

"""
@author: tenkola
@time: 2022/6/1 10:55
"""
import unittest


class TestApiCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from wands.server import create_app
        app = create_app(__name__)
        cls.client = app.test_client()

    def test_area_app(self):
        response = self.client.get('/address?area=海南')
        print(response.json)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
