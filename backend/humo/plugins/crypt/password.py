#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:15
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : password.py
# @Software    : PyCharm
# @Description :
from passlib.context import CryptContext


class Password(object):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)


if __name__ == '__main__':
    print(Password().get_password_hash('123456'))