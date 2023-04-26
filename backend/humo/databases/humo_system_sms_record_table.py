#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 23:26
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : humo_sms_record_table.py
# @Software    : PyCharm
# @Description :

from sqlalchemy import Column, Integer, String, Text

from humo.databases import Base, gen_id


class HumoSystemSMSRecordTable(Base):
    __tablename__ = "humo_system_sms_record"
    __table_args__ = ({'comment': '短信发送记录表'})
    # 日志记录的唯一标识符
    id = Column(String(50), default=gen_id, primary_key=True, index=True)
    mobile = Column(String(15), nullable=False, comment="手机号")
    template_code = Column(String(15), nullable=False, comment="短信模板code")
    template_params = Column(Text, comment="短信模板参数")
    send_status_code = Column(Integer, nullable=False, comment="手机号")
    send_biz_id = Column(Text, comment="发送回执ID")
    send_code = Column(Text, comment="请求状态码")
    send_message = Column(Text, comment="状态码的描述")
    send_request_id = Column(Text, comment="请求ID")
