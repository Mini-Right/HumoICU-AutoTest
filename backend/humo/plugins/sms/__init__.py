#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 23:22
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
import json
import typing
from functools import wraps

from alibabacloud_dysmsapi20170525.models import SendSmsResponse

from humo.databases.humo_system_sms_record_table import HumoSystemSMSRecordTable
from humo.plugins.aliyun.sms import AliYunSMSService
from humo.plugins.curd import HumoTableCURD
from humo.plugins.logger import logger

T = typing.TypeVar("T")


def sms_record(func: T) -> T:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        payload, response = func(self, *args, **kwargs)
        logger.info(f"短信发送结果: {response}")
        response: SendSmsResponse
        HumoTableCURD().add_one(
            table_class=HumoSystemSMSRecordTable(
                mobile=payload.get('mobile'),
                template_code=payload.get('template_code'),
                template_params=json.dumps(payload.get('template_params')),
                send_status_code=response.status_code,
                send_biz_id=response.body.biz_id,
                send_code=response.body.code,
                send_message=response.body.message,
                send_request_id=response.body.request_id,
            )
        )

    return wrapper


class HumoSMSService(object):

    @sms_record
    def send_register_sms(self, mobile: str, code: str):
        """发送注册短信"""
        template_code = 'SMS_460610232'
        payload = dict(
            mobile=mobile,
            template_code=template_code,
            template_params={"code": code}
        )
        logger.info(f"短信发送信息: {payload}")
        return payload, AliYunSMSService().send_sms(**payload)


if __name__ == '__main__':
    HumoSMSService().send_register_sms('17601614656', '473415')
