#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:04
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from humo.apps.auth.routers import auth

api = APIRouter()

api.include_router(router=auth, prefix='/auth', tags=['鉴权'])
