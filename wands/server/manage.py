# -*- coding: utf-8 -*-

"""
@author: onefeng
@time: 2022/5/23 11:41
"""

from wands.server import create_app

app = create_app(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9989)
