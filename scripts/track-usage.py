#!/usr/bin/env python3
"""
Skill 使用埋点 - 匿名上报安装/使用事件

隐私保护:
- 用户可通过设置 SKILL_TRACKING=off 关闭埋点
- 只收集匿名 hash，不收集真实用户 ID
- 静默上报，失败不影响正常使用

跨企业数据收集方案:
- 所有机器人发送数据到统一的飞书 Webhook
- Webhook 触发大少爷的小炸弹接收并写入多维表格
- 无需跨企业权限，100% 可达

使用方式:
    python3 track-usage.py install   # 安装时
    python3 track-usage.py run       # 运行时
    python3 track-usage.py sync      # 同步（每小时）
"""

import os
import sys
import hashlib
import json
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError

# ============ 配置 ============
# 飞书 Webhook（大少爷的数据收集机器人）
# 这个 Webhook 是公开的，所有企业的机器人都可以发送
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/f570f27b-d21d-412d-8dcd-065ff809e14c"

# 本地日志（Fallback）
LOCAL_LOG_DIR = os.path.expanduser("~/.openclaw/workspace/logs")
LOCAL_LOG_FILE = os.path.join(LOCAL_LOG_DIR, "skill-usage.jsonl")

# Skill 信息
SKILL_NAME = "bot-quality-monitor"
SKILL_VERSION = "3.0.0"

# ============ 核心功能 ============

def get_anonymous_user_id():
    """生成匿名用户 ID"""
    if os.environ.get("SKILL_TRACKING", "on").lower() == "off":
        return None
    
    user = os.environ.get("USER", "unknown")
    home = os.environ.get("HOME", "unknown")
    hostname = os.popen("hostname").read().strip()
    
    unique_string = f"{user}:{home}:{hostname}"
    hash_id = hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    return f"anon_{hash_id}"

def get_system_info():
    """获取系统信息（匿名）"""
    import platform
    return {
        "os": os.name,
        "platform": platform.system().lower(),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}"
    }

def log_event(event_type, extra=None):
    """记录事件到本地日志"""
    user_id = get_anonymous_user_id()
    if user_id is None:
        print("[track] SKILL_TRACKING=off, 跳过埋点")
        return
    
    event_data = {
        "event_type": event_type,
        "skill_name": SKILL_NAME,
        "skill_version": SKILL_VERSION,
        "user_id": user_id,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "source": "unknown",
        "extra": json.dumps({**get_system_info(), **(extra or {})}, ensure_ascii=False)
    }
    
    # 写入本地日志
    os.makedirs(LOCAL_LOG_DIR, exist_ok=True)
    with open(LOCAL_LOG_FILE, "a") as f:
        f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
    
    print(f"[track] {event_type} | {SKILL_NAME} v{SKILL_VERSION} | {datetime.now().isoformat()}")
    print(f"[track] 已记录到 {LOCAL_LOG_FILE}")

def sync_to_webhook():
    """
    同步本地日志到飞书 Webhook
    
    跨企业解决方案：通过公开 Webhook 发送数据
    """
    if not os.path.exists(LOCAL_LOG_FILE):
        print("[sync] 没有待同步数据")
        return
    
    # 读取所有事件
    with open(LOCAL_LOG_FILE, "r") as f:
        events = [json.loads(line.strip()) for line in f if line.strip()]
    
    if not events:
        print("[sync] 没有待同步数据")
        return
    
    print(f"[sync] 准备同步 {len(events)} 条记录")
    
    # 构造消息（飞书卡片格式）
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📊 Bot Quality Monitor 使用数据上报"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**事件数量**: {len(events)}\n**上报时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"```json\n{json.dumps(events, indent=2, ensure_ascii=False)}\n```"
                    }
                }
            ]
        }
    }
    
    # 发送到 Webhook
    try:
        req = Request(
            FEISHU_WEBHOOK_URL,
            data=json.dumps(message).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        with urlopen(req, timeout=10) as response:
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
                if result.get("code") == 0:
                    print(f"[sync] ✓ 成功上报 {len(events)} 条记录")
                    
                    # 归档本地日志
                    timestamp = int(datetime.now().timestamp())
                    archived_file = f"{LOCAL_LOG_FILE}.uploaded.{timestamp}"
                    os.rename(LOCAL_LOG_FILE, archived_file)
                    print(f"[sync] ✓ 已归档: {archived_file}")
                else:
                    print(f"[sync] ⚠ 飞书返回错误: {result}")
            else:
                print(f"[sync] ⚠ HTTP {response.status}")
    except URLError as e:
        print(f"[sync] ⚠ 网络错误: {e}")
        print(f"[sync] 数据保留在本地，下次继续尝试")
    except Exception as e:
        print(f"[sync] ⚠ 同步失败: {e}")

# ============ 命令行入口 ============

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: track-usage.py <command> [extra_json]")
        print("命令: install, run, uninstall, error, sync")
        sys.exit(1)
    
    command = sys.argv[1]
    extra = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if command == "sync":
        sync_to_webhook()
    elif command in ["install", "run", "uninstall", "error"]:
        log_event(command, extra)
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
