#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 02:05
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : mysql.py
# @Software    : PyCharm
# @Description :
from urllib import parse

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from humo.config import DBItemSchema, config


class MySQLSessionGenerate(object):
    _session = None

    def __init__(self, database_config: DBItemSchema = config.DB.HUMO):
        self.database_config = database_config

    @property
    def session(self):
        if not self._session:
            engine = self.init_engine()
            self._session = scoped_session(sessionmaker(bind=engine))
        return self._session

    def init_engine(self):
        if self.database_config.database:
            uri = f"mysql+pymysql://{self.database_config.user}:{parse.quote_plus(self.database_config.password)}@{self.database_config.host}:{self.database_config.port}/{self.database_config.database}?charset=utf8mb4"
        else:
            uri = f"mysql+pymysql://{self.database_config.user}:{parse.quote_plus(self.database_config.password)}@{self.database_config.host}:{self.database_config.port}/?charset=utf8mb4"
        return create_engine(
            uri,
            poolclass=QueuePool,
            pool_size=8,
            max_overflow=16,
            pool_recycle=1800,
            echo=False,
        )

    def execute(self, sql: str, kwargs=None):
        if not kwargs:
            kwargs = {}
        self.session.execute(text(sql), kwargs)
        self.session.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.close()
