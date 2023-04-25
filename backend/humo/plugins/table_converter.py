#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:35
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : data_handler.py
# @Software    : PyCharm
# @Description :

import decimal
from datetime import date, datetime

from sqlalchemy import func

from humo.plugins.json_encoders import jsonable_encoder


# 递归获取树形结构数据
def get_tree_data(paren_list, child_list):
    for paren in paren_list:
        for child in child_list:
            if paren["id"] == child["parent_id"]:
                if "children" in paren and child not in paren["children"]:
                    paren["children"].append(child)
                else:
                    paren["children"] = [child]
                get_tree_data(paren["children"], child_list)

    return paren_list


# orm方式： 将多条查询结果列表转化为对应字段的table_tree列表数据
def get_table_tree_data(table_data):
    paren_list = []
    child_list = []
    for dept in table_data:
        # 第一层
        if not dept["parent_id"]:
            paren_list.append(dept)
        else:
            child_list.append(dept)
    if not paren_list and child_list:
        table_tree_data = child_list
    else:
        # 递归获取子的层
        table_tree_data = get_tree_data(paren_list, child_list)

    return table_tree_data


def orm_fields_one_to_dict(result):
    """
    将一条查询的结果转化为对应字段的字典结果
    """
    if not result or isinstance(result, list):
        return {}
    return jsonable_encoder(dict(zip(result._fields, result._data)))


def orm_fields_all_to_list(result_list):
    """
   将多条查询的结果转化为对应字段的字典结果
   """
    if not isinstance(result_list, list):
        return []
    return jsonable_encoder([dict(zip(v._fields, v._data)) for v in result_list])


def orm_table_one_to_dict(table_cls, result):
    """
    将ORM表一条查询的结果转化为对应字段的字典结果
    """
    return_dict = {}
    if isinstance(result, table_cls):
        for key in result.__dict__:
            if key.startswith("_"):
                continue
            value = getattr(result, key)
            if isinstance(value, decimal.Decimal):
                value = float(value)
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            return_dict[key] = value
    return return_dict


def orm_table_all_to_list(table_cls, result_list):
    """
    将ORM表地盘条查询的结果转化为对应字段的字典结果
    """
    result = []
    for row in result_list:
        result.append(orm_table_one_to_dict(table_cls, row))
    return result


def orm_field_date_format(field):
    """将ORM表字段的值转YYYY-MM-DD格式"""
    return func.date_format(field, "%Y-%m-%d").label(field.key)
