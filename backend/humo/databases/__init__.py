#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:37
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

import uuid
from datetime import datetime

from sqlalchemy import Column, func, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base, declared_attr

base = declarative_base()


def gen_id():
    return uuid.uuid4().hex


class Base(base):
    __abstract__ = True
    # id = Column(VARCHAR(50), default=gen_id, primary_key=True, index=True)
    create_time = Column(DATETIME, default=datetime.now, server_default=func.now(), comment="创建时间")
    update_time = Column(DATETIME, default=datetime.now, onupdate=datetime.now, server_default=func.now(), server_onupdate=func.now(), comment="更新时间")
    create_user = Column(VARCHAR(50), default='pomelo', comment="创建人")
    operation_user = Column(VARCHAR(50), default='pomelo', comment="更新人")
    remark = Column(LONGTEXT, comment="备注")
    is_delete = Column(INTEGER(11), server_default=text("'0'"), comment="逻辑删除:0=未删除,1=删除")

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        import re

        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表名格式替换成 下划线_格式 如 MallUser 替换成 mall_user
        return "_".join(name_list).lower()

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
