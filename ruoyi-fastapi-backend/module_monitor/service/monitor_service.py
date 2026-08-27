"""监控模块 Service 层"""
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from module_monitor.dao.monitor_dao import (
    MonitorHistoryDao,
    MonitorIndexDao,
    MonitorResourceDao,
    MonitorScanDao,
    MonitorScaningDao,
    MonitorValueDao,
)
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


def _split_ids(ids_str: str) -> list[str]:
    if not ids_str:
        return []
    return [x.strip() for x in ids_str.split(',') if x.strip()]


# ----------------- 指标 -----------------
class MonitorIndexService:
    @classmethod
    async def get_list_services(
        cls, db: AsyncSession, query_object: ItResourceIndexPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await MonitorIndexDao.get_list(db, query_object, is_page)

    @classmethod
    async def get_detail_services(cls, db: AsyncSession, pk: str) -> ItResourceIndexModel | None:
        obj = await MonitorIndexDao.get_detail(db, pk)
        return ItResourceIndexModel.model_validate(obj) if obj else None

    @classmethod
    async def add_services(cls, db: AsyncSession, model: ItResourceIndexModel) -> CrudResponseModel:
        await MonitorIndexDao.add(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增指标成功')

    @classmethod
    async def edit_services(cls, db: AsyncSession, model: ItResourceIndexModel) -> CrudResponseModel:
        await MonitorIndexDao.edit(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='更新指标成功')

    @classmethod
    async def delete_services(cls, db: AsyncSession, ids: str) -> CrudResponseModel:
        await MonitorIndexDao.delete(db, _split_ids(ids))
        await db.commit()
        return CrudResponseModel(is_success=True, message='删除指标成功')


# ----------------- 资源/设备 -----------------
class MonitorResourceService:
    @classmethod
    async def get_list_services(
        cls, db: AsyncSession, query_object: ItResourceListPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await MonitorResourceDao.get_list(db, query_object, is_page)

    @classmethod
    async def get_detail_services(cls, db: AsyncSession, pk: str) -> ItResourceListModel | None:
        obj = await MonitorResourceDao.get_detail(db, pk)
        return ItResourceListModel.model_validate(obj) if obj else None

    @classmethod
    async def add_services(cls, db: AsyncSession, model: ItResourceListModel) -> CrudResponseModel:
        await MonitorResourceDao.add(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增资源成功')

    @classmethod
    async def edit_services(cls, db: AsyncSession, model: ItResourceListModel) -> CrudResponseModel:
        await MonitorResourceDao.edit(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='更新资源成功')

    @classmethod
    async def delete_services(cls, db: AsyncSession, ids: str) -> CrudResponseModel:
        await MonitorResourceDao.delete(db, _split_ids(ids))
        await db.commit()
        return CrudResponseModel(is_success=True, message='删除资源成功')


# ----------------- 子资源类型 -----------------
class MonitorScanService:
    @classmethod
    async def get_list_services(
        cls, db: AsyncSession, query_object: ItResourceScanPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await MonitorScanDao.get_list(db, query_object, is_page)

    @classmethod
    async def get_detail_services(cls, db: AsyncSession, pk: str) -> ItResourceScanModel | None:
        obj = await MonitorScanDao.get_detail(db, pk)
        return ItResourceScanModel.model_validate(obj) if obj else None

    @classmethod
    async def add_services(cls, db: AsyncSession, model: ItResourceScanModel) -> CrudResponseModel:
        await MonitorScanDao.add(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增子资源类型成功')

    @classmethod
    async def edit_services(cls, db: AsyncSession, model: ItResourceScanModel) -> CrudResponseModel:
        await MonitorScanDao.edit(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='更新子资源类型成功')

    @classmethod
    async def delete_services(cls, db: AsyncSession, ids: str) -> CrudResponseModel:
        await MonitorScanDao.delete(db, _split_ids(ids))
        await db.commit()
        return CrudResponseModel(is_success=True, message='删除子资源类型成功')


# ----------------- 子资源实例 -----------------
class MonitorScaningService:
    @classmethod
    async def get_list_services(
        cls, db: AsyncSession, query_object: ItResourceScaningPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await MonitorScaningDao.get_list(db, query_object, is_page)

    @classmethod
    async def get_detail_services(cls, db: AsyncSession, pk: str) -> ItResourceScaningModel | None:
        obj = await MonitorScaningDao.get_detail(db, pk)
        return ItResourceScaningModel.model_validate(obj) if obj else None

    @classmethod
    async def add_services(cls, db: AsyncSession, model: ItResourceScaningModel) -> CrudResponseModel:
        await MonitorScaningDao.add(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增子资源成功')

    @classmethod
    async def edit_services(cls, db: AsyncSession, model: ItResourceScaningModel) -> CrudResponseModel:
        await MonitorScaningDao.edit(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='更新子资源成功')

    @classmethod
    async def delete_services(cls, db: AsyncSession, ids: str) -> CrudResponseModel:
        await MonitorScaningDao.delete(db, _split_ids(ids))
        await db.commit()
        return CrudResponseModel(is_success=True, message='删除子资源成功')


# ----------------- 最新取值 -----------------
class MonitorValueService:
    @classmethod
    async def get_list_services(
        cls, db: AsyncSession, query_object: ItValueListPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await MonitorValueDao.get_list(db, query_object, is_page)

    @classmethod
    async def get_detail_services(cls, db: AsyncSession, pk: str) -> ItValueListModel | None:
        obj = await MonitorValueDao.get_detail(db, pk)
        return ItValueListModel.model_validate(obj) if obj else None

    @classmethod
    async def add_services(cls, db: AsyncSession, model: ItValueListModel) -> CrudResponseModel:
        await MonitorValueDao.add(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增取值记录成功')

    @classmethod
    async def edit_services(cls, db: AsyncSession, model: ItValueListModel) -> CrudResponseModel:
        await MonitorValueDao.edit(db, model)
        await db.commit()
        return CrudResponseModel(is_success=True, message='更新取值记录成功')

    @classmethod
    async def delete_services(cls, db: AsyncSession, ids: str) -> CrudResponseModel:
        await MonitorValueDao.delete(db, _split_ids(ids))
        await db.commit()
        return CrudResponseModel(is_success=True, message='删除取值记录成功')


# ----------------- 看板统计 (对应 3 个测试问题) -----------------
class MonitorDashboardService:
    @classmethod
    async def get_device_count(cls, db: AsyncSession) -> int:
        """Q1: 监控了多少台设备"""
        from sqlalchemy import func, select

        from module_monitor.entity.do.monitor_do import ItResourceList

        return int(
            (
                await db.execute(
                    select(func.count(ItResourceList.id)).where(ItResourceList.delete_time.is_(None))
                )
            ).scalar_one()
        )

    @classmethod
    async def get_top_cpu_devices(cls, db: AsyncSession, limit: int = 10) -> list[dict[str, Any]]:
        """Q2: 当前平均 CPU 利用率最高的 N 台设备"""
        return await MonitorHistoryDao.get_top_cpu_devices(db, limit=limit)

    @classmethod
    async def get_recent_ping_by_ip(
        cls, db: AsyncSession, ip: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Q3: 某资源最近 N 次 ping 响应时间"""
        # 先从 it_resource_list 找到 resource_id
        resource = await MonitorResourceDao.get_by_ip(db, ip)
        if not resource:
            return []
        # 找到 "Ping响应时间" 指标 id
        from sqlalchemy import select

        from module_monitor.entity.do.monitor_do import ItResourceIndex

        idx = (
            await db.execute(
                select(ItResourceIndex.id).where(ItResourceIndex.index_name == 'Ping响应时间')
            )
        ).scalars().first()
        if not idx:
            return []
        return await MonitorHistoryDao.get_recent_values(db, resource.id, idx, limit=limit)
