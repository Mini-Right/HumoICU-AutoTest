#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 22:59
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : sms.py
# @Software    : PyCharm
# @Description :
import json

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_dysmsapi20170525.models import SendSmsResponse, QuerySendDetailsResponse
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from humo.plugins.aliyun import AliYunService


class AliYunSMSService(AliYunService):
    def __init__(self):
        super().__init__()
        self.config.endpoint = 'dysmsapi.aliyuncs.com'
        self.client = Dysmsapi20170525Client(self.config)
        # 短信签名名称
        self.sign_name = 'HumoICU'

    def send_sms(self, mobile: str, template_code: str, template_params: dict) -> SendSmsResponse:
        """
        发送短信
        :param mobile:              手机号
        :param template_code:       模板编码
        :param template_params:     模板参数
        :return:
        """
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=mobile,
            sign_name=self.sign_name,
            template_code=template_code,
            template_param=json.dumps(template_params),
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = self.client.send_sms_with_options(request=send_sms_request, runtime=runtime)
            return response
        except Exception as e:
            UtilClient.assert_as_string(e.message)

    def query_send_detail(self, mobile: str, send_biz_id: str, send_date: str) -> QuerySendDetailsResponse:
        """
        查询短信发送详情
        :param mobile:          手机号
        :param send_biz_id:     回执ID
        :param send_date:       发送时间
        :return:
        """
        query_send_details_request = dysmsapi_20170525_models.QuerySendDetailsRequest(
            phone_number=mobile,
            send_date=send_date,
            page_size=1,
            current_page=1,
            biz_id=send_biz_id
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = self.client.query_send_details_with_options(query_send_details_request, runtime)
            return response
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
