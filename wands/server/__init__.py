# -*- coding: utf-8 -*-

"""
@author: onefeng
@time: 2022/5/23 10:53
"""

from flask import Flask

from .views import register_api


def create_app(name):
    app = Flask(name)
    app.config["JSON_AS_ASCII"] = False
    register_api(app)
    return app
