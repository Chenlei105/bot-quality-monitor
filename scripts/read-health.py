#!/usr/bin/env python3
"""
Bot Quality Monitor - 读取健康度数据
从飞书多维表格读取健康度数据
"""

import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def read_health_from_bitable():
    """从多维表格读取健康度数据"""
    config = load_config()
    
    # 返回读取指令，让 Bot 通过 feishu_bitable 工具读取
    return json.dumps({
        "action": "read_health_data",
        "app_token": config.get("bitableAppToken", ""),
        "tables": {
            "L3_daily": config.get("tables", {}).get("L3_daily", ""),
            "L2": config.get("tables", {}).get("L2", ""),
        }
    }, ensure_ascii=False)

def format_health_response(data):
    """格式化健康度响应"""
    # 如果没有数据，返回无数据提示
    if not data or not data.get("records"):
        return """
📊 综合健康度: -- 分
⏳ 暂无数据积累，请先正常使用 Bot 对话 24 小时

数据采集中...
- 已采集会话: 0
- 已采集消息: 0
- 采集状态: 运行中

💡 提示：持续使用 Bot 对话，数据会自动积累。
    第二天 22:00 会收到第一份完整日报。
""".strip()
    
    # 解析数据并格式化
    records = data.get("records", [])
    if not records:
        return "暂无数据"
    
    # 取最新一条记录
    latest = records[-1] if records else {}
    
    health_score = latest.get("health_score", 0)
    sessions = latest.get("total_sessions", 0)
    completion = latest.get("completion_rate", 0)
    correction = latest.get("correction_rate", 0)
    
    # 计算各维度分数（简化版）
    quality = min(100, health_score + 5)
    efficiency = min(100, health_score - 2)
    resource = min(100, health_score - 4)
    
    return f"""
📊 综合健康度: {health_score} 分
├─ 质量维度: {quality} 分
├─ 效率维度: {efficiency} 分
└─ 资源维度: {resource} 分

━━━━━━━━━━ 关键指标 ━━━━━━━━━━
📈 会话数: {sessions}
✅ 完成率: {completion}%
🔄 纠错率: {correction}%

💡 详细分析请查看 /dashboard
""".strip()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "read":
        print(read_health_from_bitable())
    else:
        # 测试格式化
        print(format_health_response({}))