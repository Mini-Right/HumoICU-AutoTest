#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/4/9 15:54
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 也可以设置为"*"，即为所有。
        allow_credentials=True,
        allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
        allow_headers=["*"],  # 允许跨域的headers，可以用来鉴别来源等作用。
    )
