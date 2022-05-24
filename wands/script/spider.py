# -*- coding: utf-8 -*-

"""
@author: tenkola
@time: 2022/5/24 10:15
"""
import re

from urllib.parse import urljoin

import requests
from pyquery import PyQuery as pq


class AreaSpider:

    def __init__(self, level=3, year=2019):
        """设置抓取地域等级"""
        self.level = level
        self.year = year

    def start_request(self):
        self.set_version()
        response = requests.get(url=self.start_url)
        response.encoding = self.encoding
        self.parse_page(response)

    def set_version(self):
        self.start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{}/index.html'.format(self.year)
        if self.year >= 2021:
            self.encoding = 'utf8'
        else:
            self.encoding = 'gbk'

    def set_level(self, doc):
        if self.level == 1:
            return None, None, None, None, None
        if self.level == 2:
            return doc('.provincetr'), None, None, None, None
        if self.level == 3:
            return doc('.provincetr'), doc('.citytr'), None, None, None
        if self.level == 4:
            return doc('.provincetr'), doc('.citytr'), doc('.countytr'), None, None
        if self.level == 5:
            return doc('.provincetr'), doc('.citytr'), doc('.countytr'), doc('.towntr'), None

    @staticmethod
    def retry_response(url):
        n = 0
        while n < 5:
            try:
                response = requests.get(url=url, timeout=5)
                return response
            except requests.exceptions.ReadTimeout:
                print(f'重试{n}', url)
                n += 1

    def parse_page(self, response):
        response.encoding = self.encoding
        doc = pq(response.text)
        province, city, county, town, village = self.set_level(doc)
        detail = self.parse_detail(response)
        for data in detail:
            print(data)
            # yield data
        items = []
        if province:
            items = province('a[href]').items()
        if city:
            items = city("td:eq(0) a").items()
        if county:
            items = county("td:eq(0) a").items()
        if town:
            items = town("td:eq(0) a").items()
        if village:
            items = village("td:eq(0) a").items()

        parent_url = response.url
        for item in items:
            sub_href = item.attr('href')
            sub_url = urljoin(parent_url, sub_href)
            # print(sub_url)
            response = self.retry_response(sub_url)

            self.parse_page(response)

    def parse_detail(self, response):
        response.encoding = self.encoding
        doc = pq(response.text)
        province = doc('.provincetr')
        city = doc('.citytr')
        county = doc('.countytr')
        town = doc('.towntr')
        village = doc('.villagetr')

        parent_url = response.url
        parent_id = re.findall(r'/([^/]*?)\.html$', parent_url)[0]
        if province:
            items = province('td > a[href]').items()  # td > a[href]
            for item in items:
                data = dict()
                pattern = re.compile(r'\d{2}', re.S)
                data['name'] = item.text()
                area_id = re.search(pattern, item.attr('href'))
                if area_id:
                    data['id'] = area_id.group(0)
                data['parent_id'] = '0'
                data['area_level'] = '1'
                yield data
        elif city:
            items = city.items()
            for item in items:
                data = dict()
                id = item('td:eq(0)').text()
                data['name'] = item('td:eq(1)').text()
                data['id'] = id[0:4]
                data['parent_id'] = parent_id
                data['area_level'] = '2'
                yield data
        elif county:
            items = county.items()
            for item in items:
                data = dict()
                id = item('td:eq(0)').text()
                data['name'] = item('td:eq(1)').text()
                data['id'] = id[0:6]
                data['parent_id'] = parent_id
                data['area_level'] = '3'
                yield data
        elif town:
            items = town.items()
            for item in items:
                data = dict()
                id = item('td:eq(0)').text()
                data['name'] = item('td:eq(1)').text()
                data['id'] = id[0:9]
                data['parent_id'] = parent_id
                data['area_level'] = '4'
                yield data
        elif village:
            items = village.items()
            for item in items:
                data = dict()
                id = item('td:eq(0)').text()
                data['name'] = item('td:eq(2)').text()
                data['id'] = id
                data['parent_id'] = parent_id
                data['area_level'] = '5'
                yield data


if __name__ == '__main__':
    s = AreaSpider(3, 2020)
    s.start_request()