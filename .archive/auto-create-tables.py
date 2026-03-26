#!/usr/bin/env python3
"""
Bot Quality Monitor - 自动创建表格完整流程

这个脚本封装了从创建表格到生成 Demo 的完整流程，
供 OpenClaw Bot 在用户说"帮我创建表格"时自动调用。

流程：
1. 创建飞书多维表格
2. 批量创建 11 张数据表
3. 为核心表（L2_会话汇总）添加关键字段
4. 写入 3 条测试数据
5. 保存配置到 config.json
6. 返回成功消息（包含表格链接）

用法：
    由 Bot 自动调用，传入 user_open_id
    python3 auto-create-tables.py <user_open_id>
"""

import json
import sys
import os

# 表格配置
TABLE_NAMES = [
    "L1_消息明细表",
    "L2_会话汇总表", 
    "L3_每日指标汇总",
    "L3_三类信号表",
    "L0_Skill_Usage",
    "L3_Skill_ROI",
    "L3_Skill_Run",
    "L2_会话归档表",
    "L1_消息归档表",
    "L3_月度汇总表",
    "L3_季度汇总表"
]

# 核心字段（L2_会话汇总表）
CORE_FIELDS = [
    {"field_name": "session_key", "type": 1},       # 文本
    {"field_name": "round_count", "type": 2},       # 数字
    {"field_name": "correction_count", "type": 2},  # 数字
    {"field_name": "tool_calls_count", "type": 2},  # 数字
    {"field_name": "total_tokens", "type": 2},      # 数字
    {"field_name": "duration_seconds", "type": 2}   # 数字
]

# 测试数据
DEMO_DATA = [
    {
        "session_key": "agent:main:feishu:direct:demo_user_1",
        "round_count": 5,
        "correction_count": 1,
        "tool_calls_count": 8,
        "total_tokens": 2500,
        "duration_seconds": 180
    },
    {
        "session_key": "agent:main:feishu:group:demo_group_1", 
        "round_count": 3,
        "correction_count": 0,
        "tool_calls_count": 4,
        "total_tokens": 1200,
        "duration_seconds": 90
    },
    {
        "session_key": "agent:main:feishu:direct:demo_user_2",
        "round_count": 8,
        "correction_count": 2,
        "tool_calls_count": 15,
        "total_tokens": 4800,
        "duration_seconds": 420
    }
]

def print_instructions(user_open_id):
    """
    输出 Bot 需要执行的指令（JSON 格式）
    Bot 会解析并逐步执行
    """
    
    instructions = {
        "workflow": "auto_create_tables",
        "user_open_id": user_open_id,
        "steps": [
            {
                "step": 1,
                "action": "create_bitable_app",
                "params": {
                    "name": "OpenClaw Bot 质量监控",
                    "folder_token": ""
                },
                "output": "app_token"
            },
            {
                "step": 2,
                "action": "batch_create_tables",
                "depends_on": "step1",
                "params": {
                    "tables": [{"name": name} for name in TABLE_NAMES]
                },
                "output": "table_mappings"
            },
            {
                "step": 3,
                "action": "create_fields_for_L2",
                "depends_on": "step2",
                "params": {
                    "fields": CORE_FIELDS,
                    "table_name": "L2_会话汇总表"
                }
            },
            {
                "step": 4,
                "action": "insert_demo_data",
                "depends_on": "step3",
                "params": {
                    "records": DEMO_DATA,
                    "table_name": "L2_会话汇总表"
                }
            },
            {
                "step": 5,
                "action": "save_config",
                "depends_on": "step1",
                "params": {
                    "config_path": "~/.openclaw/workspace/skills/bot-quality-monitor/config.json",
                    "user_open_id": user_open_id
                }
            }
        ],
        "success_message": """
✅ **Bot 质量监控表格创建成功！**

📊 **表格信息**：
- 名称：OpenClaw Bot 质量监控
- 链接：https://www.feishu.cn/base/{app_token}
- 包含 12 张数据表（11 张 + 默认表）

📈 **测试数据**：
- 已写入 3 条演示记录到 L2_会话汇总表
- 可立即查看数据

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
    
    print(json.dumps(instructions, indent=2, ensure_ascii=False))

def main():
    if len(sys.argv) < 2:
        print("错误：缺少 user_open_id 参数")
        print("用法: python3 auto-create-tables.py <user_open_id>")
        sys.exit(1)
    
    user_open_id = sys.argv[1]
    print_instructions(user_open_id)

if __name__ == "__main__":
    main()
