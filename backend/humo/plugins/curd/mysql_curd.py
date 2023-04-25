#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 02:09
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : mysql_curd.py
# @Software    : PyCharm
# @Description :
import logging
import typing
from functools import wraps
from typing import Any, List

from sqlalchemy import distinct, exists, text
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.orm import Session

from humo.plugins.session import MySQLSession
from humo.plugins.table_converter import (orm_fields_all_to_list, orm_fields_one_to_dict, orm_table_all_to_list, orm_table_one_to_dict)

__all__ = ['HumoTableCreate', 'HumoTableUpdate', 'HumoTableRead', 'HumoTableDelete']

logger = logging.getLogger(__name__)

T = typing.TypeVar("T")


def lower(func: T) -> T:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if kwargs.get('is_dict') and kwargs.get('is_lower'):
            result: dict = {
                key.lower() if type(key) == str else key: value
                for key, value in result.items()
            }
            return result
        elif kwargs.get('is_list') and kwargs.get('is_lower'):
            result_list = [
                {
                    key.lower() if type(key) == str else key: value
                    for key, value in some_dict.items()
                }
                for some_dict in result
            ]
            return result_list
        return result

    return wrapper


def count(func: T) -> T:
    @wraps
    def wrapper(self, *args, **kwargs):
        is_count = kwargs.get('is_count')
        result_list = func(self, *args, **kwargs)
        if not is_count:
            return result_list
        with self.session() as session:
            table_class = kwargs.get('table_class')
            table_fields_list = kwargs.get('table_fields_list')
            if table_class:
                query = session.query(table_class)
            else:
                query = session.query(*table_fields_list)
            params = kwargs.get('params')
            group_bys = kwargs.get('group_bys')
            if params:
                query = query.filter(*params)
            if group_bys:
                query = query.group_by(*group_bys)
            count = query.count()
            return result_list, count

    return wrapper


class CURDTableBase(object):
    def __init__(self, session=MySQLSession.HUMO):
        self.session = session

    def execute(self, sql: str, kwargs=None):
        with self.session() as session:
            session: Session
            session.execute(text(sql), kwargs)
            session.commit()


class HumoTableCreate(CURDTableBase):
    def __init__(self, session=MySQLSession.HUMO):
        super().__init__(session)

    def add_one(self, table_class: Any):
        """
        添加一条
        """
        with self.session() as session:
            session: Session
            try:
                with session.begin_nested():
                    session.add(table_class)
                    session.commit()
            except Exception as e:
                session.rollback()
                msg = f"插入失败: {e}"
                logger.warning(msg)
                raise Exception(msg)

    def add_list(self, table_class_list: List[Any]):
        """
        添加多条
        """
        with self.session() as session:
            session: Session
            try:
                with session.begin_nested():
                    session.add_all(table_class_list)
                session.commit()
            except Exception as e:
                session.rollback()
                msg = f"插入失败: {e}"
                logger.warning(msg)
                raise Exception(msg)


class HumoTableDelete(CURDTableBase):
    def __init__(self, session=MySQLSession.HUMO):
        super().__init__(session)

    def delete(self, table_class: Any, params: list):
        with self.session() as session:
            session: Session
            try:
                with session.begin_nested():
                    session.query(table_class).filter(*params).delete()
                    session.commit()
                    return True
            except Exception as e:
                session.rollback()
                msg = f"删除失败: {e}"
                logger.warning(msg)
                raise Exception(msg)


class HumoTableUpdate(CURDTableBase):
    def __init__(self, session=MySQLSession.HUMO):
        super().__init__(session)

    def update(self, table_class: Any, params: list, update: dict):
        with self.session() as session:
            session: Session
            try:
                session.query(table_class).filter(*params).update(update)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                msg = f"更新失败: {e}"
                logger.warning(msg)
                raise Exception(msg)


class HumoTableRead(CURDTableBase):
    def __init__(self, session=MySQLSession.HUMO):
        super().__init__(session)

    def query_count(self, table_class: object, params=None):
        if params is None:
            params = []
        with self.session() as session:
            return session.query(table_class).filter(*params).count()

    def query_exists(self, params: list):
        exist = exists()
        for i in params:
            exist = exist.where(i)
        with self.session() as session:
            return session.query(exist).scalar()

    def query_distinct(self, table_field, label: str, to_list: bool = False):
        with self.session() as session:
            query = (
                distinct(table_field).label(label) if label else distinct(table_field)
            )
            result = session.query(query).all()
            return orm_fields_all_to_list(result) if to_list else result

    @lower
    def query_table_one(
            self,
            table_class: object,
            params: list,
            is_dict: bool = False,
            is_lower: bool = False,
    ):
        with self.session() as session:
            result: table_class = session.query(table_class).filter(*params).first()
            if is_dict:
                result: dict = orm_table_one_to_dict(table_class, result)
            return result

    @lower
    def query_table_fields_one(
            self,
            table_fields_list: list,
            params: list,
            is_dict: bool = False,
            is_lower: bool = False,
    ):
        with self.session() as session:
            result = session.query(*table_fields_list).filter(*params).first()
            if is_dict:
                result: dict = orm_fields_one_to_dict(result)
            return result

    @lower
    def query_sql_one(
            self, sql: str, is_dict: bool = False, is_lower: bool = False
    ):
        with self.session() as session:
            result = session.execute(text(sql)).fetchone()
            if is_dict:
                result: dict = orm_fields_one_to_dict(result)
            return result

    @staticmethod
    def __query(
            query,
            params: list = None,
            page: int = None,
            limit: int = None,
            order_bys: list = None,
            group_bys: list = None,
    ):
        if params:
            query = query.filter(*params)
        if order_bys:
            query = query.order_by(*order_bys)
        if group_bys:
            query = query.group_by(*group_bys)
        if page and limit:
            query = query.limit(limit).offset((page - 1) * limit)
        return query

    @staticmethod
    def __count(query, params: list = None, group_bys: list = None):
        if params:
            query = query.filter(*params)
        if group_bys:
            query = query.group_by(*group_bys)
        return query.count()

    @staticmethod
    def __lower_list(result):
        result_list = [
            {
                key.lower() if type(key) == str else key: value
                for key, value in some_dict.items()
            }
            for some_dict in result
        ]
        return result_list

    def query_table_list(
            self,
            table_class: object,
            params: list = None,
            page: int = None,
            limit: int = None,
            order_bys: list = None,
            group_bys: list = None,
            is_list: bool = False,
            is_lower: bool = False,
            is_count: bool = False,
    ):

        with self.session() as session:
            query = session.query(table_class)
            result_list: List[table_class] = self.__query(
                query=query,
                params=params,
                page=page,
                limit=limit,
                order_bys=order_bys,
                group_bys=group_bys,
            ).all()
            if is_list:
                result_list: List[dict] = orm_table_all_to_list(
                    table_class, result_list
                )
            if is_list and is_lower:
                result_list = self.__lower_list(result_list)
            if is_count:
                return result_list, self.__count(query=query, params=params, group_bys=group_bys)
            return result_list

    def query_table_fields_list(
            self,
            table_fields_list: list,
            params: list = None,
            page: int = None,
            limit: int = None,
            order_bys: list = None,
            group_bys: list = None,
            is_list: bool = False,
            is_lower: bool = False,
            is_count: bool = False,
    ):

        with self.session() as session:
            query = session.query(*table_fields_list)
            result_list = self.__query(
                query=query,
                params=params,
                page=page,
                limit=limit,
                order_bys=order_bys,
                group_bys=group_bys,
            ).all()
            if is_list:
                result_list: List[dict] = orm_fields_all_to_list(result_list)
            if is_list and is_lower:
                result_list = self.__lower_list(result_list)
            if is_count:
                return self.__count(query=query, params=params, group_bys=group_bys)
            return result_list

    def query_table_all(
            self,
            table_class: object,
            params: list = None,
            order_bys: list = None,
            group_bys: list = None,
            is_list: bool = False,
            is_lower: bool = False,
            is_count: bool = False,
    ):

        with self.session() as session:
            query = session.query(table_class)
            result_list: List[table_class] = self.__query(
                query=query, params=params, order_bys=order_bys, group_bys=group_bys
            ).all()
            if is_list:
                result_list: List[dict] = orm_table_all_to_list(
                    table_class, result_list
                )
            if is_list and is_lower:
                result_list = self.__lower_list(result_list)
            if is_count:
                return self.__count(query=query, params=params, group_bys=group_bys)
            return result_list

    def query_table_fields_all(
            self,
            table_fields_list: list,
            params: list = None,
            order_bys: list = None,
            group_bys: list = None,
            is_list: bool = False,
            is_lower: bool = False,
            is_count: bool = False,
    ):

        with self.session() as session:
            query = session.query(*table_fields_list)
            result_list = self.__query(
                query=query, params=params, order_bys=order_bys, group_bys=group_bys
            ).all()
            if is_list:
                result_list: List[dict] = orm_fields_all_to_list(result_list)
            if is_list and is_lower:
                result_list = self.__lower_list(result_list)
            if is_count:
                return self.__count(query=query, params=params, group_bys=group_bys)
            return result_list

    def query_sql_list(
            self, sql: str, is_list: bool = False, is_lower: bool = False
    ):
        with self.session() as session:
            try:
                result_list = session.execute(text(sql)).fetchall()
            except ResourceClosedError as e:
                logger.warning(e)
                return [{}]
            if is_list:
                result_list: List[dict] = orm_fields_all_to_list(result_list)
            if is_list and is_lower:
                result_list = self.__lower_list(result_list)
            return result_list

    def query_table_column_options(self, table_name: str, column: str, where: str = ''):
        SQL = f"SELECT DISTINCT r.{column} FROM {table_name} r WHERE {where} r.{column} IS NOT NULL;"
        table_data = self.query_sql_list(sql=SQL, is_list=True)
        options = [{'label': _.get(column), 'value': _.get(column)} for _ in table_data]
        return options



