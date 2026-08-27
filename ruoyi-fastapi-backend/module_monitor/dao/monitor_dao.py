"""监控模块 DAO 层"""
from typing import Any

from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_monitor.entity.do.monitor_do import (
    ItResourceIndex,
    ItResourceList,
    ItResourceScan,
    ItResourceScaning,
    ItValueList,
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
from utils.page_util import PageUtil


# 安全表名校白名单，避免 SQL 注入 (动态历史表查询用)
_ALLOWED_TABLE_PREFIX = 'it_'
_HISTORY_TABLE_RE = r'^it_\d{5,}$'


class MonitorIndexDao:
    """it_resource_index DAO"""

    @classmethod
    async def get_list(
        cls, db: AsyncSession, query_object: ItResourceIndexPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ItResourceIndex)
            .where(
                ItResourceIndex.index_name.like(f'%{query_object.index_name}%')
                if query_object.index_name
                else True,
                ItResourceIndex.index_class == query_object.index_class if query_object.index_class else True,
                ItResourceIndex.delete_time.is_(None),
            )
            .order_by(ItResourceIndex.index_sort.asc())
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_detail(cls, db: AsyncSession, pk: str) -> ItResourceIndex | None:
        return (
            await db.execute(
                select(ItResourceIndex).where(ItResourceIndex.id == pk, ItResourceIndex.delete_time.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def add(cls, db: AsyncSession, model: ItResourceIndexModel) -> ItResourceIndex:
        obj = ItResourceIndex(**model.model_dump(exclude_unset=False))
        db.add(obj)
        await db.flush()
        return obj

    @classmethod
    async def edit(cls, db: AsyncSession, model: ItResourceIndexModel) -> None:
        from sqlalchemy import update

        data = model.model_dump(exclude_unset=True, exclude={'id', 'create_time'})
        await db.execute(update(ItResourceIndex).where(ItResourceIndex.id == model.id).values(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, ids: list[str]) -> None:
        from sqlalchemy import update

        await db.execute(update(ItResourceIndex).where(ItResourceIndex.id.in_(ids)).values(delete_time=0))


class MonitorResourceDao:
    """it_resource_list DAO (设备/资源)"""

    @classmethod
    async def get_list(
        cls, db: AsyncSession, query_object: ItResourceListPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ItResourceList)
            .where(
                ItResourceList.resource_name.like(f'%{query_object.resource_name}%')
                if query_object.resource_name
                else True,
                ItResourceList.resource_ip.like(f'%{query_object.resource_ip}%')
                if query_object.resource_ip
                else True,
                ItResourceList.resource_type == query_object.resource_type if query_object.resource_type else True,
                ItResourceList.delete_time.is_(None),
            )
            .order_by(ItResourceList.resource_sort.asc())
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_detail(cls, db: AsyncSession, pk: str) -> ItResourceList | None:
        return (
            await db.execute(
                select(ItResourceList).where(ItResourceList.id == pk, ItResourceList.delete_time.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def get_by_ip(cls, db: AsyncSession, ip: str) -> ItResourceList | None:
        return (
            await db.execute(
                select(ItResourceList).where(ItResourceList.resource_ip == ip, ItResourceList.delete_time.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def add(cls, db: AsyncSession, model: ItResourceListModel) -> ItResourceList:
        obj = ItResourceList(**model.model_dump(exclude_unset=False))
        db.add(obj)
        await db.flush()
        return obj

    @classmethod
    async def edit(cls, db: AsyncSession, model: ItResourceListModel) -> None:
        from sqlalchemy import update
        data = model.model_dump(exclude_unset=True, exclude={'id', 'create_time'})
        await db.execute(update(ItResourceList).where(ItResourceList.id == model.id).values(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, ids: list[str]) -> None:
        from sqlalchemy import update
        await db.execute(update(ItResourceList).where(ItResourceList.id.in_(ids)).values(delete_time=0))


class MonitorScanDao:
    """it_resource_scan DAO (子资源类型)"""

    @classmethod
    async def get_list(
        cls, db: AsyncSession, query_object: ItResourceScanPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ItResourceScan)
            .where(
                ItResourceScan.scan_name.like(f'%{query_object.scan_name}%')
                if query_object.scan_name
                else True,
                ItResourceScan.delete_time.is_(None),
            )
            .order_by(ItResourceScan.scan_sort.asc())
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_detail(cls, db: AsyncSession, pk: str) -> ItResourceScan | None:
        return (
            await db.execute(
                select(ItResourceScan).where(ItResourceScan.id == pk, ItResourceScan.delete_time.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def add(cls, db: AsyncSession, model: ItResourceScanModel) -> ItResourceScan:
        obj = ItResourceScan(**model.model_dump(exclude_unset=False))
        db.add(obj)
        await db.flush()
        return obj

    @classmethod
    async def edit(cls, db: AsyncSession, model: ItResourceScanModel) -> None:
        from sqlalchemy import update
        data = model.model_dump(exclude_unset=True, exclude={'id', 'create_time'})
        await db.execute(update(ItResourceScan).where(ItResourceScan.id == model.id).values(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, ids: list[str]) -> None:
        from sqlalchemy import update
        await db.execute(update(ItResourceScan).where(ItResourceScan.id.in_(ids)).values(delete_time=0))


class MonitorScaningDao:
    """it_resource_scaning DAO (子资源实例)"""

    @classmethod
    async def get_list(
        cls, db: AsyncSession, query_object: ItResourceScaningPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ItResourceScaning)
            .where(
                ItResourceScaning.scaning_resource == query_object.scaning_resource
                if query_object.scaning_resource
                else True,
                ItResourceScaning.scaning_name.like(f'%{query_object.scaning_name}%')
                if query_object.scaning_name
                else True,
                ItResourceScaning.delete_time.is_(None),
            )
            .order_by(ItResourceScaning.scaning_sort.asc())
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_detail(cls, db: AsyncSession, pk: str) -> ItResourceScaning | None:
        return (
            await db.execute(
                select(ItResourceScaning).where(ItResourceScaning.id == pk, ItResourceScaning.delete_time.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def add(cls, db: AsyncSession, model: ItResourceScaningModel) -> ItResourceScaning:
        obj = ItResourceScaning(**model.model_dump(exclude_unset=False))
        db.add(obj)
        await db.flush()
        return obj

    @classmethod
    async def edit(cls, db: AsyncSession, model: ItResourceScaningModel) -> None:
        from sqlalchemy import update
        data = model.model_dump(exclude_unset=True, exclude={'id', 'create_time'})
        await db.execute(update(ItResourceScaning).where(ItResourceScaning.id == model.id).values(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, ids: list[str]) -> None:
        from sqlalchemy import update
        await db.execute(update(ItResourceScaning).where(ItResourceScaning.id.in_(ids)).values(delete_time=0))


class MonitorValueDao:
    """it_value_list DAO (最新取值)"""

    @classmethod
    async def get_list(
        cls, db: AsyncSession, query_object: ItValueListPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(ItValueList)
            .where(
                ItValueList.resource_id == query_object.resource_id if query_object.resource_id else True,
                ItValueList.index_id == query_object.index_id if query_object.index_id else True,
                ItValueList.delete_time.is_(None),
            )
            .order_by(ItValueList.value_time.desc())
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_detail(cls, db: AsyncSession, pk: str) -> ItValueList | None:
        return (
            await db.execute(select(ItValueList).where(ItValueList.id == pk))
        ).scalars().first()

    @classmethod
    async def add(cls, db: AsyncSession, model: ItValueListModel) -> ItValueList:
        obj = ItValueList(**model.model_dump(exclude_unset=False))
        db.add(obj)
        await db.flush()
        return obj

    @classmethod
    async def edit(cls, db: AsyncSession, model: ItValueListModel) -> None:
        from sqlalchemy import update
        data = model.model_dump(exclude_unset=True, exclude={'id', 'create_time'})
        await db.execute(update(ItValueList).where(ItValueList.id == model.id).values(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, ids: list[str]) -> None:
        from sqlalchemy import update
        await db.execute(update(ItValueList).where(ItValueList.id.in_(ids)).values(delete_time=0))


class MonitorHistoryDao:
    """动态历史表 DAO - 用于查询 it_<resource_id> 历史指标数据表"""

    @staticmethod
    def _validate_table_name(table_name: str) -> None:
        """校验动态表名格式，避免 SQL 注入"""
        import re

        if not re.match(_HISTORY_TABLE_RE, table_name):
            raise ValueError(f'非法的历史表名: {table_name}')

    @classmethod
    async def get_recent_values(
        cls,
        db: AsyncSession,
        resource_id: str,
        index_id: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """查询某资源某指标的最近 N 次历史取值 (用于 Q3)

        :param db: orm
        :param resource_id: 资源id (对应历史表名后缀)
        :param index_id: 指标id
        :param limit: 返回条数
        :return: list[{id, scaning_id, index_id, index_value, scan_time}]
        """
        table_name = f'it_{resource_id}'
        cls._validate_table_name(table_name)
        # id = 时间戳+9位纳秒，去掉后9位即得秒级时间戳
        sql = text(
            f'SELECT id, scaning_id, index_id, index_value, '
            f"DATE_FORMAT(FROM_UNIXTIME(CEIL(id / 1000000000)), '%Y-%m-%d %H:%i:%s') AS scan_time "
            f'FROM `{table_name}` '
            f'WHERE index_id = :index_id AND scaning_id = 1 '
            f'ORDER BY id DESC LIMIT :limit'
        )
        result = await db.execute(sql, {'index_id': index_id, 'limit': limit})
        return [dict(row._mapping) for row in result.all()]

    @classmethod
    async def get_top_cpu_devices(
        cls,
        db: AsyncSession,
        cpu_index_name: str = '平均CPU利用率',
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """查询当前平均 CPU 利用率最高的 N 台设备 (用于 Q2)

        通过 it_value_list 关联 it_resource_index 找到 CPU 指标, 然后按 value_word 数值降序.
        """
        sql = text(
            'SELECT v.resource_id, r.resource_name, r.resource_ip, v.value_word '
            'FROM it_value_list v '
            'JOIN it_resource_index i ON v.index_id = i.id '
            'LEFT JOIN it_resource_list r ON v.resource_id = r.id '
            f'WHERE i.index_name = :cpu_name AND v.scaning_id = 1 '
            "AND v.value_word REGEXP '^[0-9]+(\\\\.[0-9]+)?$' "
            'ORDER BY CAST(v.value_word AS DECIMAL(10,2)) DESC '
            'LIMIT :limit'
        )
        result = await db.execute(sql, {'cpu_name': cpu_index_name, 'limit': limit})
        return [dict(row._mapping) for row in result.all()]
