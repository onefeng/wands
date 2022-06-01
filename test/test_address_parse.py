# -*- coding: utf-8 -*-

"""
@author: tenkola
@time: 2022/6/1 10:54
"""
import unittest
import time

from wands import AddressParse


class TestParseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.ap = AddressParse()
        cls.ap('')

    def test_address_parse(self):
        text = '河南郑州中原开封'
        start = time.time()
        result = self.ap(text, True)
        end = time.time()

        print(end - start)

        print(result)

        self.assertEqual(True, True)

    def test_address_parse1(self):
        text = '河口'
        result = self.ap(text)

        print(result)
        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()