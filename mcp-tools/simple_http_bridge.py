"""
HTTP Bridge (端口 8093) - 给 Langflow 自定义组件 ITMonitorToolkit 调用
直接查询 ruoyi-fastapi MySQL, 返回 JSON

接口:
  GET /tools/device_count           -> {"device_count": 67, ...}
  GET /tools/top_cpu?limit=10      -> {"data": [...]}
  GET /tools/recent_ping?ip=...&limit=10 -> {"data": [...]}
  GET /health                       -> {"status": "ok"}

启动: python simple_http_bridge.py
"""
import os
import time
from typing import Any

import pymysql
import uvicorn
from fastapi import FastAPI, Query

MYSQL_HOST = os.getenv("MONITOR_MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MONITOR_MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MONITOR_MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MONITOR_MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MONITOR_MYSQL_DATABASE", "ruoyi-fastapi")
MYSQL_CHARSET = os.getenv("MONITOR_MYSQL_CHARSET", "utf8mb4")

_conn = None
_conn_time = 0


def _get_conn():
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
    conn = _get_conn()
    with conn.cursor() as cur:
        cur.execute(sql, args)
        rows = cur.fetchall()
    if one:
        return rows[0] if rows else None
    return list(rows)


app = FastAPI(title="IT Monitor HTTP Bridge")


@app.get("/health")
def health():
    return {"status": "ok", "service": "it-monitor-bridge"}


@app.get("/tools/device_count")
def tool_device_count():
    """Q1: 监控设备总数"""
    row = _query(
        "SELECT COUNT(*) AS cnt FROM it_resource_list WHERE delete_time IS NULL",
        one=True,
    )
    cnt = int(row["cnt"]) if row else 0
    return {
        "device_count": cnt,
        "description": f"当前共监控 {cnt} 台设备 (it_resource_list 表 delete_time 为空)",
    }


@app.get("/tools/top_cpu")
def tool_top_cpu(limit: int = Query(default=10, ge=1, le=100)):
    """Q2: CPU 利用率 Top N"""
    rows = _query(
        """
        SELECT v.resource_id, r.resource_name, r.resource_ip, v.value_word AS cpu_usage
        FROM it_value_list v
        JOIN it_resource_index i ON v.index_id = i.id
        LEFT JOIN it_resource_list r ON v.resource_id = r.id
        WHERE i.index_name = %s
          AND v.scaning_id = 1
          AND v.value_word REGEXP '^[0-9]+(\\.[0-9]+)?$'
        ORDER BY CAST(v.value_word AS DECIMAL(10,2)) DESC
        LIMIT %s
        """,
        ("平均CPU利用率", limit),
    )
    data = [
        {
            "rank": i + 1,
            "resource_id": r.get("resource_id"),
            "resource_name": r.get("resource_name"),
            "resource_ip": r.get("resource_ip"),
            "cpu_usage": r.get("cpu_usage"),
        }
        for i, r in enumerate(rows)
    ]
    return {
        "limit": limit,
        "data": data,
        "description": f"CPU 利用率 Top {len(data)} 设备",
    }


@app.get("/tools/recent_ping")
def tool_recent_ping(
    ip: str = Query(default="192.168.145.253"),
    limit: int = Query(default=10, ge=1, le=100),
):
    """Q3: 指定 IP 最近 N 次 Ping 响应时间"""
    res = _query(
        "SELECT id, resource_name FROM it_resource_list WHERE resource_ip = %s AND delete_time IS NULL LIMIT 1",
        (ip,),
        one=True,
    )
    if not res:
        return {"ip": ip, "limit": limit, "data": [], "description": f"未找到 IP {ip}"}
    resource_id = res["id"]
    resource_name = res.get("resource_name")

    idx = _query(
        "SELECT id FROM it_resource_index WHERE index_name = %s LIMIT 1",
        ("Ping响应时间",),
        one=True,
    )
    if not idx:
        return {"ip": ip, "data": [], "description": "未找到 Ping响应时间 指标"}
    index_id = idx["id"]

    table = f"it_{resource_id}"
    if not table[3:].isdigit():
        return {"ip": ip, "data": [], "description": f"非法历史表名: {table}"}

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
        }
        for i, r in enumerate(rows)
    ]
    return {
        "ip": ip,
        "resource_id": resource_id,
        "resource_name": resource_name,
        "limit": limit,
        "data": data,
        "description": f"{ip} ({resource_name}) 最近 {len(data)} 次 Ping 响应时间",
    }


if __name__ == "__main__":
    print("Starting IT Monitor HTTP Bridge on http://0.0.0.0:8093")
    uvicorn.run(app, host="0.0.0.0", port=8093, log_level="info")
