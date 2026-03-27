#!/usr/bin/env python3
"""
Bot Quality Monitor - 完整工作流处理器
当用户说"帮我创建 Bot 质量监控数据表"时，调用此脚本执行完整流程
"""

import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SKILL_DIR)

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if action == "create_bitable_full":
        # 完整流程：创建多维表格 + 生成测试数据 + 生成 Demo 日报
        user_open_id = sys.argv[2] if len(sys.argv) > 2 else ""
        
        result = {
            "action": "create_bitable_full",
            "steps": [
                {
                    "step": 1,
                    "name": "create_app",
                    "description": "创建飞书多维表格应用",
                    "api": "feishu_bitable_app",
                    "params": {
                        "action": "create",
                        "name": "Bot Quality Monitor"
                    }
                },
                {
                    "step": 2,
                    "name": "create_tables",
                    "description": "创建 12 张数据表",
                    "api": "feishu_bitable_app_table",
                    "params": {
                        "action": "create",
                        "table": {
                            "name": "L1_消息明细",
                            "fields": [
                                {"field_name": "session_key", "type": 1},
                                {"field_name": "message_id", "type": 1},
                                {"field_name": "sender_id", "type": 1},
                                {"field_name": "scene", "type": 1},
                                {"field_name": "is_correction", "type": 7},
                                {"field_name": "create_time", "type": 1001}
                            ]
                        }
                    }
                },
                {
                    "step": 3,
                    "name": "write_demo_data",
                    "description": "写入 7 天测试数据",
                    "api": "feishu_bitable_app_table_record",
                    "params": {
                        "action": "batch_create",
                        "records": generate_demo_records()
                    }
                },
                {
                    "step": 4,
                    "name": "generate_demo_report",
                    "description": "生成并推送 Demo 日报",
                    "script": f"python3 {SKILL_DIR}/scripts/generate-demo-data.py"
                }
            ],
            "next_action": "ask_set_time"
        }
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif action == "read_health_data":
        # 读取健康度数据
        result = {
            "action": "read_health_data",
            "api": "feishu_bitable_app_table_record",
            "params": {
                "action": "list",
                "field_names": ["date", "health_score", "total_sessions", "completion_rate", "correction_rate"]
            }
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif action == "generate_dashboard":
        # 生成 Dashboard
        result = {
            "action": "generate_dashboard",
            "script": f"python3 {SKILL_DIR}/bot-daily-report/scripts/generate-html-dashboard.py"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    else:
        print(json.dumps({"error": f"Unknown action: {action}"}))

def generate_demo_records():
    """生成测试数据记录"""
    import random
    from datetime import datetime, timedelta
    
    records = []
    base_date = datetime.now() - timedelta(days=7)
    
    for day in range(7):
        current_date = base_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 每日汇总记录
        record = {
            "fields": {
                "date": date_str,
                "total_sessions": random.randint(100, 200),
                "total_messages": random.randint(500, 1000),
                "completion_rate": random.uniform(80, 95),
                "correction_rate": random.uniform(2, 8),
                "first_solve_rate": random.uniform(75, 95),
                "avg_turns": random.randint(4, 8),
                "error_rate": random.uniform(2, 8),
                "health_score": random.randint(70, 90),
                "health_grade": random.choice(["A", "A", "B", "B", "C"])
            }
        }
        records.append(record)
    
    return records

if __name__ == "__main__":
    main()