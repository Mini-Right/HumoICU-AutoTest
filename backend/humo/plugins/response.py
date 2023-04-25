#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 02:01
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : response.py
# @Software    : PyCharm
# @Description :
from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def response(
        data: Union[list, dict, str, any] = None,
        msg: str = None,
        code: int = 200,
        status_code: int = 200,
) -> JSONResponse:
    """
    根据输入参数返回JSON格式的响应。
    Args:
        data (Union[list, dict, str, any]): 响应数据，默认为None。
        msg (str): 响应消息，默认为None。
        code (int): 响应码，默认为200。
        status_code (int): HTTP状态码，默认为200。
    Returns:
        JSONResponse: 包含响应内容和状态码的FastAPI响应对象。
    """
    content = {
        "data": data,
        "msg": msg,
        "code": code,
    }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


def success_response(
        data: Union[list, dict, str, any] = None,
        msg: str = "成功"
) -> JSONResponse:
    """
    返回成功响应。默认状态码为200，响应码为200。
    Args:
        data (Union[list, dict, str, any]): 响应数据，默认为None。
        msg (str): 响应消息，默认为“成功”。
    Returns:
        JSONResponse: 包含成功响应的FastAPI响应对象。
    """
    return response(data=data, msg=msg, code=200, status_code=200)


def fail_response(
        data: Union[list, dict, str, any] = None,
        msg: str = None
) -> JSONResponse:
    """
    返回失败响应。默认状态码为500，响应码为500。
    Args:
        data (Union[list, dict, str, any]): 响应数据，默认为None。
        msg (str): 响应消息，默认为None。
    Returns:
        JSONResponse: 包含失败响应的FastAPI响应对象。
    """
    return response(data=data, msg=msg, code=500, status_code=500)


def login_fail_response(
        data: Union[list, dict, str, any] = None,
        msg: str = None
) -> JSONResponse:
    """
    返回登录失败响应。默认状态码为401，响应码为500。
    Args:
        data (Union[list, dict, str, any]): 响应数据，默认为None。
        msg (str): 响应消息，默认为None。
    Returns:
        JSONResponse: 包含登录失败响应的FastAPI响应对象。
    """
    return response(data=data, msg=msg, code=500, status_code=401)
