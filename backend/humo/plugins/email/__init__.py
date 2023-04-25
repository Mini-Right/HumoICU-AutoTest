#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 00:28
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

import logging

from yagmail import SMTP

from humo.config import config

logger = logging.getLogger(__name__)


class SendEmail(object):
    def __init__(self):
        self.yag = SMTP(
            user=config.SMTP.SENDER,
            password=config.SMTP.PASSWORD,
            host=config.SMTP.SMTP,
        )

    def send(
            self,
            subject: str,
            content: str,
            to_list: list,
            cc_list: list = None,
            file_path=None,
    ):
        logger.info(f"{'=' * 10} 发送邮件开始 {'=' * 10}")
        logger.info(f"subject: {subject}")
        logger.info(f"content: {content}")
        logger.info(f"to_list: {to_list}")
        logger.info(f"cc_list: {cc_list}")
        logger.info(f"file_path: {file_path}")
        # 发送邮件
        self.yag.send(
            # to 收件人，如果一个收件人用字符串，多个收件人用列表即可
            to=to_list,
            # cc 抄送，含义和传统抄送一致，使用方法和to 参数一致
            cc=cc_list,
            # subject 邮件主题（也称为标题）
            subject=subject,
            # contents 邮件正文
            contents=content,
            # attachments 附件，和收件人一致，如果一个附件用字符串，多个附件用列表
            attachments=[file_path] if file_path else [],
        )
        # 记得关掉链接，避免浪费资源
        self.yag.close()
        logger.info(f"{'=' * 10} 发送邮件完成 {'=' * 10}")
