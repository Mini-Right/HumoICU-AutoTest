#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/5/1 02:50
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : token.py
# @Software    : PyCharm
# @Description :
from typing import Any, Optional, Union

from fastapi import Request, HTTPException
from jose import jwt

from humo.config import config
from humo.config.redis_key import REDIS_KEY_USER_TOKEN
from humo.plugins.session import RedisSession

ALGORITHM = "HS256"
NO_PARSE_TOKEN_API_LIST = [
    '/api/auth/register',
    '/api/auth/sign_in',
]


class Token(object):

    @staticmethod
    def create_access_token(subject: Union[str, Any]) -> str:
        """
        # 生成token
        :param subject: 保存到token的值
        :return:
        """
        to_encode = {"sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def check_jwt_token(token: Optional[str]) -> Union[str, Any]:
        """
        解析验证 headers中为token的值
        """
        try:
            user_id = Token.get_user_id(token)
            if RedisSession.HUMO.exists(f"user:{user_id}:token") == 1:
                RedisSession.HUMO.expire(
                    REDIS_KEY_USER_TOKEN.format(user_id=user_id), config.REQUEST_TIMEOUT
                )
            else:
                raise Exception("token失效 请重新登陆")
            return user_id
        except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
            # 抛出自定义异常， 然后捕获统一响应
            raise Exception("token失效 请重新登陆")

    @staticmethod
    def get_user_id(token: str):
        """根据token获取user_id"""
        try:
            payload = jwt.decode(token, config.JWT_SECRET, algorithms=[ALGORITHM])
            return payload['sub']
        except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
            # 抛出自定义异常， 然后捕获统一响应
            raise Exception("token失效 请重新登陆")

    @staticmethod
    def parse_request_header_token(request: Request):
        """解析请求头token"""
        try:
            # 不校验token
            if any(request.url.path.startswith(api) for api in NO_PARSE_TOKEN_API_LIST):
                return
            raw_token = request.headers.get("Authorization")
            token = raw_token.replace("Bearer ", "")
            user_id = Token.check_jwt_token(token)
            request.state.user_id = user_id
            return user_id
        except Exception as e:
            raise HTTPException(status_code=401)
