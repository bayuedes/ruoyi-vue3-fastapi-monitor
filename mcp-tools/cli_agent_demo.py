"""
命令行 Agent Demo - IT 监控智能助手 (LangChain 1.x / Python 3.13 兼容版)
========================================================================
基于 ChatOllama.bind_tools() 手写 tool calling 循环, 不依赖 AgentExecutor。

测试 3 个面试问题:
  1. 监控了多少台设备
  2. 当前平均 CPU 利用率最高的 10 台设备是哪些
  3. 192.168.145.253 这个资源的最近的十次 ping 响应时间是多少

前置依赖:
  - HTTP Bridge 运行中: python simple_http_bridge.py (端口 8093)
  - Ollama 运行中 + 已拉取模型 (默认 qwen3:0.6b, 也可换 qwen2.5:7b)

启动:
  python cli_agent_demo.py
"""
import json
import os
import sys
from typing import Optional

# 关键: 绕过系统 Clash 代理 (HTTP_PROXY=127.0.0.1:7890), 让 127.0.0.1 直连
os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")
os.environ.setdefault("no_proxy", "127.0.0.1,localhost")

import httpx
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

BRIDGE_URL = os.getenv("BRIDGE_URL", "http://127.0.0.1:8093")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

# trust_env=False: 不读取系统 HTTP_PROXY 环境变量, 避免 Clash 代理拦截 127.0.0.1 请求
_client = httpx.Client(timeout=30, trust_env=False)


def _get(path: str, params: Optional[dict] = None) -> dict:
    url = BRIDGE_URL.rstrip("/") + path
    r = _client.get(url, params=params or {})
    r.raise_for_status()
    return r.json()


@tool
def get_monitored_device_count() -> dict:
    """
    查询当前监控了多少台设备。
    无参数。返回 {"device_count": int, "description": str}
    对应面试问题: "监控了多少台设备"
    """
    return _get("/tools/device_count")


@tool
def get_top_cpu_devices(limit: int = 10) -> dict:
    """
    查询当前平均 CPU 利用率最高的 N 台设备。
    参数 limit: 默认 10
    返回 {"data": [{rank, resource_id, resource_name, resource_ip, cpu_usage}]}
    对应面试问题: "CPU 利用率最高的 10 台设备是哪些"
    """
    return _get("/tools/top_cpu", {"limit": limit})


@tool
def get_recent_ping_times(ip: str = "192.168.145.253", limit: int = 10) -> dict:
    """
    查询指定 IP 资源最近 N 次 Ping 响应时间(单位 ms)。
    参数:
      ip: 资源管理 IP, 默认 192.168.145.253
      limit: 返回条数, 默认 10
    返回 {"data": [{seq, ping_ms, scan_time}]}
    对应面试问题: "192.168.145.253 最近的十次 ping 响应时间"
    """
    return _get("/tools/recent_ping", {"ip": ip, "limit": limit})


TOOLS = [get_monitored_device_count, get_top_cpu_devices, get_recent_ping_times]
TOOL_BY_NAME = {t.name: t for t in TOOLS}


def run_agent(question: str, llm: ChatOllama, max_iter: int = 6) -> str:
    """手写 tool calling 循环"""
    messages = [
        SystemMessage(content=(
            "你是 IT 监控智能助手。当用户询问监控设备数量、CPU 利用率、Ping 响应时间等问题时,"
            "请调用合适的工具获取真实数据后再回答。"
            "回答时请用中文,简明列出关键数据,不要凭空编造。"
            "如果工具返回的数据为空,请如实告知。"
        )),
        HumanMessage(content=question),
    ]

    llm_with_tools = llm.bind_tools(TOOLS)

    for i in range(max_iter):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content or "(无回答)"

        for tc in ai_msg.tool_calls:
            name = tc["name"]
            args = tc.get("args", {}) or {}
            print(f"  [调用工具] {name}({args})")
            t = TOOL_BY_NAME.get(name)
            if t is None:
                result = f"工具 {name} 不存在"
            else:
                try:
                    result = t.invoke(args)
                except Exception as e:
                    result = f"工具调用失败: {e}"
            # ToolMessage 要求 tool_call_id
            if isinstance(result, (dict, list)):
                content_str = json.dumps(result, ensure_ascii=False)
            else:
                content_str = str(result)
            messages.append(ToolMessage(content=content_str, tool_call_id=tc.get("id", name)))

    return "(达到最大迭代次数,未得到最终回答)"


def main():
    print("=" * 60)
    print("IT 监控智能助手 (命令行 Demo)")
    print("=" * 60)
    print(f"  Bridge URL : {BRIDGE_URL}")
    print(f"  Ollama URL : {OLLAMA_BASE_URL}")
    print(f"  Model      : {OLLAMA_MODEL}")
    print("-" * 60)

    try:
        health = _get("/health")
        print(f"[OK] HTTP Bridge 已就绪: {health}")
    except Exception as e:
        print(f"[FAIL] 无法连接 HTTP Bridge ({BRIDGE_URL}): {e}")
        print("请先启动: python simple_http_bridge.py")
        sys.exit(1)

    try:
        llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL, temperature=0)
        test = llm.invoke("你好")
        print(f"[OK] Ollama 模型可用: {OLLAMA_MODEL}")
    except Exception as e:
        print(f"[FAIL] Ollama 不可用 ({OLLAMA_BASE_URL}, model={OLLAMA_MODEL}): {e}")
        print("请先启动 ollama 服务并拉取模型:")
        print(f"  docker exec knowledge_base_system-ollama-1 ollama pull {OLLAMA_MODEL}")
        sys.exit(1)

    print("-" * 60)
    print("输入问题测试 (q 退出, demo 自动测试 3 个面试题)")
    print("-" * 60)

    samples = [
        "监控了多少台设备",
        "当前平均CPU利用率最高的10台设备是哪些",
        "192.168.145.253这个资源的最近的十次ping响应时间是多少",
    ]

    while True:
        try:
            q = input("\n用户> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见")
            break
        if not q:
            continue
        if q.lower() == "q":
            print("再见")
            break
        if q.lower() == "demo":
            for i, s in enumerate(samples, 1):
                print(f"\n========== 示例问题 {i}: {s} ==========")
                ans = run_agent(s, llm)
                print(f"\n[最终回答]: {ans}")
            continue

        ans = run_agent(q, llm)
        print(f"\n[最终回答]: {ans}")


if __name__ == "__main__":
    main()
