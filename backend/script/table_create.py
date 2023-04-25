#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 02:45
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : table_create.py
# @Software    : PyCharm
# @Description :
import importlib
import os

from humo.plugins.session import MySQLSessionGenerate
from root_path import ROOT_PATH


def init_table():
    """创建指定表"""
    from humo.databases.humo_api_record_table import Base
    Base.metadata.create_all(MySQLSessionGenerate().init_engine())


def init_all_tables():
    """创建所有表"""
    filenames = os.listdir(f"{ROOT_PATH}/humo/databases")
    for filename in filenames:
        if filename.endswith('table.py'):
            module_name: str = os.path.splitext(filename)[0]
            model_path = f"humo.databases.{module_name}"
            module = importlib.import_module(model_path)

            base = getattr(module, 'Base')
            base.metadata.create_all(MySQLSessionGenerate().init_engine())


if __name__ == '__main__':
    init_all_tables()
