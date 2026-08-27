"""监控模块 Pydantic VO 模型"""
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ItResourceIndexModel(BaseModel):
    """指标表 VO"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None, description='id')
    index_sort: int | None = Field(default=None, description='序号')
    index_name: str | None = Field(default=None, description='名称')
    index_class: str | None = Field(default=None, description='指标种类')
    index_type: str | None = Field(default=None, description='指标类型')
    index_ompany: str | None = Field(default=None, description='指标单位')
    index_script: str | None = Field(default=None, description='取值脚本')
    index_special: str | None = Field(default=None, description='特殊取值')
    create_time: int | None = Field(default=None, description='创建时间')
    update_time: int | None = Field(default=None, description='修改时间')
    delete_time: int | None = Field(default=None, description='删除时间')


class ItResourceIndexPageQueryModel(ItResourceIndexModel):
    """指标分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class ItResourceListModel(BaseModel):
    """资源列表 VO"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None, description='id')
    resource_sort: int | None = Field(default=None, description='序号')
    resource_name: str | None = Field(default=None, description='名称')
    resource_ip: str | None = Field(default=None, description='管理ip')
    resource_community: str | None = Field(default=None, description='共同体名')
    resource_manage: str | None = Field(default=None, description='管理状态')
    resource_crux: str | None = Field(default=None, description='关键状态')
    resource_type: str | None = Field(default=None, description='资源类型')
    resource_region: str | None = Field(default=None, description='资源地域')
    resource_manufacturer: str | None = Field(default=None, description='取值脚本')
    resource_modelnumber: str | None = Field(default=None, description='扫描脚本')
    resource_lable: str | None = Field(default=None)
    resource_location: str | None = Field(default=None)
    resource_person: str | None = Field(default=None)
    resource_telephone: str | None = Field(default=None)
    resource_gather: str | None = Field(default=None, description='指标集合')
    resource_model: str | None = Field(default=None, description='扫描集合')
    resource_index: str | None = Field(default=None, description='取值脚本')
    resource_scan: str | None = Field(default=None, description='扫描脚本')
    resource_collector: str | None = Field(default=None, description='采集节点')
    resource_time: float | None = Field(default=None)
    resource_health: float | None = Field(default=None)
    resource_usable: float | None = Field(default=None)
    resource_system_ip: str | None = Field(default=None, description='系统ip')
    resource_system_mac: str | None = Field(default=None, description='系统mac')
    resource_system_name: str | None = Field(default=None, description='系统名称')
    resource_system_oid: str | None = Field(default=None, description='系统oid')
    resource_system_describe: str | None = Field(default=None, description='系统描述')
    resource_revise: str | None = Field(default=None, description='修改时间')
    create_time: int | None = Field(default=None, description='创建时间')
    update_time: int | None = Field(default=None, description='修改时间')
    delete_time: int | None = Field(default=None, description='删除时间')


class ItResourceListPageQueryModel(ItResourceListModel):
    """资源分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class ItResourceScanModel(BaseModel):
    """子资源类型 VO"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None, description='id')
    scan_sort: int | None = Field(default=None, description='序号')
    scan_name: str | None = Field(default=None, description='名称')
    scan_gather: str | None = Field(default=None, description='指标集合')
    scan_index: str | None = Field(default=None)
    scan_script: str | None = Field(default=None, description='扫描脚本')
    name_script: str | None = Field(default=None, description='名称脚本')
    scan_special: str | None = Field(default=None)
    create_time: int | None = Field(default=None, description='创建时间')
    update_time: int | None = Field(default=None, description='修改时间')
    delete_time: int | None = Field(default=None, description='删除时间')


class ItResourceScanPageQueryModel(ItResourceScanModel):
    """子资源类型分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class ItResourceScaningModel(BaseModel):
    """子资源 VO"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None)
    scaning_sort: int | None = Field(default=None)
    scaning_name: str | None = Field(default=None)
    scaning_resource: str | None = Field(default=None, description='所属资源id')
    scaning_key: str | None = Field(default=None)
    scaning_manage: str | None = Field(default=None)
    scaning_crux: str | None = Field(default=None)
    scaning_type: str | None = Field(default=None)
    scaning_region: str | None = Field(default=None)
    scaning_gather: str | None = Field(default=None)
    scaning_index: str | None = Field(default=None, description='监控指标')
    scaning_lock: str | None = Field(default=None)
    scaning_revise: str | None = Field(default=None)
    create_time: int | None = Field(default=None, description='创建时间')
    update_time: int | None = Field(default=None, description='修改时间')
    delete_time: int | None = Field(default=None, description='删除时间')


class ItResourceScaningPageQueryModel(ItResourceScaningModel):
    """子资源分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class ItValueListModel(BaseModel):
    """最新取值结果 VO"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: str | None = Field(default=None)
    value_time: str | None = Field(default=None)
    resource_id: str | None = Field(default=None, description='资源id')
    scaning_id: str | None = Field(default=None, description='子资源id')
    index_id: str | None = Field(default=None, description='指标id')
    value_word: str | None = Field(default=None, description='取值结果')
    create_time: int | None = Field(default=None, description='创建时间')
    update_time: int | None = Field(default=None, description='修改时间')
    delete_time: int | None = Field(default=None, description='删除时间')


class ItValueListPageQueryModel(ItValueListModel):
    """取值结果分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteMonitorModel(BaseModel):
    """删除监控记录模型 (逗号分隔 id)"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    ids: str = Field(description='需要删除的id列表(逗号分隔)')
