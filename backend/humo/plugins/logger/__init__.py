#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/26 01:16
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from humo.plugins.logger.request_id import get_request_id
from root_path import ROOT_PATH


class RequestFilter(logging.Filter):
    def filter(self, record):
        request_id = get_request_id()
        record.request_id = request_id
        return True


if not os.path.exists(f'{ROOT_PATH}/logs'):
    os.mkdir(f"{ROOT_PATH}/logs")

log_formatter = logging.Formatter('%(asctime)s [%(thread)s] [%(levelname)s] [%(request_id)s] [%(module)s.%(funcName)s] %(message)s')
log_file_handler = RotatingFileHandler(f'{ROOT_PATH}/logs/debug-{datetime.now().strftime("%Y-%m-%d")}.log', maxBytes=1000000, backupCount=10)
log_file_handler.setFormatter(log_formatter)
log_file_handler.addFilter(RequestFilter())

log_console_handler = logging.StreamHandler()
log_console_handler.setFormatter(log_formatter)
log_console_handler.addFilter(RequestFilter())

# 创建日志记录器 logger
logger = logging.getLogger('humo')
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    logger.addHandler(log_console_handler)
    logger.addHandler(log_file_handler)
