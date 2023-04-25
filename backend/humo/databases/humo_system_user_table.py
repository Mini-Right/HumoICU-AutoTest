#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/25 23:22
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : humo_system_user_table.py
# @Software    : PyCharm
# @Description :
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, INTEGER

from humo.databases import Base, gen_id


class HumoSystemUserTable(Base):
    __tablename__ = "humo_system_user"
    __table_args__ = ({'comment': '系统用户表'})
    user_id = Column(VARCHAR(50), default=gen_id, primary_key=True, index=True)
    username = Column(VARCHAR(50), nullable=False, unique=True, comment="账号")
    nickname = Column(VARCHAR(50), nullable=False, comment="姓名")
    password = Column(VARCHAR(255), nullable=False, comment="密码")
    gender = Column(VARCHAR(1), default=0, comment="性别 1男 2女 0未知")
    mobile = Column(VARCHAR(11), comment="手机号")
    email = Column(VARCHAR(255), unique=True, comment="邮箱")
    signature = Column(LONGTEXT, comment="个性签名")
    avatar = Column(LONGTEXT, comment="头像")
    lark_suite_open_id = Column(VARCHAR(50), unique=True, comment="飞书账号openID")
    wechat_id = Column(VARCHAR(50), unique=True, comment="微信ID")
    status = Column(VARCHAR(1), default=0, comment="用户状态 1启用 0禁用")
    active = Column(INTEGER(1), default=0, comment="激活状态 1已激活 0未激活")
