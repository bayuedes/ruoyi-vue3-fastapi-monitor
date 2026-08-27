"""监控资源相关表 ORM 模型

对应数据库中的 5 个不带数字的监控表:
- it_resource_index   指标表
- it_resource_list    资源(设备)列表
- it_resource_scan    子资源类型表(磁盘/接口等)
- it_resource_scaning 资源的子资源表(具体磁盘/接口)
- it_value_list       最新取值结果表
"""
from sqlalchemy import BigInteger, Column, Float, String, Text

from config.database import Base


class ItResourceIndex(Base):
    """指标脚本表 (it_resource_index)"""

    __tablename__ = 'it_resource_index'
    __table_args__ = {'comment': '指标脚本'}

    id = Column(String(250), primary_key=True, nullable=False, comment='id')
    index_sort = Column(BigInteger, nullable=True, comment='序号')
    index_name = Column(Text, nullable=True, comment='名称')
    index_class = Column(Text, nullable=True, comment='指标种类')
    index_type = Column(Text, nullable=True, comment='指标类型')
    index_ompany = Column(Text, nullable=True, comment='指标单位')
    index_script = Column(Text, nullable=True, comment='取值脚本')
    index_special = Column(Text, nullable=True, comment='特殊取值')
    create_time = Column(BigInteger, nullable=True, comment='创建时间')
    update_time = Column(BigInteger, nullable=True, comment='修改时间')
    delete_time = Column(BigInteger, nullable=True, comment='删除时间')


class ItResourceList(Base):
    """资源列表表 (it_resource_list)"""

    __tablename__ = 'it_resource_list'
    __table_args__ = {'comment': '资源列表'}

    id = Column(String(250), primary_key=True, nullable=False, comment='id')
    resource_sort = Column(BigInteger, nullable=True, comment='序号')
    resource_name = Column(Text, nullable=True, comment='名称')
    resource_ip = Column(String(999), nullable=True, comment='管理ip')
    resource_community = Column(Text, nullable=True, comment='共同体名')
    resource_manage = Column(Text, nullable=True, comment='管理状态')
    resource_crux = Column(Text, nullable=True, comment='关键状态')
    resource_type = Column(Text, nullable=True, comment='资源类型')
    resource_region = Column(Text, nullable=True, comment='资源地域')
    resource_manufacturer = Column(Text, nullable=True, comment='取值脚本')
    resource_modelnumber = Column(Text, nullable=True, comment='扫描脚本')
    resource_lable = Column(Text, nullable=True)
    resource_location = Column(Text, nullable=True)
    resource_person = Column(Text, nullable=True)
    resource_telephone = Column(Text, nullable=True)
    resource_gather = Column(Text, nullable=True, comment='指标集合')
    resource_model = Column(Text, nullable=True, comment='扫描集合')
    resource_index = Column(Text, nullable=True, comment='取值脚本')
    resource_scan = Column(Text, nullable=True, comment='扫描脚本')
    resource_collector = Column(Text, nullable=True, comment='采集节点')
    resource_time = Column(Float, nullable=True)
    resource_health = Column(Float, nullable=True)
    resource_usable = Column(Float, nullable=True)
    resource_system_ip = Column(Text, nullable=True, comment='系统ip')
    resource_system_mac = Column(Text, nullable=True, comment='系统mac')
    resource_system_name = Column(Text, nullable=True, comment='系统名称')
    resource_system_oid = Column(Text, nullable=True, comment='系统oid')
    resource_system_describe = Column(Text, nullable=True, comment='系统描述')
    resource_revise = Column(Text, nullable=True, comment='修改时间')
    create_time = Column(BigInteger, nullable=True, comment='创建时间')
    update_time = Column(BigInteger, nullable=True, comment='修改时间')
    delete_time = Column(BigInteger, nullable=True, comment='删除时间')


class ItResourceScan(Base):
    """扫描脚本表 (it_resource_scan) - 子资源类型"""

    __tablename__ = 'it_resource_scan'
    __table_args__ = {'comment': '扫描脚本'}

    id = Column(String(250), primary_key=True, nullable=False, comment='id')
    scan_sort = Column(BigInteger, nullable=True, comment='序号')
    scan_name = Column(Text, nullable=True, comment='名称')
    scan_gather = Column(Text, nullable=True, comment='指标集合')
    scan_index = Column(Text, nullable=True)
    scan_script = Column(Text, nullable=True, comment='扫描脚本')
    name_script = Column(Text, nullable=True, comment='名称脚本')
    scan_special = Column(Text, nullable=True)
    create_time = Column(BigInteger, nullable=True, comment='创建时间')
    update_time = Column(BigInteger, nullable=True, comment='修改时间')
    delete_time = Column(BigInteger, nullable=True, comment='删除时间')


class ItResourceScaning(Base):
    """资源的子资源表 (it_resource_scaning) - 具体的磁盘/接口等"""

    __tablename__ = 'it_resource_scaning'
    __table_args__ = (
        {'comment': '资源的子资源表'},
    )

    id = Column(String(250), primary_key=True, nullable=False)
    scaning_sort = Column(BigInteger, nullable=True)
    scaning_name = Column(Text, nullable=True)
    scaning_resource = Column(String(250), nullable=True, comment='所属资源id')
    scaning_key = Column(String(250), nullable=True)
    scaning_manage = Column(Text, nullable=True)
    scaning_crux = Column(Text, nullable=True)
    scaning_type = Column(String(250), nullable=True)
    scaning_region = Column(Text, nullable=True)
    scaning_gather = Column(Text, nullable=True)
    scaning_index = Column(Text, nullable=True, comment='监控指标')
    scaning_lock = Column(Text, nullable=True)
    scaning_revise = Column(Text, nullable=True)
    create_time = Column(BigInteger, nullable=True, comment='创建时间')
    update_time = Column(BigInteger, nullable=True, comment='修改时间')
    delete_time = Column(BigInteger, nullable=True, comment='删除时间')


class ItValueList(Base):
    """最新取值结果表 (it_value_list)"""

    __tablename__ = 'it_value_list'
    __table_args__ = (
        {'comment': '资源最新取值结果'},
    )

    id = Column(String(250), primary_key=True, nullable=False)
    value_time = Column(Text, nullable=True)
    resource_id = Column(String(250), nullable=True, comment='资源id')
    scaning_id = Column(String(250), nullable=True, comment='子资源id')
    index_id = Column(String(250), nullable=True, comment='指标id')
    value_word = Column(Text, nullable=True, comment='取值结果')
    create_time = Column(BigInteger, nullable=True, comment='创建时间')
    update_time = Column(BigInteger, nullable=True, comment='修改时间')
    delete_time = Column(BigInteger, nullable=True, comment='删除时间')
