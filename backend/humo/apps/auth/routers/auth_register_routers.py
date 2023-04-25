#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 01:52
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_register_routers.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from humo.apps.auth.schemas.auth_register_schemas import HumoAuthRegisterSchema
from humo.apps.auth.services.auth_register_service import HumoAuthRegisterService
from humo.plugins.response import success_response, fail_response

register = APIRouter()


@register.post('/email', name='新用户注册')
def auth_register(data: HumoAuthRegisterSchema):
    try:
        HumoAuthRegisterService().main(data=data)
        return success_response(msg='激活邮件已发送')
    except Exception as e:
        return fail_response(msg=str(e))


@register.get('/active', name='新用户激活')
def auth_register_active(token: str):
    try:
        HumoAuthRegisterService().active(token)
        return success_response(msg='用户激活成功')
    except Exception as e:
        return fail_response(msg=str(e))
