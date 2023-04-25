#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:02
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : root_path.py
# @Software    : PyCharm
# @Description :
import os

__all__ = ['ROOT_PATH']


def root_path():
    return os.path.dirname(os.path.abspath(__file__))


ROOT_PATH = root_path()
