#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter, Depends

from humo.apps.auth.routers.auth_register_routers import register
from humo.apps.auth.routers.auth_sign_in_routers import sign_in
from humo.apps.auth.routers.auth_user_info_routers import user
from humo.plugins.crypt.token import Token

auth = APIRouter()

auth.include_router(router=register, prefix='/register', tags=['注册'])
auth.include_router(router=sign_in, prefix='/sign_in', tags=['登录'])
auth.include_router(router=user, prefix='/user', tags=['用户信息'], dependencies=[Depends(Token.parse_request_header_token)])


