#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/4/18 01:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py
# @Software    : PyCharm
# @Description :
import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from humo.plugins.logger.request_id import set_request_id
from humo.apps import api
from humo.databases.humo_system_api_record_table import HumoSystemAPIRecordTable
from humo.plugins.curd import HumoTableCURD
from humo.plugins.middlewares import middlewares
from root_path import ROOT_PATH

humo = FastAPI(
    title='HumoICU AutoTest',
    version='0.0.1',
    docs_url=None,
    redoc_url=None,
)

humo.mount(path='/static', app=StaticFiles(directory=f"{ROOT_PATH}/static"), name='static')

humo.include_router(router=api, prefix='/api')


@humo.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=humo.openapi_url,
        title="HumoICU AutoTest",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url='/static/favicon.jpeg',
    )


middlewares(humo)

@humo.middleware('http')
async def process_timer(request: Request, call_next):

    request_id = uuid.uuid4().hex
    set_request_id(request_id)

    start_time = datetime.utcnow()
    # 获取请求 IP 地址
    ip_address = request.client.host

    # 获取请求方法和路径
    method = request.method
    path = str(request.url.path)

    # 读取查询参数
    query_params = dict(request.query_params)

    # 读取请求头和请求体
    request_headers = dict(request.headers)
    # request_body = await request.body()

    # 读取用户代理和 Referrer
    user_agent = request_headers.get("User-Agent")
    referrer = request_headers.get("Referer")

    response = await call_next(request)

    # 读取响应状态、响应头和响应体
    response_status = response.status_code
    response_headers = dict(response.headers)

    # 计算请求时长
    end_time = datetime.utcnow()
    process_time = (end_time - start_time).total_seconds() * 1000

    api_record_info = dict(
        timestamp=start_time,
        ip_address=ip_address,
        method=method,
        path=path,
        query_params=str(query_params),
        request_headers=str(request_headers),
        # request_body=request_body,
        user_agent=user_agent,
        referrer=referrer,
        response_status=response_status,
        response_headers=str(response_headers),
        # response_body=response_body,
        process_time=process_time
    )

    HumoTableCURD().add_one(
        table_class=HumoSystemAPIRecordTable(
            **api_record_info
        )
    )

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    return response


@humo.get('/get')
def haha(name: str):
    return f"{name}"
