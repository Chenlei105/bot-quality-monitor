#!/usr/bin/env python3
"""
Skill 使用埋点 - 匿名上报安装/使用事件

隐私保护:
- 用户可通过设置 SKILL_TRACKING=off 关闭埋点
- 只收集匿名 hash，不收集真实用户 ID
- 静默上报，失败不影响正常使用

使用方式:
    python3 track-usage.py install   # 安装时
    python3 track-usage.py run       # 运行时
    python3 track-usage.py error     # 出错时
"""

import os
import sys
import hashlib
import json
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError

# ============ 配置 ============
BITABLE_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
TABLE_ID = "tbllGdVAIIzITahT"
SKILL_NAME = "bot-quality-monitor"
SKILL_VERSION = "3.0.0"

# 飞书 API（使用 App Token 直接写入，需要表格开放编辑权限）
# 注意：生产环境建议使用 Webhook 或有鉴权的 API
API_BASE = "https://open.feishu.cn/open-apis/bitable/v1"


def get_anonymous_id() -> str:
    """生成匿名用户标识（基于机器特征的 hash）"""
    features = [
        os.environ.get("USER", ""),
        os.environ.get("HOME", ""),
        os.environ.get("HOSTNAME", ""),
    ]
    raw = "|".join(features)
    return "anon_" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def get_extra_info() -> str:
    """收集非敏感的环境信息"""
    info = {
        "os": os.name,
        "platform": sys.platform,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
    }
    # 检查 OpenClaw 版本
    openclaw_version = os.environ.get("OPENCLAW_VERSION", "unknown")
    if openclaw_version != "unknown":
        info["openclaw"] = openclaw_version
    return json.dumps(info, ensure_ascii=False)


def track(event_type: str, extra_data: dict = None):
    """
    上报埋点事件
    
    Args:
        event_type: install | uninstall | run | error
        extra_data: 额外信息（可选）
    """
    # 检查用户是否关闭埋点
    if os.environ.get("SKILL_TRACKING", "on").lower() == "off":
        print("[track] 埋点已关闭 (SKILL_TRACKING=off)")
        return False
    
    # 构建记录
    timestamp = int(datetime.now().timestamp() * 1000)
    extra_info = get_extra_info()
    if extra_data:
        extra_info = json.dumps({**json.loads(extra_info), **extra_data}, ensure_ascii=False)
    
    record = {
        "fields": {
            "event_type": event_type,
            "skill_name": SKILL_NAME,
            "skill_version": SKILL_VERSION,
            "user_id": get_anonymous_id(),
            "timestamp": timestamp,
            "source": os.environ.get("SKILL_SOURCE", "unknown"),
            "extra": extra_info
        }
    }
    
    # 打印本地日志（调试用）
    print(f"[track] {event_type} | {SKILL_NAME} v{SKILL_VERSION} | {datetime.now().isoformat()}")
    
    # 注意：直接调用飞书 API 需要 access_token
    # 这里先写入本地日志，实际上报需要配置鉴权
    log_file = os.path.expanduser("~/.openclaw/workspace/logs/skill-usage.jsonl")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(json.dumps(record["fields"], ensure_ascii=False) + "\n")
    
    print(f"[track] 已记录到 {log_file}")
    return True


def sync_to_bitable():
    """
    将本地日志同步到飞书多维表格
    
    方案：生成待上报数据文件，由 OpenClaw Agent 自动上报
    """
    log_file = os.path.expanduser("~/.openclaw/workspace/logs/skill-usage.jsonl")
    if not os.path.exists(log_file):
        print("[sync] 无待同步数据")
        return
    
    # 读取本地日志
    records = []
    with open(log_file, "r") as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    if not records:
        print("[sync] 无有效数据")
        return
    
    print(f"[sync] 准备同步 {len(records)} 条记录到飞书多维表格")
    print(f"[sync] 目标表: {BITABLE_APP_TOKEN}/{TABLE_ID}")
    
    # 生成待上报数据文件，供 OpenClaw Agent 读取
    sync_data_file = os.path.expanduser("~/.openclaw/workspace/logs/skill-usage-sync.json")
    with open(sync_data_file, "w") as f:
        json.dump({
            "app_token": BITABLE_APP_TOKEN,
            "table_id": TABLE_ID,
            "records": [{"fields": r} for r in records]
        }, f, ensure_ascii=False, indent=2)
    
    print(f"[sync] 待上报数据已保存: {sync_data_file}")
    print("[sync] OpenClaw Agent 会在下次 heartbeat 时自动上报")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 track-usage.py <event_type> [extra_json]")
        print("  event_type: install | uninstall | run | error | sync")
        print("  extra_json: 可选的 JSON 格式额外信息")
        print("\nExamples:")
        print("  python3 track-usage.py install")
        print("  python3 track-usage.py run '{\"scene\": \"daily_report\"}'")
        print("  python3 track-usage.py sync  # 同步到飞书")
        sys.exit(1)
    
    event = sys.argv[1]
    
    if event == "sync":
        sync_to_bitable()
    else:
        extra = None
        if len(sys.argv) > 2:
            try:
                extra = json.loads(sys.argv[2])
            except json.JSONDecodeError:
                extra = {"raw": sys.argv[2]}
        track(event, extra)
