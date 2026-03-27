#!/usr/bin/env python3
"""
Bot Quality Monitor - 创建飞书多维表格

完整流程:
1. 创建多维表格应用
2. 创建 12 张数据表
3. 为每张表创建字段
4. 生成 7 天测试数据
5. 生成并推送 Demo 日报
6. 保存配置到 config.json

使用方式:
    由 OpenClaw Bot 直接调用（通过 SKILL.md 触发）
    Bot 自动传入 user_open_id
"""

import json
import os
import sys
from datetime import datetime

# 表格配置
TABLE_CONFIGS = [
    {
        "name": "L1_消息明细表",
        "table_id": "tblmKO3HejbWpUWe",  # 占位符，实际创建后会替换
        "fields": [
            {"field_name": "session_key", "type": 1},  # 文本
            {"field_name": "message_id", "type": 1},
            {"field_name": "sender_id", "type": 1},
            {"field_name": "scene", "type": 3, "property": {"options": [
                {"name": "数据分析"}, {"name": "文档处理"}, 
                {"name": "健康诊断"}, {"name": "搜索查询"}, 
                {"name": "代码调试"}, {"name": "闲聊"}, {"name": "其他"}
            ]}},
            {"field_name": "is_correction", "type": 7},  # 复选框
            {"field_name": "create_time", "type": 1001}  # 创建时间
        ]
    },
    {
        "name": "L2_会话汇总表",
        "table_id": "tblT0I1nCFhbpvGa",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "user_owner_id", "type": 1},
            {"field_name": "scene_type", "type": 3, "property": {"options": [
                {"name": "数据分析"}, {"name": "文档处理"}, 
                {"name": "健康诊断"}, {"name": "搜索查询"}, 
                {"name": "代码调试"}, {"name": "闲聊"}, {"name": "其他"}
            ]}},
            {"field_name": "resolution_status", "type": 3, "property": {"options": [
                {"name": "resolved"}, {"name": "partial"}, {"name": "failed"}
            ]}},
            {"field_name": "round_count", "type": 2},  # 数字
            {"field_name": "correction_count", "type": 2},
            {"field_name": "tool_calls_count", "type": 2},
            {"field_name": "total_tokens", "type": 2},
            {"field_name": "duration_seconds", "type": 2},
            {"field_name": "create_time", "type": 1001}
        ]
    },
    {
        "name": "L3_每日指标汇总",
        "table_id": "tbldgJxU6QUSjnf6",
        "fields": [
            {"field_name": "date", "type": 5},  # 日期
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "resolved_sessions", "type": 2},
            {"field_name": "resolution_rate", "type": 2},
            {"field_name": "avg_tokens", "type": 2},
            {"field_name": "health_score", "type": 2}
        ]
    },
    {
        "name": "L3_三类信号表",
        "table_id": "tblVDILmtu1oYRTE",
        "fields": [
            {"field_name": "date", "type": 5},
            {"field_name": "signal_type", "type": 3, "property": {"options": [
                {"name": "质量红灯"}, {"name": "效率黄灯"}, {"name": "资源预警"}
            ]}},
            {"field_name": "description", "type": 1},
            {"field_name": "severity", "type": 3, "property": {"options": [
                {"name": "严重"}, {"name": "警告"}, {"name": "提示"}
            ]}}
        ]
    },
    {
        "name": "L0_Skill_Usage",
        "table_id": "tbllGdVAIIzITahT",
        "fields": [
            {"field_name": "event_type", "type": 3, "property": {"options": [
                {"name": "install"}, {"name": "run"}, 
                {"name": "uninstall"}, {"name": "error"}
            ]}},
            {"field_name": "skill_name", "type": 1},
            {"field_name": "skill_version", "type": 1},
            {"field_name": "user_id", "type": 1},
            {"field_name": "timestamp", "type": 2},
            {"field_name": "source", "type": 1},
            {"field_name": "extra", "type": 1}
        ]
    },
    {
        "name": "L3_Skill_ROI",
        "table_id": "tblvmjcMrdtSFF8D",
        "fields": [
            {"field_name": "skill_name", "type": 1},
            {"field_name": "usage_count", "type": 2},
            {"field_name": "success_rate", "type": 2},
            {"field_name": "avg_duration", "type": 2},
            {"field_name": "roi_score", "type": 2}
        ]
    },
    {
        "name": "L3_Skill_Run",
        "table_id": "tblGOfgzbcle1C4N",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "skills_used", "type": 1},
            {"field_name": "execution_order", "type": 1},
            {"field_name": "success", "type": 7},
            {"field_name": "create_time", "type": 1001}
        ]
    },
    {
        "name": "L2_会话归档表",
        "table_id": "tblarchive2",
        "fields": [
            {"field_name": "session_key", "type": 1},
            {"field_name": "archived_at", "type": 1001}
        ]
    },
    {
        "name": "L1_消息归档表",
        "table_id": "tblarchive1",
        "fields": [
            {"field_name": "message_id", "type": 1},
            {"field_name": "archived_at", "type": 1001}
        ]
    },
    {
        "name": "L3_月度汇总表",
        "table_id": "tblmonthly",
        "fields": [
            {"field_name": "month", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "health_score", "type": 2}
        ]
    },
    {
        "name": "L3_季度汇总表",
        "table_id": "tblquarterly",
        "fields": [
            {"field_name": "quarter", "type": 1},
            {"field_name": "total_sessions", "type": 2},
            {"field_name": "health_score", "type": 2}
        ]
    },
    {
        "name": "配置表",
        "table_id": "tblconfig",
        "fields": [
            {"field_name": "key", "type": 1},
            {"field_name": "value", "type": 1},
            {"field_name": "updated_at", "type": 1001}
        ]
    }
]

def create_bitable_app(user_open_id):
    """
    步骤 1: 创建飞书多维表格应用
    
    Returns:
        dict: {"app_token": "xxx", "url": "xxx"}
    """
    print("[1/6] 创建飞书多维表格应用...")
    print(f"USER_OPEN_ID: {user_open_id}")
    
    # 返回 Bot 需要执行的指令
    return {
        "tool": "feishu_bitable_app",
        "action": "create",
        "name": f"OpenClaw Bot 质量监控 · {datetime.now().strftime('%Y%m%d%H%M')}",
        "folder_token": "",  # 空表示创建在"我的空间"
        "user_open_id": user_open_id  # 关键：传入用户 ID，确保创建在用户空间
    }

def create_tables(app_token):
    """
    步骤 2: 创建所有数据表
    
    Returns:
        list: 批量创建指令列表
    """
    print("[2/6] 创建 12 张数据表...")
    
    return {
        "tool": "feishu_bitable_app_table",
        "action": "batch_create",
        "app_token": app_token,
        "tables": [{"name": t["name"]} for t in TABLE_CONFIGS]
    }

def create_fields(app_token, table_mappings):
    """
    步骤 3: 为每张表创建字段
    
    Args:
        table_mappings: {"L1_消息明细表": "tbl_real_id_xxx", ...}
    
    Returns:
        list: 批量创建字段指令
    """
    print("[3/6] 创建表格字段...")
    
    field_creation_tasks = []
    
    for table_config in TABLE_CONFIGS:
        table_name = table_config["name"]
        table_id = table_mappings.get(table_name)
        
        if not table_id:
            continue
        
        for field in table_config["fields"]:
            task = {
                "tool": "feishu_bitable_app_table_field",
                "action": "create",
                "app_token": app_token,
                "table_id": table_id,
                "field_name": field["field_name"],
                "type": field["type"]
            }
            
            # 如果有 property（如单选/多选的选项），添加
            if "property" in field:
                task["property"] = field["property"]
            
            field_creation_tasks.append(task)
    
    return field_creation_tasks

def generate_demo_data(app_token, table_mappings):
    """
    步骤 4: 生成 7 天测试数据
    
    Returns:
        dict: 生成 Demo 数据指令
    """
    print("[4/6] 生成 7 天测试数据...")
    
    return {
        "tool": "exec",
        "command": f"cd ~/.openclaw/workspace/skills/bot-quality-monitor && python3 scripts/generate-demo-data.py {app_token} {json.dumps(table_mappings)}"
    }

def generate_demo_report(app_token, table_mappings, user_open_id):
    """
    步骤 5: 生成并推送 Demo 日报
    
    Returns:
        dict: 生成 Demo 日报指令
    """
    print("[5/6] 生成 Demo 日报...")
    
    return {
        "tool": "exec",
        "command": f"cd ~/.openclaw/workspace/skills/bot-quality-monitor/bot-daily-report && python3 scripts/generate-signal-alerts.py"
    }

def save_config(app_token, table_mappings, user_open_id):
    """
    步骤 6: 保存配置到 config.json
    
    Returns:
        dict: 保存配置指令
    """
    print("[6/6] 保存配置...")
    
    config_path = os.path.expanduser("~/.openclaw/workspace/skills/bot-quality-monitor/config.json")
    
    config = {
        "reportTime": "22:00",
        "timezone": "GMT+8",
        "bitableAppToken": app_token,
        "receiverOpenId": user_open_id,
        "tables": table_mappings
    }
    
    return {
        "tool": "write_file",
        "path": config_path,
        "content": json.dumps(config, indent=2, ensure_ascii=False)
    }

def main():
    """
    主流程：返回完整的执行计划
    Bot 会按顺序执行这些指令
    """
    if len(sys.argv) < 2:
        print("用法: create-bitable.py <user_open_id>")
        sys.exit(1)
    
    user_open_id = sys.argv[1]
    
    # 返回完整的执行计划（JSON 格式）
    # Bot 会解析这个 JSON 并逐步执行
    
    plan = {
        "workflow": "create_bitable_full",
        "user_open_id": user_open_id,
        "steps": [
            {
                "step": 1,
                "name": "create_app",
                "description": "创建飞书多维表格应用",
                "instruction": create_bitable_app(user_open_id),
                "output_var": "app_token"  # 输出变量，后续步骤可用
            },
            {
                "step": 2,
                "name": "create_tables",
                "description": "创建 12 张数据表",
                "instruction": "DEPENDS_ON:step1",  # 需要等步骤 1 完成
                "output_var": "table_mappings"
            },
            {
                "step": 3,
                "name": "create_fields",
                "description": "创建表格字段",
                "instruction": "DEPENDS_ON:step2",
                "note": "字段创建比较慢，预计 2-3 分钟"
            },
            {
                "step": 4,
                "name": "generate_demo",
                "description": "生成 7 天测试数据",
                "instruction": "DEPENDS_ON:step3"
            },
            {
                "step": 5,
                "name": "generate_report",
                "description": "生成 Demo 日报",
                "instruction": "DEPENDS_ON:step4"
            },
            {
                "step": 6,
                "name": "save_config",
                "description": "保存配置",
                "instruction": "DEPENDS_ON:step1"
            }
        ],
        "success_message": """
✅ **Bot 质量监控表格创建完成！**

📊 **表格信息**：
- 名称：OpenClaw Bot 质量监控
- 链接：https://www.feishu.cn/base/{app_token}
- 包含 12 张数据表

📈 **测试数据**：
- 已生成 7 天模拟数据
- Demo 日报已推送

⚙️ **配置保存**：
- config.json 已自动更新
- 推送时间：22:00 (GMT+8)

🎯 **下一步**：
1. 查看表格：[点击访问](https://www.feishu.cn/base/{app_token})
2. 修改推送时间：对我说 `/settime 21:00`
3. 数据采集已自动开始，明天 22:00 将推送首份日报

有任何问题随时问我！💣
        """
    }
    
    print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
