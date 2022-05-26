# wands

## 概览
wands项目意为“魔杖”，主要是想继承一些基础服务的用法提供接口，目前实现地址的解析。

## 环境部署
pip install wheel
pip install twine


python setup.py upload

wands runserver --host=0.0.0.0 --port=7689


gunicorn -w 4 -b 0.0.0.0:9989 wands.server.manage:app

gunicorn wands.server.manage:app -c ./gunicorn.conf.py --access-logfile -

