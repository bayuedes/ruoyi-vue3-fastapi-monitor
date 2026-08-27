"""监控看板 Controller - 展示统计数据 + 3 个测试问题对应的接口"""
from typing import Annotated, Any

from fastapi import Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from common.vo import DynamicResponseModel, ResponseBaseModel
from module_monitor.service.monitor_service import MonitorDashboardService
from utils.log_util import logger
from utils.response_util import ResponseUtil


# 响应模型
class DeviceCountModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    device_count: int = Field(description='监控设备总数')


class CpuTopItemModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    resource_id: str | None = Field(default=None, description='资源ID')
    resource_name: str | None = Field(default=None, description='资源名称')
    resource_ip: str | None = Field(default=None, description='资源IP')
    value_word: str | None = Field(default=None, description='CPU利用率%')


class CpuTopResponseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    data: list[CpuTopItemModel] = Field(default_factory=list, description='CPU Top 列表')


class PingHistoryItemModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None, description='取值ID(含时间戳)')
    scaning_id: str | None = Field(default=None, description='子资源ID')
    index_id: str | None = Field(default=None, description='指标ID')
    index_value: str | None = Field(default=None, description='Ping响应时间(ms)')
    scan_time: str | None = Field(default=None, description='取值时间')


class PingHistoryResponseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    ip: str = Field(description='查询的IP')
    data: list[PingHistoryItemModel] = Field(default_factory=list, description='最近10次Ping记录')


dashboard_controller = APIRouterPro(
    prefix='/monitor/dashboard', order_num=25, tags=['监控管理-看板统计'], dependencies=[PreAuthDependency()]
)


@dashboard_controller.get(
    '/deviceCount',
    summary='Q1 监控了多少台设备',
    description='查询当前监控的设备总数 (it_resource_list 表中 delete_time 为空)',
    response_model=DynamicResponseModel[DeviceCountModel],
)
async def get_device_count(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    count = await MonitorDashboardService.get_device_count(query_db)
    logger.info(f'监控设备总数: {count}')
    return ResponseUtil.success(model_content=DeviceCountModel(device_count=count))


@dashboard_controller.get(
    '/topCpu',
    summary='Q2 当前平均CPU利用率最高的10台设备',
    description='从 it_value_list 关联 it_resource_index 平均CPU利用率 指标, 取 Top 10',
    response_model=DynamicResponseModel[CpuTopResponseModel],
)
async def get_top_cpu_devices(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    limit: Annotated[int, Query(description='返回条数, 默认10')] = 10,
) -> Response:
    rows: list[dict[str, Any]] = await MonitorDashboardService.get_top_cpu_devices(query_db, limit=limit)
    items = [CpuTopItemModel.model_validate(r) for r in rows]
    logger.info(f'获取CPU Top{limit} 设备: {len(items)} 条')
    return ResponseUtil.success(model_content=CpuTopResponseModel(data=items))


@dashboard_controller.get(
    '/recentPing',
    summary='Q3 指定资源IP最近的十次Ping响应时间',
    description='根据 IP 找到资源, 然后从 it_<resource_id> 历史表查询 Ping响应时间 最近10条',
    response_model=DynamicResponseModel[PingHistoryResponseModel],
)
async def get_recent_ping(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    ip: Annotated[str, Query(description='资源管理IP, 如 192.168.145.253')],
    limit: Annotated[int, Query(description='返回条数, 默认10')] = 10,
) -> Response:
    rows: list[dict[str, Any]] = await MonitorDashboardService.get_recent_ping_by_ip(query_db, ip, limit=limit)
    items = [PingHistoryItemModel.model_validate(r) for r in rows]
    logger.info(f'获取 {ip} 最近{limit}次Ping记录: {len(items)} 条')
    return ResponseUtil.success(model_content=PingHistoryResponseModel(ip=ip, data=items))
