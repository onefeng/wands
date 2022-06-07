# wands

## 概览

wands项目意为“魔杖”，最初的目的是为了智能解析快递单国内省市区的地址，无需完整地址也能正确匹配，最后返回一个最有可能的结果，本项目的数据来源2021年[国家统计局](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html) 。 \
解析的算法基于树结构搜索和最大匹配概率实现，后面会将其他文本解析功能加入到项目中。\
为了使不同语言都能调用，这里提供api接口，可部署为单体应用。

## 安装

```shell
pip install wands-ce
```

## 开始使用

1.python调用

```python
import wands

text = '涪城区'
result = wands.parse_address(text)
print(result)
"""
{
    'province': '四川省', 
    'city': '绵阳市', 
    'county': '涪城区', 
    'province_id': 51, 
    'city_id': 5107, 
    'county_id': 510703, 
    'fit': 0.8999999999999999 # 值越大可信度越高
}
"""
```

2.api接口调用

开发环境快速部署命令
```shell
wands runserver --host=0.0.0.0 --port=9989
```

请求地址:

http://localhost:9989/address?area=山西城区

请求方式：GET

响应示例

```json
{
    "code": 200,
    "data": {
        "city": "晋城市",
        "city_id": 1405,
        "county": "城区",
        "county_id": 140502,
        "fit": 1.4,
        "province": "山西省",
        "province_id": 14
    },
    "message": "success"
}
```

3.docker部署

```shell
docker run --name wands-ce -d -p 9989:9989 onefeng/wands-ce
```

生产环境建议使用docker部署

## 致谢

感谢[tenkola](https://github.com/tenkola) 提供的爬虫脚本，和数据的清洗。可以抓取不同年份和层级的数据，脚本在script目录。
