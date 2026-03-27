#!/usr/bin/env python3
"""
Bot Quality Monitor - 全自动安装脚本

功能:
- 一句话完成所有安装步骤
- 创建飞书多维表格
- 批量创建 12 张数据表
- 添加必要字段
- 写入测试数据
- 保存配置文件

用法:
    由 OpenClaw Bot 自动调用
    python3 auto-setup.py <user_open_id>
    
    或手动测试:
    python3 auto-setup.py ou_baa3525cf6cb5c0fc1ce4e26753d812d
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 配置路径
CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"

def main():
    """主流程"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少 user_open_id 参数",
            "usage": "python3 auto-setup.py <user_open_id>"
        }))
        sys.exit(1)
    
    user_open_id = sys.argv[1]
    
    # 生成完整的自动化工作流
    workflow = {
        "description": "Bot Quality Monitor 全自动安装",
        "user_open_id": user_open_id,
        "steps": [
            # 步骤 1: 创建飞书多维表格应用
            {
                "step": 1,
                "description": "创建飞书多维表格应用",
                "tool": "feishu_bitable_app",
                "action": "create",
                "params": {
                    "action": "create",
                    "name": "OpenClaw Bot 质量监控"
                },
                "save_as": "app_token"
            },
            
            # 步骤 2: 批量创建 12 张数据表
            {
                "step": 2,
                "description": "批量创建 12 张数据表",
                "tool": "feishu_bitable_app_table",
                "action": "batch_create",
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
                "save_as": "table_ids"
            },
            
            # 步骤 3: 为 L2_会话汇总表 添加字段
            {
                "step": 3,
                "description": "为 L2_会话汇总表 添加字段",
                "substeps": [
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "会话ID",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "用户所有者ID",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "Bot ID",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "Bot昵称",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "场景类型",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "轮次数",
                            "type": 2
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "纠错次数",
                            "type": 2
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "工具调用次数",
                            "type": 2
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "完成状态",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "模型名称",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "开始时间",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "结束时间",
                            "type": 1
                        }
                    },
                    {
                        "tool": "feishu_bitable_app_table_field",
                        "params": {
                            "action": "create",
                            "app_token": "${app_token}",
                            "table_id": "${table_ids.L2_会话汇总表}",
                            "field_name": "创建时间",
                            "type": 5
                        }
                    }
                ]
            },
            
            # 步骤 4: 写入 3 条测试数据
            {
                "step": 4,
                "description": "写入 3 条测试数据",
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": "${app_token}",
                    "table_id": "${table_ids.L2_会话汇总表}",
                    "records": [
                        {
                            "fields": {
                                "会话ID": "demo_session_1",
                                "用户所有者ID": user_open_id,
                                "Bot ID": "cli_a922b6c0b8b89bd1",
                                "Bot昵称": "小炸弹 💣",
                                "场景类型": "数据分析",
                                "轮次数": 5,
                                "纠错次数": 0,
                                "工具调用次数": 3,
                                "完成状态": "completed",
                                "模型名称": "claude-k4-sonnet",
                                "创建时间": int(datetime.now().timestamp() * 1000)
                            }
                        },
                        {
                            "fields": {
                                "会话ID": "demo_session_2",
                                "用户所有者ID": user_open_id,
                                "Bot ID": "cli_a922b6c0b8b89bd1",
                                "Bot昵称": "小炸弹 💣",
                                "场景类型": "文档处理",
                                "轮次数": 3,
                                "纠错次数": 1,
                                "工具调用次数": 2,
                                "完成状态": "completed",
                                "模型名称": "claude-k4-sonnet",
                                "创建时间": int(datetime.now().timestamp() * 1000)
                            }
                        },
                        {
                            "fields": {
                                "会话ID": "demo_session_3",
                                "用户所有者ID": user_open_id,
                                "Bot ID": "cli_a922b6c0b8b89bd1",
                                "Bot昵称": "小炸弹 💣",
                                "场景类型": "搜索查询",
                                "轮次数": 8,
                                "纠错次数": 2,
                                "工具调用次数": 5,
                                "完成状态": "failed",
                                "模型名称": "claude-k4-sonnet",
                                "创建时间": int(datetime.now().timestamp() * 1000)
                            }
                        }
                    ]
                }
            },
            
            # 步骤 5: 保存配置到 config.json
            {
                "step": 5,
                "description": "保存配置到 config.json",
                "action": "write_file",
                "params": {
                    "path": str(CONFIG_PATH),
                    "content": {
                        "reportTime": "22:00",
                        "timezone": "GMT+8",
                        "bitableAppToken": "${app_token}",
                        "receiverOpenId": user_open_id,
                        "tables": {
                            "L1": "${table_ids.L1_消息明细表}",
                            "L2": "${table_ids.L2_会话汇总表}",
                            "L3_daily": "${table_ids.L3_每日指标汇总}",
                            "L3_signals": "${table_ids.L3_三类信号表}",
                            "L0_usage": "${table_ids.L0_Skill_Usage}",
                            "L3_roi": "${table_ids.L3_Skill_ROI}",
                            "L3_run": "${table_ids.L3_Skill_Run}",
                            "L2_archive": "${table_ids.L2_会话归档表}",
                            "L1_archive": "${table_ids.L1_消息归档表}",
                            "L3_monthly": "${table_ids.L3_月度汇总表}",
                            "L3_quarterly": "${table_ids.L3_季度汇总表}"
                        }
                    }
                }
            }
        ],
        
        # 成功消息
        "success_message": f"""✅ **Bot 质量监控表格创建成功！**

📊 **表格信息**：
- 在你的飞书空间创建
- 链接：https://www.feishu.cn/base/{{app_token}}
- 你拥有完全控制权
- 包含 12 张数据表（11 张 + 默认表）

📈 **测试数据**：已写入 3 条演示记录

⚙️ **配置已保存**：
- 数据采集已自动开始
- 明天 22:00 将推送首份日报

🎯 **下一步**：
- 点击链接查看你的表格
- 修改推送时间：/settime 21:00

**重要**：请把表格链接保存好，这是你的监控数据中心！
"""
    }
    
    # 输出 JSON (Bot 会解析并执行)
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
