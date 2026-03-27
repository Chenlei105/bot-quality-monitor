#!/usr/bin/env python3
"""
Bot Quality Monitor - 全自动安装脚本 v5.0

新增功能:
- 添加 L3_年度汇总表
- L2_会话汇总表: 35+ 个字段
- L3_每日指标汇总: 25+ 个字段
- L3_三类信号表: 8 个字段
- 完整测试数据

用法:
    python3 auto-setup-v5.py <user_open_id>
"""

import sys
import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"

# ============ 字段定义 ============

# L2_会话汇总表字段（35 个）
L2_FIELDS = [
    {"field_name": "session_id", "type": 1},  # 文本
    {"field_name": "bot_id", "type": 1},
    {"field_name": "bot_name", "type": 1},
    {"field_name": "user_id", "type": 1},
    {"field_name": "用户所有者ID", "type": 1},  # 关键字段
    {"field_name": "channel_type", "type": 3, "property": {  # 单选
        "options": [
            {"name": "group"}, {"name": "p2p"}, {"name": "bot_push"}
        ]
    }},
    {"field_name": "scene_type", "type": 3, "property": {
        "options": [
            {"name": "数据分析"}, {"name": "文档处理"}, {"name": "健康诊断"},
            {"name": "技能管理"}, {"name": "配置咨询"}, {"name": "闲聊"}
        ]
    }},
    {"field_name": "turn_count", "type": 2},  # 数字
    {"field_name": "completion_status", "type": 3, "property": {
        "options": [
            {"name": "completed"}, {"name": "failed"}, {"name": "abandoned"}
        ]
    }},
    {"field_name": "satisfaction_signal", "type": 3, "property": {
        "options": [
            {"name": "positive"}, {"name": "negative"}, {"name": "neutral"}
        ]
    }},
    {"field_name": "correction_count", "type": 2},
    {"field_name": "first_resolve", "type": 7},  # 复选框
    {"field_name": "knowledge_hit", "type": 7},
    {"field_name": "failure_type", "type": 3, "property": {
        "options": [
            {"name": "api失效"}, {"name": "输出为空"}, {"name": "纳错率过高"},
            {"name": "首解率低"}, {"name": "知识库缺失"}, {"name": "超时"}, {"name": "其他"}
        ]
    }},
    {"field_name": "session_start", "type": 5, "property": {"date_formatter": "yyyy/MM/dd HH:mm"}},  # 日期时间
    {"field_name": "session_end", "type": 5, "property": {"date_formatter": "yyyy/MM/dd HH:mm"}},
    {"field_name": "duration_ms", "type": 2},
    {"field_name": "skills_triggered", "type": 1},
    {"field_name": "Skill数量", "type": 2},
    {"field_name": "协作成本系数", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "关键路径", "type": 7},
    {"field_name": "total_tokens", "type": 2},
    {"field_name": "input_tokens", "type": 2},
    {"field_name": "output_tokens", "type": 2},
    {"field_name": "model_used", "type": 1},
    {"field_name": "api_calls", "type": 2},
    {"field_name": "api_errors", "type": 2},
    {"field_name": "memory_used_kb", "type": 2},
    {"field_name": "task_resolution", "type": 3, "property": {
        "options": [
            {"name": "solved"}, {"name": "partial"}, {"name": "unsolved"}
        ]
    }},
    {"field_name": "user_feedback", "type": 1},
    {"field_name": "error_message", "type": 1},
    {"field_name": "retry_count", "type": 2},
    {"field_name": "session_cost_usd", "type": 2, "property": {"formatter": "0.0000"}},
]

# L3_每日指标汇总字段（25 个）
L3_DAILY_FIELDS = [
    {"field_name": "date", "type": 5, "property": {"date_formatter": "yyyy/MM/dd"}},
    {"field_name": "bot_id", "type": 1},
    {"field_name": "bot_name", "type": 1},
    {"field_name": "用户所有者ID", "type": 1},
    {"field_name": "total_sessions", "type": 2},
    {"field_name": "completed_sessions", "type": 2},
    {"field_name": "task_completion_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "correction_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "first_resolve_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "knowledge_hit_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "approval_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "avg_response_ms", "type": 2},
    {"field_name": "timeout_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "api_success_rate", "type": 2, "property": {"formatter": "0.00%"}},
    {"field_name": "total_tokens", "type": 2},
    {"field_name": "total_cost_usd", "type": 2, "property": {"formatter": "0.0000"}},
    {"field_name": "avg_tokens_per_session", "type": 2},
    {"field_name": "avg_cost_per_session", "type": 2, "property": {"formatter": "0.0000"}},
    {"field_name": "quality_score", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "efficiency_score", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "resource_score", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "health_score", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "unique_users", "type": 2},
    {"field_name": "peak_hour", "type": 1},
    {"field_name": "trend_vs_yesterday", "type": 1},  # JSON: {quality: "+2.1%", efficiency: "-0.8%"}
]

# L3_三类信号表字段（8 个）
L3_SIGNALS_FIELDS = [
    {"field_name": "signal_id", "type": 1},
    {"field_name": "signal_type", "type": 3, "property": {  # 高分低用/首解率下降/知识缺失
        "options": [
            {"name": "高分低用"}, {"name": "首解率下降"}, {"name": "知识缺失"}
        ]
    }},
    {"field_name": "bot_id", "type": 1},
    {"field_name": "用户所有者ID", "type": 1},
    {"field_name": "trigger_date", "type": 5, "property": {"date_formatter": "yyyy/MM/dd"}},
    {"field_name": "severity", "type": 3, "property": {
        "options": [{"name": "P0"}, {"name": "P1"}, {"name": "P2"}]
    }},
    {"field_name": "description", "type": 1},
    {"field_name": "action_required", "type": 1},
]

# L0_Skill_Usage字段（7 个）
L0_SKILL_FIELDS = [
    {"field_name": "event_type", "type": 3, "property": {
        "options": [
            {"name": "install"}, {"name": "uninstall"}, {"name": "run"}, {"name": "error"}
        ]
    }},
    {"field_name": "skill_name", "type": 1},
    {"field_name": "skill_version", "type": 1},
    {"field_name": "user_id", "type": 1},  # 匿名 hash
    {"field_name": "timestamp", "type": 5, "property": {"date_formatter": "yyyy/MM/dd HH:mm"}},
    {"field_name": "source", "type": 3, "property": {
        "options": [
            {"name": "clawhub"}, {"name": "github"}, {"name": "manual"}, {"name": "unknown"}
        ]
    }},
    {"field_name": "extra", "type": 1},  # JSON
]

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少 user_open_id 参数"}))
        sys.exit(1)
    
    user_open_id = sys.argv[1]
    
    workflow = {
        "description": "Bot Quality Monitor v5.0 全自动安装",
        "user_open_id": user_open_id,
        "steps": [
            # 步骤 1: 创建多维表格
            {
                "step": 1,
                "description": "创建飞书多维表格应用",
                "tool": "feishu_bitable_app",
                "params": {
                    "action": "create",
                    "name": f"OpenClaw Bot 质量监控 - {user_open_id[:8]}"
                },
                "save_as": "app_token"
            },
            
            # 步骤 2: 批量创建 12 张表
            {
                "step": 2,
                "description": "批量创建 12 张数据表",
                "tool": "feishu_bitable_app_table",
                "params": {
                    "action": "batch_create",
                    "app_token": "${app_token}",
                    "tables": [
                        {"name": "L1_消息明细表"},
                        {"name": "L2_会话汇总表"},
                        {"name": "L3_每日指标汇总"},
                        {"name": "L3_三类信号表"},
                        {"name": "L0_Skill_Usage"},
                        {"name": "L3_Skill_ROI"},
                        {"name": "L3_Skill_Run"},
                        {"name": "L2_会话归档表"},
                        {"name": "L1_消息归档表"},
                        {"name": "L3_月度汇总表"},
                        {"name": "L3_季度汇总表"},
                        {"name": "L3_年度汇总表"}  # 新增
                    ]
                },
                "save_as": "table_ids"
            },
            
            # 步骤 3: 为 L2_会话汇总表 批量添加字段
            {
                "step": 3,
                "description": "为 L2_会话汇总表 批量添加 35 个字段",
                "foreach": L2_FIELDS,
                "tool": "feishu_bitable_app_table_field",
                "params": {
                    "action": "create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L2_会话汇总表}",
                    "field_name": "${item.field_name}",
                    "type": "${item.type}",
                    "property": "${item.property}"  # 可选
                }
            },
            
            # 步骤 4: 为 L3_每日指标汇总 批量添加字段
            {
                "step": 4,
                "description": "为 L3_每日指标汇总 批量添加 25 个字段",
                "foreach": L3_DAILY_FIELDS,
                "tool": "feishu_bitable_app_table_field",
                "params": {
                    "action": "create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L3_每日指标汇总}",
                    "field_name": "${item.field_name}",
                    "type": "${item.type}",
                    "property": "${item.property}"
                }
            },
            
            # 步骤 5: 为 L3_三类信号表 批量添加字段
            {
                "step": 5,
                "description": "为 L3_三类信号表 批量添加 8 个字段",
                "foreach": L3_SIGNALS_FIELDS,
                "tool": "feishu_bitable_app_table_field",
                "params": {
                    "action": "create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L3_三类信号表}",
                    "field_name": "${item.field_name}",
                    "type": "${item.type}",
                    "property": "${item.property}"
                }
            },
            
            # 步骤 6: 为 L0_Skill_Usage 批量添加字段
            {
                "step": 6,
                "description": "为 L0_Skill_Usage 批量添加 7 个字段",
                "foreach": L0_SKILL_FIELDS,
                "tool": "feishu_bitable_app_table_field",
                "params": {
                    "action": "create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L0_Skill_Usage}",
                    "field_name": "${item.field_name}",
                    "type": "${item.type}",
                    "property": "${item.property}"
                }
            },
            
            # 步骤 7: 写入完整测试数据（7 天 × 10 条 = 70 条）
            {
                "step": 7,
                "description": "写入完整测试数据到 L2 表",
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L2_会话汇总表}",
                    "records": "${generate_test_data(70, user_open_id)}"  # 动态生成
                }
            },
            
            # 步骤 8: 保存配置文件
            {
                "step": 8,
                "description": "保存配置到 config.json",
                "action": "write_file",
                "params": {
                    "path": str(CONFIG_PATH),
                    "content": {
                        "reportTime": "22:00",
                        "timezone": "GMT+8",
                        "bitableAppToken": "${app_token}",
                        "receiverOpenId": user_open_id,
                        "tables": "${table_ids}"  # 所有表的 ID
                    }
                }
            }
        ],
        "success_message": f"✅ Bot Quality Monitor v5.0 安装成功！\n\n📊 已创建 12 张表格\n📝 已添加 75+ 个字段\n🧪 已写入 70 条测试数据\n\n配置已保存到: {CONFIG_PATH}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
