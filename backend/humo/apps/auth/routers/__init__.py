#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from humo.apps.auth.routers.auth_register_routers import register

auth = APIRouter()

auth.include_router(router=register, prefix='/register', tags=['注册'])
