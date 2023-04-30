#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:06
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_register_service.py
# @Software    : PyCharm
# @Description :
import random
import secrets
import uuid

from jinja2 import Template

from humo.apps.auth.schemas.auth_register_schemas import HumoAuthRegisterSchema, HumoAuthEmailRegisterSchema, HumoAuthMobileRegisterSchema
from humo.config import config
from humo.config.redis_key import REDIS_KEY_REGISTER_SEND_CODE_COUNT, REDIS_KEY_REGISTER_MOBILE_CODE, REDIS_KEY_REGISTER_EMAIL
from humo.databases.humo_system_user_table import HumoSystemUserTable
from humo.plugins.crypt import Password
from humo.plugins.curd import HumoTableCURD
from humo.plugins.email import SendEmail
from humo.plugins.logger import logger
from humo.plugins.session import RedisSession
from humo.plugins.sms import HumoSMSService
from humo.plugins.time_utils import get_any_datetime, get_current_datetime, get_seconds_until_tomorrow
from humo.plugins.validates import verify_email, verify_mobile
from root_path import ROOT_PATH


class HumoAuthRegisterService(object):

    def main(self, data: HumoAuthRegisterSchema):
        logger.info(f"新用户注册: {data.dict()}")
        if HumoTableCURD().query_exists(params=[HumoSystemUserTable.username == data.username]):
            raise Exception('用户名已存在')

    @staticmethod
    def register(data: HumoAuthRegisterSchema):
        """注册用户"""
        user_id = uuid.uuid4().hex
        HumoTableCURD().add_one(
            table_class=HumoSystemUserTable(
                user_id=user_id,
                username=data.username,
                password=Password().get_password_hash(data.password),
                nickname=data.username,
                mobile=data.mobile,
                email=data.email,
                avatar='https://humo-bucket.oss-cn-beijing.aliyuncs.com/icu/avatar.png',
                status=0,
                active=0,
            )
        )
        logger.info(f"用户信息插入数据库成功 user_id: {user_id}")
        return user_id


class HumoAuthMobileRegisterService(HumoAuthRegisterService):

    def __init__(self):
        super().__init__()

    @staticmethod
    def __send_code_count(mobile: str):
        """发送注册短信次数"""
        send_code_count = RedisSession.HUMO.get(REDIS_KEY_REGISTER_SEND_CODE_COUNT.format(mobile=mobile))
        logger.info(f"手机号当日发送注册短信次数 {mobile}: {send_code_count}")
        if send_code_count is not None and int(send_code_count) > 3:
            raise Exception('今日短信发送过多 请明日再试')

    def send_code(self, mobile: str):
        """发送注册验证码"""
        if not verify_mobile(mobile):
            raise Exception('手机号格式非法 请检查')
        self.__send_code_count(mobile=mobile)
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        logger.info(f"发送注册验证码开始 {mobile}: {code}")
        HumoSMSService().send_register_sms(mobile=mobile, code=code)
        RedisSession.HUMO.set(
            name=REDIS_KEY_REGISTER_MOBILE_CODE.format(mobile=mobile),
            value=code,
            ex=60 * 10
        )
        # 手机号发送次数计数并设置过期时间 23:9:59
        redis_count_key = REDIS_KEY_REGISTER_SEND_CODE_COUNT.format(mobile=mobile)
        RedisSession.HUMO.incr(name=redis_count_key)
        RedisSession.HUMO.expire(name=redis_count_key, time=get_seconds_until_tomorrow())
        logger.info(f"发送注册验证码结束 {mobile}: {code}")

    @staticmethod
    def check_verification_code(mobile: str, code: str):
        """校验注册验证码"""
        verification_code = RedisSession.HUMO.get(name=REDIS_KEY_REGISTER_MOBILE_CODE.format(mobile=mobile))
        if not verification_code:
            raise Exception('验证码已失效 请重试')
        if verification_code != code:
            raise Exception('验证码错误 请重试')

    def main(self, data: HumoAuthMobileRegisterSchema):
        super().main(HumoAuthRegisterSchema(**data.dict()))
        if not verify_mobile(data.mobile):
            raise Exception('手机号格式非法 请检查')
        if HumoTableCURD().query_exists(params=[HumoSystemUserTable.mobile == data.mobile]):
            raise Exception('手机号已存在')
        self.check_verification_code(mobile=data.mobile, code=data.code)
        self.register(HumoAuthRegisterSchema(**data.dict()))


class HumoAuthEmailRegisterService(HumoAuthRegisterService):
    def __init__(self):
        super().__init__()

    def main(self, data: HumoAuthEmailRegisterSchema):
        super().main(HumoAuthRegisterSchema(**data.dict()))
        if not verify_email(data.email):
            raise Exception('邮箱格式非法 请检查')
        if HumoTableCURD().query_exists(params=[HumoSystemUserTable.email == data.email]):
            raise Exception('邮箱已存在')
        user_id = self.register(HumoAuthRegisterSchema(**data.dict()))
        self.send_email_captcha(user_id=user_id, data=data)

    @staticmethod
    def generate_activation_token():
        # 使用HMAC算法对用户ID和随机字节串进行散列运算，以生成唯一的令牌
        token = secrets.token_urlsafe(64)
        return token

    def send_email_captcha(self, user_id: str, data: HumoAuthEmailRegisterSchema):
        hour = 6
        token = self.generate_activation_token()
        activation_link = f"{config.LOCAL_HOST}/api/auth/register/active?token={token}"
        logger.info(f"激活链接  {user_id}: {activation_link}")
        deadline = get_any_datetime(date_time=get_current_datetime(), hour=hour)
        RedisSession.HUMO.set(
            name=REDIS_KEY_REGISTER_EMAIL.format(token=token),
            value=user_id,
            ex=60 * 60 * hour
        )
        with open(f"{ROOT_PATH}/humo/apps/auth/services/active.html") as f:
            html = f.read()
        template = Template(html)
        email_content = template.render(username=data.username, activation_link=activation_link, deadline=deadline)

        SendEmail().send(
            subject="激活您的账户 【HumoICU】",
            content=email_content,
            to_list=[data.email]
        )
        logger.info(f"发送激活邮件成功")

    @staticmethod
    def active(token: str):
        redis_key = REDIS_KEY_REGISTER_EMAIL.format(token=token)
        logger.info(f"注册用户激活 {redis_key}")
        user_id = RedisSession.HUMO.get(redis_key)
        logger.info(f"查询token对应user_id: {user_id}")
        if user_id:
            HumoTableCURD().update(
                table_class=HumoSystemUserTable,
                params=[HumoSystemUserTable.user_id == user_id],
                update=dict(
                    status=1,
                    active=1,
                )
            )
            logger.info(f"注册用户激活成功: {user_id}")
            RedisSession.HUMO.delete(redis_key)
            return

        token_invalid_message = f'激活链接已失效: {token}'
        logger.warning(token_invalid_message)
        raise Exception(token_invalid_message)


if __name__ == '__main__':
    HumoAuthMobileRegisterService().send_code('17601614656')
