#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 03:05
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_sign_in_routers.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from humo.apps.auth.schemas.auth_sign_in_schemas import HumoAuthSignInAccountSchema
from humo.apps.auth.services.auth_sign_in_service import HumoAuthSignInAccountService
from humo.plugins.response import success_response, fail_response

sign_in = APIRouter()


@sign_in.post('/account', name='账号密码登录')
def auth_sign_in_account(data: HumoAuthSignInAccountSchema):
    try:
        result = HumoAuthSignInAccountService().main(data=data)
        return success_response(data=result, msg='账号密码登录成功')
    except Exception as e:
        return fail_response(msg=str(e))
