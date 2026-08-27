"""监控模块 CRUD Controller - 5 个表的增删改查"""
from typing import Annotated

from fastapi import Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_monitor.entity.vo.monitor_vo import (
    ItResourceIndexModel,
    ItResourceIndexPageQueryModel,
    ItResourceListModel,
    ItResourceListPageQueryModel,
    ItResourceScanModel,
    ItResourceScanPageQueryModel,
    ItResourceScaningModel,
    ItResourceScaningPageQueryModel,
    ItValueListModel,
    ItValueListPageQueryModel,
)
from module_monitor.service.monitor_service import (
    MonitorIndexService,
    MonitorResourceService,
    MonitorScanService,
    MonitorScaningService,
    MonitorValueService,
)
from utils.log_util import logger
from utils.response_util import ResponseUtil


# ============ 指标管理 ============
index_controller = APIRouterPro(
    prefix='/monitor/index', order_num=20, tags=['监控管理-指标管理'], dependencies=[PreAuthDependency()]
)


@index_controller.get(
    '/list',
    summary='获取指标分页列表',
    response_model=PageResponseModel[ItResourceIndexModel],
    dependencies=[UserInterfaceAuthDependency('monitor:index:list')],
)
async def get_index_list(
    request: Request,
    query: Annotated[ItResourceIndexPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorIndexService.get_list_services(query_db, query, is_page=True)
    logger.info('获取指标列表成功')
    return ResponseUtil.success(model_content=result)


@index_controller.get(
    '/{idx_id}',
    summary='获取指标详情',
    response_model=DataResponseModel[ItResourceIndexModel],
)
async def get_index_detail(
    request: Request,
    idx_id: Annotated[str, Path(description='指标ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorIndexService.get_detail_services(query_db, idx_id)
    return ResponseUtil.success(data=result)


@index_controller.post(
    '',
    summary='新增指标',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:index:add')],
)
async def add_index(
    request: Request,
    model: ItResourceIndexModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorIndexService.add_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@index_controller.put(
    '',
    summary='修改指标',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:index:edit')],
)
async def edit_index(
    request: Request,
    model: ItResourceIndexModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorIndexService.edit_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@index_controller.delete(
    '/{ids}',
    summary='删除指标',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:index:remove')],
)
async def delete_index(
    request: Request,
    ids: Annotated[str, Path(description='逗号分隔的指标ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorIndexService.delete_services(query_db, ids)
    return ResponseUtil.success(msg=result.message)


# ============ 资源/设备管理 ============
resource_controller = APIRouterPro(
    prefix='/monitor/resource', order_num=21, tags=['监控管理-资源设备管理'], dependencies=[PreAuthDependency()]
)


@resource_controller.get(
    '/list',
    summary='获取资源分页列表',
    response_model=PageResponseModel[ItResourceListModel],
    dependencies=[UserInterfaceAuthDependency('monitor:resource:list')],
)
async def get_resource_list(
    request: Request,
    query: Annotated[ItResourceListPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorResourceService.get_list_services(query_db, query, is_page=True)
    logger.info('获取资源列表成功')
    return ResponseUtil.success(model_content=result)


@resource_controller.get(
    '/{res_id}',
    summary='获取资源详情',
    response_model=DataResponseModel[ItResourceListModel],
)
async def get_resource_detail(
    request: Request,
    res_id: Annotated[str, Path(description='资源ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorResourceService.get_detail_services(query_db, res_id)
    return ResponseUtil.success(data=result)


@resource_controller.post(
    '',
    summary='新增资源',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:resource:add')],
)
async def add_resource(
    request: Request,
    model: ItResourceListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorResourceService.add_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@resource_controller.put(
    '',
    summary='修改资源',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:resource:edit')],
)
async def edit_resource(
    request: Request,
    model: ItResourceListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorResourceService.edit_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@resource_controller.delete(
    '/{ids}',
    summary='删除资源',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:resource:remove')],
)
async def delete_resource(
    request: Request,
    ids: Annotated[str, Path(description='逗号分隔的资源ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorResourceService.delete_services(query_db, ids)
    return ResponseUtil.success(msg=result.message)


# ============ 子资源类型管理 ============
scan_controller = APIRouterPro(
    prefix='/monitor/scan', order_num=22, tags=['监控管理-子资源类型'], dependencies=[PreAuthDependency()]
)


@scan_controller.get(
    '/list',
    summary='获取子资源类型分页列表',
    response_model=PageResponseModel[ItResourceScanModel],
    dependencies=[UserInterfaceAuthDependency('monitor:scan:list')],
)
async def get_scan_list(
    request: Request,
    query: Annotated[ItResourceScanPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScanService.get_list_services(query_db, query, is_page=True)
    return ResponseUtil.success(model_content=result)


@scan_controller.get(
    '/{scan_id}',
    summary='获取子资源类型详情',
    response_model=DataResponseModel[ItResourceScanModel],
)
async def get_scan_detail(
    request: Request,
    scan_id: Annotated[str, Path(description='子资源类型ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScanService.get_detail_services(query_db, scan_id)
    return ResponseUtil.success(data=result)


@scan_controller.post(
    '',
    summary='新增子资源类型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scan:add')],
)
async def add_scan(
    request: Request,
    model: ItResourceScanModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScanService.add_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@scan_controller.put(
    '',
    summary='修改子资源类型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scan:edit')],
)
async def edit_scan(
    request: Request,
    model: ItResourceScanModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScanService.edit_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@scan_controller.delete(
    '/{ids}',
    summary='删除子资源类型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scan:remove')],
)
async def delete_scan(
    request: Request,
    ids: Annotated[str, Path(description='逗号分隔的ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScanService.delete_services(query_db, ids)
    return ResponseUtil.success(msg=result.message)


# ============ 子资源实例管理 ============
scaning_controller = APIRouterPro(
    prefix='/monitor/scaning', order_num=23, tags=['监控管理-子资源实例'], dependencies=[PreAuthDependency()]
)


@scaning_controller.get(
    '/list',
    summary='获取子资源实例分页列表',
    response_model=PageResponseModel[ItResourceScaningModel],
    dependencies=[UserInterfaceAuthDependency('monitor:scaning:list')],
)
async def get_scaning_list(
    request: Request,
    query: Annotated[ItResourceScaningPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScaningService.get_list_services(query_db, query, is_page=True)
    return ResponseUtil.success(model_content=result)


@scaning_controller.get(
    '/{scaning_id}',
    summary='获取子资源实例详情',
    response_model=DataResponseModel[ItResourceScaningModel],
)
async def get_scaning_detail(
    request: Request,
    scaning_id: Annotated[str, Path(description='子资源实例ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScaningService.get_detail_services(query_db, scaning_id)
    return ResponseUtil.success(data=result)


@scaning_controller.post(
    '',
    summary='新增子资源实例',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scaning:add')],
)
async def add_scaning(
    request: Request,
    model: ItResourceScaningModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScaningService.add_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@scaning_controller.put(
    '',
    summary='修改子资源实例',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scaning:edit')],
)
async def edit_scaning(
    request: Request,
    model: ItResourceScaningModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScaningService.edit_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@scaning_controller.delete(
    '/{ids}',
    summary='删除子资源实例',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:scaning:remove')],
)
async def delete_scaning(
    request: Request,
    ids: Annotated[str, Path(description='逗号分隔的ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorScaningService.delete_services(query_db, ids)
    return ResponseUtil.success(msg=result.message)


# ============ 最新取值管理 ============
value_controller = APIRouterPro(
    prefix='/monitor/value', order_num=24, tags=['监控管理-最新取值'], dependencies=[PreAuthDependency()]
)


@value_controller.get(
    '/list',
    summary='获取最新取值分页列表',
    response_model=PageResponseModel[ItValueListModel],
    dependencies=[UserInterfaceAuthDependency('monitor:value:list')],
)
async def get_value_list(
    request: Request,
    query: Annotated[ItValueListPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorValueService.get_list_services(query_db, query, is_page=True)
    return ResponseUtil.success(model_content=result)


@value_controller.get(
    '/{val_id}',
    summary='获取最新取值详情',
    response_model=DataResponseModel[ItValueListModel],
)
async def get_value_detail(
    request: Request,
    val_id: Annotated[str, Path(description='取值ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorValueService.get_detail_services(query_db, val_id)
    return ResponseUtil.success(data=result)


@value_controller.post(
    '',
    summary='新增取值',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:value:add')],
)
async def add_value(
    request: Request,
    model: ItValueListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorValueService.add_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@value_controller.put(
    '',
    summary='修改取值',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:value:edit')],
)
async def edit_value(
    request: Request,
    model: ItValueListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorValueService.edit_services(query_db, model)
    return ResponseUtil.success(msg=result.message)


@value_controller.delete(
    '/{ids}',
    summary='删除取值',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('monitor:value:remove')],
)
async def delete_value(
    request: Request,
    ids: Annotated[str, Path(description='逗号分隔的ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await MonitorValueService.delete_services(query_db, ids)
    return ResponseUtil.success(msg=result.message)
