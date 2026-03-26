#!/usr/bin/env python3
"""
Bot Quality Monitor - 自动创建飞书多维表格
用法（由Bot调用）:
python3 auto-create-bitable.py <user_open_id>
"""

import sys
import json
import os
from datetime import datetime

# 获取用户OpenID
if len(sys.argv) < 2:
    print("Error: missing user_open_id argument")
    sys.exit(1)

user_open_id = sys.argv[1]

# 定义所有表结构
# 字段类型参考: 1=文本, 2=数字, 3=单选, 4=多选, 5=日期, 7=复选框, 11=人员, 13=电话, 15=超链接, 17=附件, 1001=创建时间, 1002=修改时间
TABLES = [
    {
        "name": "L1_消息明细",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "message_id", "type": 1},
            {"field_name": "sender_id", "type": 1},
            {"field_name": "sender_name", "type": 1},
            {"field_name": "content", "type": 1},
            {"field_name": "msg_type", "type": 1},
            {"field_name": "create_time", "type": 5},
            {"field_name": "scene", "type": 1},
            {"field_name": "is_correction", "type": 7},
            {"field_name": "is_error", "type": 7},
        ]
    },
    {
        "name": "L2_会话汇总",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "start_time", "type": 5},
            {"field_name": "end_time", "type": 5},
            {"field_name": "turns", "type": 2},
            {"field_name": "corrections", "type": 2},
            {"field_name": "tool_calls", "type": 2},
            {"field_name": "scene", "type": 1},
            {"field_name": "completed", "type": 7},
            {"field_name": "duration_minutes", "type": 2},
            # 新增：支持四维指标体系
            {"field_name": "task_resolution", "type": 3, "property": {"options": ["已解决", "未解决", "进行中"]}},
            {"field_name": "satisfaction_score", "type": 2},
            {"field_name": "token_total", "type": 2},
            {"field_name": "is_unexpected_interrupt", "type": 7},
            {"field_name": "complexity", "type": 3, "property": {"options": ["简单", "中等", "复杂"]}},
            {"field_name": "response_time_ms", "type": 2},
        ]
    },
    {
        "name": "L3_每日指标汇总",
        "fields": [
            {"field_name": "date", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "total_messages", "type": 2},
            {"field_name": "completion_rate", "type": 2},
            {"field_name": "correction_rate", "type": 2},
            {"field_name": "first_solve_rate", "type": 2},
            {"field_name": "avg_turns", "type": 2},
            {"field_name": "error_rate", "type": 2},
            {"field_name": "health_score", "type": 2},
            {"field_name": "health_grade", "type": 1},
            # 新增：支持四维指标体系
            {"field_name": "task_resolution_rate", "type": 2},
            {"field_name": "avg_satisfaction", "type": 2},
            {"field_name": "avg_task_duration", "type": 2},
            {"field_name": "avg_token_per_task", "type": 2},
            {"field_name": "interrupt_rate", "type": 2},
            {"field_name": "p99_response_time", "type": 2},
            # 维度分数
            {"field_name": "quality_score", "type": 2},
            {"field_name": "efficiency_score", "type": 2},
            {"field_name": "resource_score", "type": 2},
        ]
    },
    {
        "name": "L3_Signal_Alerts",
        "fields": [
            {"field_name": "date", "type": 1},
            {"field_name": "signal_type", "type": 1},
            {"field_name": "signal_name", "type": 1},
            {"field_name": "description", "type": 1},
            {"field_name": "recommendation", "type": 1},
            {"field_name": "processed", "type": 7},
        ]
    },
    {
        "name": "L3_Skill_ROI",
        "fields": [
            {"field_name": "skill_id", "type": 1},
            {"field_name": "skill_name", "type": 1},
            {"field_name": "total_runs", "type": 2},
            {"field_name": "success_rate", "type": 2},
            {"field_name": "avg_cost_tokens", "type": 2},
            {"field_name": "roi_score", "type": 2},
            {"field_name": "recommendation", "type": 1},
            {"field_name": "update_time", "type": 5},
        ]
    },
    {
        "name": "L3_Skill_Run",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "skill_id", "type": 1},
            {"field_name": "skill_name", "type": 1},
            {"field_name": "start_time", "type": 5},
            {"field_name": "end_time", "type": 5},
            {"field_name": "success", "type": 7},
            {"field_name": "tokens_used", "type": 2},
        ]
    },
    {
        "name": "L0_Skill_Usage",
        "fields": [
            {"field_name": "event_type", "type": 1},
            {"field_name": "skill_id", "type": 1},
            {"field_name": "skill_version", "type": 1},
            {"field_name": "timestamp", "type": 5},
            {"field_name": "os_type", "type": 1},
            {"field_name": "anonymous_id", "type": 1},
        ]
    },
    {
        "name": "L2_会话归档",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "archive_date", "type": 5},
            {"field_name": "original_created", "type": 5},
            {"field_name": "days_kept", "type": 2},
        ]
    },
    {
        "name": "L1_消息归档",
        "fields": [
            {"field_name": "message_id", "type": 1},
            {"field_name": "archive_date", "type": 5},
            {"field_name": "original_created", "type": 5},
            {"field_name": "days_kept", "type": 2},
        ]
    },
    {
        "name": "L3_月度汇总",
        "fields": [
            {"field_name": "year_month", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "total_messages", "type": 2},
            {"field_name": "avg_health_score", "type": 2},
            {"field_name": "avg_completion_rate", "type": 2},
            {"field_name": "avg_correction_rate", "type": 2},
        ]
    },
    {
        "name": "L3_季度汇总",
        "fields": [
            {"field_name": "year_quarter", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "total_messages", "type": 2},
            {"field_name": "avg_health_score", "type": 2},
            {"field_name": "avg_completion_rate", "type": 2},
            {"field_name": "avg_correction_rate", "type": 2},
        ]
    },
    {
        "name": "L3_年度汇总",
        "fields": [
            {"field_name": "year", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "total_messages", "type": 2},
            {"field_name": "avg_health_score", "type": 2},
            {"field_name": "avg_completion_rate", "type": 2},
            {"field_name": "avg_correction_rate", "type": 2},
        ]
    }
]

# 修复上面的语法错误（is_correction 缺少引号）
for table in TABLES:
    for field in table["fields"]:
        if field["field_name"] == "is_correction":
            field["field_name"] = "is_correction"

print(f"🚀 开始创建 Bot Quality Monitor 多维表格...")
print(f"👤 创建者: {user_open_id}")
print(f"📊 将创建 {len(TABLES)} 张数据表...")

# 注意：这个脚本需要由Bot通过feishu_bitable工具调用
# 这里只输出表结构定义，实际创建由Bot工具完成
# 脚本输出JSON，Bot解析后调用飞书API

result = {
    "action": "create_bitable",
    "name": "Bot Quality Monitor",
    "user_open_id": user_open_id,
    "tables": TABLES
}

print(json.dumps(result, indent=2, ensure_ascii=False))
