#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:43
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : humo_api_record_table.py
# @Software    : PyCharm
# @Description :
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from humo.databases import Base, gen_id


class HumoSystemAPIRecordTable(Base):
    __tablename__ = "humo_system_api_record"
    __table_args__ = ({'comment': '接口请求记录表'})
    # 日志记录的唯一标识符
    id = Column(String(50), default=gen_id, primary_key=True, index=True)

    # 日志记录的时间戳，使用 UTC 时间表示
    timestamp = Column(DateTime, default=datetime.utcnow, comment="日志记录的时间戳，使用 UTC 时间表示")

    # 请求的 IP 地址
    ip_address = Column(String(15), comment="请求的 IP 地址")

    # 请求的 HTTP 方法（GET、POST、PUT 等）
    method = Column(String(10), comment="请求的 HTTP 方法（GET、POST、PUT 等）")

    # 请求的路径信息
    path = Column(String(255), comment="请求的路径信息")

    # 请求的查询参数，以字典形式存储
    query_params = Column(Text, comment="请求的查询参数，以字典形式存储")

    # 请求的头部信息，以字典形式存储
    request_headers = Column(Text, comment="请求的头部信息，以字典形式存储")

    # 请求的主体内容，以字符串形式存储
    request_body = Column(Text, comment="请求的主体内容，以字符串形式存储")

    # 请求的客户端类型和版本信息
    user_agent = Column(String(255), comment="请求的客户端类型和版本信息")

    # 来源页面的 URL 地址
    referrer = Column(String(255), comment="来源页面的 URL 地址")

    # 响应的 HTTP 状态码
    response_status = Column(Integer, comment="响应的 HTTP 状态码")

    # 响应的头部信息，以字典形式存储
    response_headers = Column(Text, comment="响应的头部信息，以字典形式存储")

    # 响应的主体内容，以字符串形式存储
    response_body = Column(Text, comment="响应的主体内容，以字符串形式存储")

    # 请求处理时长，以毫秒为单位
    process_time = Column(Integer, comment="请求处理时长，以毫秒为单位")

    def __repr__(self) -> str:
        return f"<HumoSystemAPIRecordTable(" \
               f"id={self.id}, " \
               f"timestamp='{self.timestamp}', " \
               f"ip_address='{self.ip_address}', " \
               f"method='{self.method}', " \
               f"path='{self.path}', " \
               f"query_params='{self.query_params}', " \
               f"request_headers='{self.request_headers}', " \
               f"request_body='{self.request_body}', " \
               f"user_agent='{self.user_agent}', " \
               f"referrer='{self.referrer}', " \
               f"response_status={self.response_status}, " \
               f"response_headers='{self.response_headers}', " \
               f"response_body='{self.response_body}', " \
               f"process_time={self.process_time}" \
               f">"
