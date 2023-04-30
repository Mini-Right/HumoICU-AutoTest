#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 03:54
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_user_info_routers.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter, Request

from humo.apps.auth.services.auth_user_info_service import HumoAuthUserInfoService
from humo.plugins.crypt.token import Token
from humo.plugins.response import success_response, fail_response

user = APIRouter()


@user.get('/info', name='用户信息获取')
def auth_user_info(request: Request):
    try:
        user_id = request.state.user_id
        result = HumoAuthUserInfoService.main(user_id=user_id)
        return success_response(data=result, msg='账号密码登录成功')
    except Exception as e:
        return fail_response(msg=str(e))
