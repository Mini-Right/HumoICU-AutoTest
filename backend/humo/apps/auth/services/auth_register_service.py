#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:06
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : auth_register_service.py
# @Software    : PyCharm
# @Description :
import secrets
import uuid

from jinja2 import Template

from humo.apps.auth.schemas.auth_register_schemas import HumoAuthRegisterSchema
from humo.config import config
from humo.databases.humo_system_user_table import HumoSystemUserTable
from humo.plugins.crypt import Password
from humo.plugins.curd import HumoTableCURD
from humo.plugins.email import SendEmail
from humo.plugins.logger import logger
from humo.plugins.session import RedisSession
from humo.plugins.time_utils import get_any_datetime, get_current_datetime
from humo.plugins.validates import verify_email
from root_path import ROOT_PATH


class HumoAuthRegisterService(object):
    def main(self, data: HumoAuthRegisterSchema):
        logger.info(f"新用户注册: {data.dict()}")
        if not verify_email(data.email):
            raise Exception('邮箱格式非法 请检查')
        if HumoTableCURD().query_exists(params=[HumoSystemUserTable.username == data.username]):
            raise Exception('用户名已存在')
        if HumoTableCURD().query_exists(params=[HumoSystemUserTable.email == data.email]):
            raise Exception('邮箱已存在')
        user_id = self.register(data)
        self.send_email_captcha(user_id=user_id, data=data)

    @staticmethod
    def register(data: HumoAuthRegisterSchema):
        user_id = uuid.uuid4().hex
        HumoTableCURD().add_one(
            table_class=HumoSystemUserTable(
                user_id=user_id,
                username=data.username,
                password=Password().get_password_hash(data.password),
                nickname=data.username,
                email=data.email,
                avatar='https://humo-bucket.oss-cn-beijing.aliyuncs.com/icu/avatar.png',
                status=0,
                active=0,
            )
        )
        logger.info(f"用户信息插入数据库成功 user_id: {user_id}")
        return user_id

    @staticmethod
    def generate_activation_token():
        # 使用HMAC算法对用户ID和随机字节串进行散列运算，以生成唯一的令牌
        token = secrets.token_urlsafe(64)
        return token

    def send_email_captcha(self, user_id: str, data: HumoAuthRegisterSchema):
        hour = 6
        token = self.generate_activation_token()
        activation_link = f"{config.LOCAL_HOST}/api/auth/register/active?token={token}"
        logger.info(f"激活链接  {user_id}: {activation_link}")
        deadline = get_any_datetime(date_time=get_current_datetime(), hour=hour)
        RedisSession.HUMO.set(
            name=f'register:{token}',
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
        redis_key = f"register:{token}"
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
