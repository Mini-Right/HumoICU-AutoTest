#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 00:50
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : config.schemas.py
# @Software    : PyCharm
# @Description :
import json
from typing import Optional

from pydantic import BaseModel, BaseSettings, Field


class DBItemSchema(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str = Field(default=None)


class DBSchemas(BaseModel):
    HUMO: DBItemSchema


class RedisItemSchema(BaseModel):
    host: str
    port: int
    db: int
    password: str = Field(default=None)


class RedisSchemas(BaseModel):
    HUMO: RedisItemSchema


class SMTPSchema(BaseModel):
    SENDER: str
    PASSWORD: str
    SMTP: str
    SSL: int


class ConfigSchema(BaseSettings):
    LOCAL_HOST: str
    JWT_SECRET: str
    REQUEST_TIMEOUT: int
    DB: Optional[DBSchemas] = None
    REDIS: Optional[RedisSchemas] = None
    SMTP: SMTPSchema

    class Config:
        allow_population_by_field_name = True
        env_file_encoding = 'utf-8'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, file_path: str) -> 'ConfigSchema':
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(**data)
