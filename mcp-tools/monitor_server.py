"""
MCP 服务器: IT 监控资源查询工具集
对接 ruoyi-fastapi 后端 MySQL 数据库 (it_resource_list / it_resource_index / it_value_list / it_<resource_id> 历史表)

工具:
  1. get_monitored_device_count      - 查询监控设备总数 (Q1)
  2. get_top_cpu_devices             - 查询当前平均 CPU 利用率最高的 N 台设备 (Q2)
  3. get_recent_ping_times           - 查询指定 IP 资源最近 N 次 Ping 响应时间 (Q3)
  4. list_resources                  - 分页列出监控资源(支持按 IP/名称模糊查询)
  5. describe_monitor_schema          - 描述监控相关表的字段含义, 帮助 LLM 理解数据结构

启动:
  stdio: fastmcp run knowledge_base_system/FastMCP/monitor_server.py
  SSE:   fastmcp run knowledge_base_system/FastMCP/monitor_server.py --transport sse --port 8092 --host 0.0.0.0
"""
import os
import time
from typing import Optional

import pymysql
from fastmcp import FastMCP

MYSQL_HOST = os.getenv("MONITOR_MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MONITOR_MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MONITOR_MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MONITOR_MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MONITOR_MYSQL_DATABASE", "ruoyi-fastapi")
MYSQL_CHARSET = os.getenv("MONITOR_MYSQL_CHARSET", "utf8mb4")

_conn = None
_conn_time = 0


def _get_conn():
    """获取 MySQL 连接, 5 分钟内复用"""
    global _conn, _conn_time
    if _conn is not None and (time.time() - _conn_time) < 300:
        try:
            _conn.ping(reconnect=True)
            return _conn
        except Exception:
            _conn = None
    _conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset=MYSQL_CHARSET,
        cursorclass=pymysql.cursors.DictCursor,
    )
    _conn_time = time.time()
    return _conn


def _query(sql: str, args: tuple = (), one: bool = False):
    """执行 SQL 查询, 返回 dict 列表"""
    conn = _get_conn()
    with conn.cursor() as cur:
        cur.execute(sql, args)
        rows = cur.fetchall()
    if one:
        return rows[0] if rows else None
    return list(rows)


# 创建 FastMCP 应用
mcp = FastMCP("ITMonitorServer")


@mcp.tool()
def get_monitored_device_count() -> dict:
    """
    查询当前监控的设备总数。

    对应测试问题 Q1: 监控了多少台设备?
    数据来源: it_resource_list 表 (delete_time IS NULL 视为有效设备)
    返回: {"device_count": int, "description": str}
    """
    row = _query(
        "SELECT COUNT(*) AS cnt FROM it_resource_list WHERE delete_time IS NULL",
        one=True,
    )
    cnt = int(row["cnt"]) if row else 0
    return {
        "device_count": cnt,
        "description": f"当前共监控 {cnt} 台设备 (it_resource_list 表中 delete_time 为空的记录数)",
    }


@mcp.tool()
def get_top_cpu_devices(limit: int = 10) -> dict:
    """
    查询当前平均 CPU 利用率最高的 N 台设备。

    对应测试问题 Q2: 当前平均 CPU 利用率最高的 10 台设备是哪些?
    数据来源:
      - it_value_list v: 最新取值结果
      - it_resource_index i: 指标定义 (index_name='平均CPU利用率')
      - it_resource_list r: 资源信息
    仅取 scaning_id=1 (资源本身的 CPU, 不含子资源如单核) 且 value_word 是数字的记录
    返回: {"limit": int, "data": [{resource_id, resource_name, resource_ip, cpu_usage}], "description": str}
    """
    if limit < 1 or limit > 100:
        limit = 10
    rows = _query(
        """
        SELECT v.resource_id, r.resource_name, r.resource_ip, v.value_word AS cpu_usage
        FROM it_value_list v
        JOIN it_resource_index i ON v.index_id = i.id
        LEFT JOIN it_resource_list r ON v.resource_id = r.id
        WHERE i.index_name = %s
          AND v.scaning_id = 1
          AND v.value_word REGEXP '^[0-9]+(\\\\.[0-9]+)?$'
        ORDER BY CAST(v.value_word AS DECIMAL(10,2)) DESC
        LIMIT %s
        """,
        ("平均CPU利用率", limit),
    )
    data = [
        {
            "rank": idx + 1,
            "resource_id": r.get("resource_id"),
            "resource_name": r.get("resource_name"),
            "resource_ip": r.get("resource_ip"),
            "cpu_usage": r.get("cpu_usage"),
        }
        for idx, r in enumerate(rows)
    ]
    return {
        "limit": limit,
        "data": data,
        "description": f"当前平均 CPU 利用率最高的 {len(data)} 台设备 (按 value_word 数值降序)",
    }


@mcp.tool()
def get_recent_ping_times(ip: str, limit: int = 10) -> dict:
    """
    查询指定 IP 资源最近的 N 次 Ping 响应时间。

    对应测试问题 Q3: 192.168.145.253 这个资源的最近的十次 ping 响应时间是多少?
    流程:
      1. 通过 it_resource_list.resource_ip = ip 找到 resource_id
      2. 在 it_resource_index 中找到 index_name='Ping响应时间' 的 index_id
      3. 查询历史表 it_<resource_id>, 取 scaning_id=1 (资源本身) 按 id 倒序取 N 条
    id 字段=时间戳(秒) + 9 位纳秒, 可用 FROM_UNIXTIME(CEIL(id/1e9)) 还原取值时间
    返回: {"ip": str, "limit": int, "data": [{seq, ping_ms, scan_time}], "description": str}
    """
    if limit < 1 or limit > 100:
        limit = 10

    # 1. 查 resource_id
    res = _query(
        "SELECT id, resource_name FROM it_resource_list WHERE resource_ip = %s AND delete_time IS NULL LIMIT 1",
        (ip,),
        one=True,
    )
    if not res:
        return {
            "ip": ip,
            "limit": limit,
            "data": [],
            "description": f"未找到 IP 为 {ip} 的资源",
        }
    resource_id = res["id"]
    resource_name = res.get("resource_name")

    # 2. 查 Ping 响应时间 指标 id
    idx = _query(
        "SELECT id FROM it_resource_index WHERE index_name = %s LIMIT 1",
        ("Ping响应时间",),
        one=True,
    )
    if not idx:
        return {
            "ip": ip,
            "resource_id": resource_id,
            "limit": limit,
            "data": [],
            "description": "it_resource_index 中未找到 'Ping响应时间' 指标",
        }
    index_id = idx["id"]

    # 3. 历史表名 (it_<resource_id>), 必须为 it_+纯数字, 避免注入
    table = f"it_{resource_id}"
    if not table.startswith("it_") or not table[3:].isdigit():
        return {"ip": ip, "limit": limit, "data": [], "description": f"非法历史表名: {table}"}

    rows = _query(
        f"""
        SELECT id, scaning_id, index_id, index_value,
               DATE_FORMAT(FROM_UNIXTIME(CEIL(id / 1000000000)), '%%Y-%%m-%%d %%H:%%i:%%s') AS scan_time
        FROM `{table}`
        WHERE index_id = %s AND scaning_id = 1
        ORDER BY id DESC
        LIMIT %s
        """,
        (index_id, limit),
    )
    data = [
        {
            "seq": i + 1,
            "ping_ms": r.get("index_value"),
            "scan_time": r.get("scan_time"),
            "raw_id": str(r.get("id")),
        }
        for i, r in enumerate(rows)
    ]
    return {
        "ip": ip,
        "resource_id": resource_id,
        "resource_name": resource_name,
        "limit": limit,
        "data": data,
        "description": f"{ip} ({resource_name}) 最近 {len(data)} 次 Ping 响应时间 (单位 ms, 时间倒序)",
    }


@mcp.tool()
def list_resources(
    page_num: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None,
) -> dict:
    """
    分页列出监控设备/资源 (it_resource_list 表)。

    :param page_num: 页码 (1 开始)
    :param page_size: 每页条数 (1-100)
    :param keyword: 关键字 (按 resource_name 或 resource_ip 模糊匹配)
    返回: {"page_num, page_size, total, data": [{id, resource_name, resource_ip, resource_type, resource_manage, resource_crux, resource_health, resource_usable}], "description": str}
    """
    page_num = max(1, page_num)
    page_size = max(1, min(100, page_size))
    offset = (page_num - 1) * page_size
    where = "WHERE delete_time IS NULL"
    args = []
    if keyword:
        where += " AND (resource_name LIKE %s OR resource_ip LIKE %s)"
        args.extend([f"%{keyword}%", f"%{keyword}%"])

    total_row = _query(f"SELECT COUNT(*) AS cnt FROM it_resource_list {where}", tuple(args), one=True)
    total = int(total_row["cnt"]) if total_row else 0

    rows = _query(
        f"""
        SELECT id, resource_name, resource_ip, resource_type, resource_manage, resource_crux,
               resource_health, resource_usable, resource_system_name
        FROM it_resource_list {where}
        ORDER BY resource_sort ASC
        LIMIT %s OFFSET %s
        """,
        tuple(args) + (page_size, offset),
    )
    return {
        "page_num": page_num,
        "page_size": page_size,
        "total": total,
        "data": list(rows),
        "description": f"监控资源第 {page_num} 页, 共 {total} 条 (每页 {page_size})",
    }


@mcp.tool()
def describe_monitor_schema() -> dict:
    """
    描述 IT 监控相关表结构与字段含义, 便于 LLM 决策应调用哪个工具。

    数据说明:
      - it_resource_index   : 指标定义表 (id, index_name, index_class, index_type, index_ompany 单位)
      - it_resource_list    : 资源/设备列表 (id, resource_name 名称, resource_ip 管理 IP, resource_type 类型, resource_health 健康度)
      - it_resource_scan    : 子资源类型 (磁盘/接口)
      - it_resource_scaning : 资源的具体子资源实例 (scaning_resource=所属资源id)
      - it_value_list       : 资源的最新一次取值 (resource_id, scaning_id, index_id, value_word)
      - it_<resource_id>    : 某资源的历史取值表 (动态表名), 4 个字段:
                               id (时间戳+9 位纳秒, 可反推 scan_time = FROM_UNIXTIME(id/1e9)),
                               scaning_id (1=本资源, 其他=子资源 id),
                               index_id (指标 id),
                               index_value (取值结果)
    返回: dict, 包含表清单与字段含义
    """
    return {
        "tables": {
            "it_resource_index": {
                "desc": "指标定义表 (它定义了 Ping响应时间 / 平均CPU利用率 / 平均内存利用率 等指标)",
                "key_fields": {
                    "id": "指标 id (varchar)",
                    "index_name": "指标名称, 如 'Ping响应时间', '平均CPU利用率'",
                    "index_class": "指标种类 (资源指标/子资源指标)",
                    "index_type": "指标类型 (数字/文字)",
                    "index_ompany": "单位 (ms / % / 天)",
                },
            },
            "it_resource_list": {
                "desc": "资源/设备列表 (服务器/交换机等)",
                "key_fields": {
                    "id": "资源 id (varchar)",
                    "resource_name": "资源名称",
                    "resource_ip": "管理 IP",
                    "resource_type": "资源类型 (服务器/交换机/路由器)",
                    "resource_manage": "管理状态",
                    "resource_crux": "关键状态",
                    "resource_health": "健康度",
                    "resource_usable": "可用度",
                    "delete_time": "删除时间, NULL 表示有效",
                },
            },
            "it_resource_scan": {"desc": "子资源类型 (如磁盘, 接口)"},
            "it_resource_scaning": {
                "desc": "资源的具体子资源实例 (一台服务器有多个磁盘)",
                "key_fields": {
                    "id": "子资源 id",
                    "scaning_resource": "所属资源 id (关联 it_resource_list.id)",
                    "scaning_name": "子资源名称 (如 /dev/shm, G1)",
                },
            },
            "it_value_list": {
                "desc": "资源的最新一次取值结果",
                "key_fields": {
                    "resource_id": "资源 id",
                    "scaning_id": "子资源 id (1=资源本身)",
                    "index_id": "指标 id",
                    "value_word": "取值结果",
                },
            },
            "it_<resource_id>": {
                "desc": "动态命名的历史取值表 (一台资源一张表)",
                "key_fields": {
                    "id": "时间戳+9 位纳秒, 用 FROM_UNIXTIME(CEIL(id/1e9)) 还原取值时间",
                    "scaning_id": "1=本资源, 其他=子资源 id",
                    "index_id": "指标 id",
                    "index_value": "取值结果",
                },
            },
        },
        "tips": [
            "Q1 设备总数: COUNT it_resource_list WHERE delete_time IS NULL",
            "Q2 CPU Top10: JOIN it_value_list + it_resource_index (index_name='平均CPU利用率', scaning_id=1)",
            "Q3 Ping 历史: 先 it_resource_list 找 resource_id, 再查 it_<id> WHERE index_id=(Ping响应时间的 index_id)",
        ],
    }


if __name__ == "__main__":
    mcp.run()
