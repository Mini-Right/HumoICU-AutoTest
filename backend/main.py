#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 00:44
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : main.py
# @Software    : PyCharm
# @Description :
import uvicorn
from humo import humo


if __name__ == "__main__":
    uvicorn.run(
        'humo.__init__:humo',
        host="0.0.0.0",
        port=5004,
        workers=1
    )
