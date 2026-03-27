#!/usr/bin/env python3
"""
Bot Quality Monitor - 完整表格创建脚本

功能：
1. 创建飞书多维表格应用
2. 批量创建 12 张数据表
3. 为核心表添加字段
4. 写入测试数据
5. 保存配置到 config.json

用法：
    由 OpenClaw Bot 自动调用
    python3 create-full-tables.py <user_open_id>
"""

import json
import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("❌ 错误：缺少 user_open_id 参数")
        print("用法: python3 create-full-tables.py <user_open_id>")
        sys.exit(1)
    
    user_open_id = sys.argv[1]
    
    # 输出 Bot 需要执行的操作（JSON 格式）
    # Bot 会解析这个 JSON 并逐步执行
    
    workflow = {
        "description": "创建 Bot 质量监控完整数据表",
        "user_open_id": user_open_id,
        "steps": [
            {
                "step": 1,
                "description": "创建飞书多维表格应用",
                "tool": "feishu_bitable_app",
                "params": {
                    "action": "create",
                    "name": "OpenClaw Bot 质量监控"
                },
                "save_output": "app_token"
            },
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
                        {"name": "L3_季度汇总表"}
                    ]
                },
                "save_output": "table_mappings"
            },
            {
                "step": 3,
                "description": "为 L2_会话汇总表 添加核心字段",
                "substeps": [
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_mappings.L2_会话汇总表}",
                            "field_name": "session_key",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_mappings.L2_会话汇总表}",
                            "field_name": "round_count",
                            "type": 2
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_mappings.L2_会话汇总表}",
                            "field_name": "total_tokens",
                            "type": 2
                        }
                    }
                ]
            },
            {
                "step": 4,
                "description": "写入 3 条测试数据",
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": "${app_token}",
                    "table_id": "${table_mappings.L2_会话汇总表}",
                    "records": [
                        {"fields": {"session_key": "demo_session_1", "round_count": 5, "total_tokens": 2500}},
                        {"fields": {"session_key": "demo_session_2", "round_count": 3, "total_tokens": 1200}},
                        {"fields": {"session_key": "demo_session_3", "round_count": 8, "total_tokens": 4800}}
                    ]
                }
            },
            {
                "step": 5,
                "description": "保存配置到 config.json",
                "action": "save_config",
                "config_path": "~/.openclaw/workspace/skills/bot-quality-monitor/config.json",
                "config_data": {
                    "reportTime": "22:00",
                    "timezone": "GMT+8",
                    "bitableAppToken": "${app_token}",
                    "receiverOpenId": user_open_id,
                    "tables": "${table_mappings}"
                }
            }
        ],
        "success_message": f"""✅ **Bot 质量监控表格创建成功！**

📊 **表格信息**：
- 在你的飞书空间创建
- 链接：https://www.feishu.cn/base/{{app_token}}
- 你拥有完全控制权

📈 **测试数据**：已写入 3 条演示记录

⚙️ **配置已保存**：
- 数据采集已自动开始
- 明天 22:00 将推送首份日报

🎯 **下一步**：
- 点击链接查看你的表格
- 修改推送时间：/settime 21:00
- 所有数据都在你的飞书空间，完全私密

**重要**：请把表格链接保存好，这是你的监控数据中心！
"""
    }
    
    # 输出 JSON（Bot 会解析并执行）
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
