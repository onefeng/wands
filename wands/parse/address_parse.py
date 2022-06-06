# -*- coding: utf-8 -*-

"""
@author: onefeng
@time: 2022/5/19 14:09
"""
import copy

from wands.data.load_data import load_address


class AddressParse:

    def __init__(self):
        self.map_list = None

    def _prepare(self):
        self.map_list = load_address()
        self.tree = self.generate_tree(self.map_list, 0)

    def generate_tree(self, source, parent):
        tree = []
        for item in source:
            if item["parent_id"] == parent:
                item["child"] = self.generate_tree(source, item["id"])
                tree.append(item)
        return tree

    def get_candidates_result(self, address_text):
        candidates = []
        for item in self.map_list:
            if item['name'] in address_text or item['alias'] in address_text:
                candidates.append(item)
        return candidates

    def find_tree(self, id):
        """遍历树"""
        for i in self.tree:
            if i['id'] == id:
                return i
            for j in i['child']:
                if j['id'] == id:
                    return j
                for k in j['child']:
                    if k['id'] == id:
                        return k

    @staticmethod
    def parse_address_by_province(province, text):

        result = {'province': None,
                  'city': None,
                  'county': None,
                  'province_id': None,
                  'city_id': None,
                  'county_id': None,
                  'province_fit': 0,
                  'city_fit': 0,
                  'county_fit': 0
                  }

        result_list = list()

        result['province'] = province['name']
        result['province_id'] = province['id']
        result['province_fit'] = len(province['name']) if province['name'] in text else len(province['alias'])
        cur_province = copy.deepcopy(result)

        # 向下查找市
        city_n = 0
        for city in province['child']:
            if city['name'] in text or city['alias'] in text:
                cur_city = copy.deepcopy(result)
                cur_city['city'] = city['name']
                cur_city['city_id'] = city['id']
                cur_city['city_fit'] = len(city['name']) if city['name'] in text else len(city['alias'])
                city_n += 1
                # 向下查县
                county_n = 0
                for county in city['child']:
                    if county['name'] in text or county['alias'] in text:
                        cur_county = copy.deepcopy(cur_city)
                        cur_county['county'] = county['name']
                        cur_county['county_id'] = county['id']
                        cur_county['county_fit'] = len(county['name']) if county['name'] in text else len(
                            county['alias'])
                        county_n += 1
                        result_list.append(cur_county)
                if county_n == 0:
                    result_list.append(cur_city)
        if city_n == 0:
            result_list.append(cur_province)
        return result_list

    def parse_address_by_city(self, city, text):
        # 向上查找省
        result = {'province': None,
                  'city': None,
                  'county': None,
                  'province_id': None,
                  'city_id': None,
                  'county_id': None,
                  'province_fit': 0,
                  'city_fit': 0,
                  'county_fit': 0
                  }
        result_list = list()
        province = self.find_tree(city['parent_id'])
        result['province'] = province['name']
        result['province_id'] = province['id']
        if province['name'] in text or province['alias'] in text:
            result['province_fit'] = len(province['name']) if province['name'] in text else len(province['alias'])
        result['city'] = city['name']
        result['city_id'] = city['id']
        result['city_fit'] = len(city['name']) if city['name'] in text else len(city['alias'])

        county_n = 0
        for county in city['child']:
            if county['name'] in text or county['alias'] in text:
                cur_county = copy.deepcopy(result)
                cur_county['county'] = county['name']
                cur_county['county_id'] = county['id']
                cur_county['county_fit'] = len(county['name']) if county['name'] in text else len(
                    county['alias'])
                county_n += 1
                result_list.append(cur_county)
        if county_n == 0:
            result_list.append(result)
        return result_list

    def parse_address_by_county(self, county, text):
        # 向上查找省市
        result = {'province': None,
                  'city': None,
                  'county': None,
                  'province_id': None,
                  'city_id': None,
                  'county_id': None,
                  'province_fit': 0,
                  'city_fit': 0,
                  'county_fit': 0
                  }
        city = self.find_tree(county['parent_id'])
        province = self.find_tree(city['parent_id'])
        result['province'] = province['name']
        result['province_id'] = province['id']
        if province['name'] in text or province['alias'] in text:
            result['province_fit'] = len(province['name']) if province['name'] in text else len(province['alias'])
        result['city'] = city['name']
        result['city_id'] = city['id']
        if city['name'] in text or city['alias'] in text:
            result['city_fit'] = len(city['name']) if city['name'] in text else len(city['alias'])
        result['county'] = county['name']
        result['county_id'] = county['id']
        result['county_fit'] = len(county['name']) if county['name'] in text else len(county['alias'])
        return [result]

    def smart_parse(self, candidates, text, all_result=False):
        result_list = list()
        result = []
        for candidate in candidates:
            if candidate['area_level'] == 1:
                result = self.parse_address_by_province(candidate, text)
            if candidate['area_level'] == 2:
                result = self.parse_address_by_city(candidate, text)
            if candidate['area_level'] == 3:
                result = self.parse_address_by_county(candidate, text)
            result_list.extend(result)
        results = set()
        for item in result_list:
            result = dict()
            result['province'] = item['province']
            result['city'] = item['city']
            result['county'] = item['county']
            result['province_id'] = item['province_id']
            result['city_id'] = item['city_id']
            result['county_id'] = item['county_id']
            result['fit'] = 0.4 * item['province_fit'] + 0.3 * item['city_fit'] + 0.3 * item['county_fit']
            results.add(tuple(result.items()))

        s = [dict(t) for t in results]
        s_sorted = sorted(s, key=lambda e: e.__getitem__('fit'), reverse=True)
        if all_result:
            return s_sorted
        return s_sorted[0]

    def __call__(self, address_text, all_result=False):
        if self.map_list is None:
            self._prepare()
        result = {'province': None,
                  'city': None,
                  'county': None,
                  'province_id': None,
                  'city_id': None,
                  'county_id': None,
                  'fit': 0
                  }

        candidates = self.get_candidates_result(address_text)
        if not candidates:
            return result

        result = self.smart_parse(candidates, address_text, all_result)

        return result