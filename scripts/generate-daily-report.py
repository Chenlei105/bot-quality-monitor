#!/usr/bin/env python3
"""
用户日报生成脚本 - 飞书卡片版

功能:
- 读取 L3_每日指标汇总表
- 读取 L3_三类信号表
- 生成飞书卡片（参考设计图）
- 输出 JSON 工作流供 Bot 执行

卡片格式:
- Header: 科技蓝背景 + Bot 名称健康报告
- 模块 1: 📊 执行摘要（四维指标）
- 模块 2: 👤 用户使用（今日数据）
- 模块 3: 📈 趋势对比（7天表格）
- 模块 4: 🔍 智能洞察（三类信号）
- 模块 5: ⚡ 优先行动（紧急/重要/优化）
- Footer: 详细报告链接 + Dashboard 链接

配色:
- 主色: 科技蓝 #1677FF
- 绿色: #52C41A (增长)
- 黄色: #FAAD14 (警告)
- 红色: #FF4D4F (下降/紧急)

用法:
    python3 generate-daily-report.py
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"

def load_config():
    """加载配置"""
    try:
        if not CONFIG_PATH.exists():
            return None
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except Exception as e:
        print(f"加载配置失败: {e}", file=sys.stderr)
        return None

def generate_feishu_card(data):
    """生成飞书卡片 JSON"""
    
    # 提取数据
    today = data.get('today', {})
    yesterday = data.get('yesterday', {})
    week_trend = data.get('week_trend', [])
    signals = data.get('signals', [])
    bot_name = data.get('bot_name', '小炸弹')
    
    # 计算趋势
    health_trend = _calc_trend(today.get('health_score', 0), yesterday.get('health_score', 0))
    quality_trend = _calc_trend(today.get('quality_score', 0), yesterday.get('quality_score', 0))
    efficiency_trend = _calc_trend(today.get('efficiency_score', 0), yesterday.get('efficiency_score', 0))
    resource_trend = _calc_trend(today.get('resource_score', 0), yesterday.get('resource_score', 0))
    
    # 构造飞书卡片
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",  # 科技蓝
                "title": {
                    "tag": "plain_text",
                    "content": f"🤖 {bot_name} 健康报告"
                },
                "subtitle": {
                    "tag": "plain_text",
                    "content": datetime.now().strftime('%Y年%m月%d日')
                }
            },
            "elements": [
                # 模块 1: 📊 执行摘要
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**📊 执行摘要**"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "grey",
                    "columns": [
                        _score_column("综合健康度", today.get('health_score', 0), health_trend, "blue"),
                        _score_column("质量维度", today.get('quality_score', 0), quality_trend, "green"),
                        _score_column("效率维度", today.get('efficiency_score', 0), efficiency_trend, "orange"),
                        _score_column("资源维度", today.get('resource_score', 0), resource_trend, "purple")
                    ]
                },
                
                # 模块 2: 👤 用户使用
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**👤 用户使用**"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "grey",
                    "columns": [
                        _metric_column("今日会话", today.get('total_sessions', 0)),
                        _metric_column("完成率", f"{today.get('task_completion_rate', 0):.0%}"),
                        _metric_column("平均响应", f"{today.get('avg_response_ms', 0)/1000:.1f}s"),
                        _metric_column("满意度", f"{today.get('approval_rate', 0):.0%}")
                    ]
                },
                
                # 模块 3: 📈 趋势对比（7天）
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**📈 近7天趋势**"
                    }
                },
                {
                    "tag": "hr"
                },
                _week_trend_table(week_trend),
                
                # 模块 4: 🔍 智能洞察
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**🔍 智能洞察**"
                    }
                },
                {
                    "tag": "hr"
                },
                _signals_section(signals),
                
                # 模块 5: ⚡ 优先行动
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**⚡ 优先行动**"
                    }
                },
                {
                    "tag": "hr"
                },
                _action_section(signals),
                
                # Footer: 详细报告 + Dashboard
                {
                    "tag": "hr"
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "📄 详细报告"
                            },
                            "type": "primary",
                            "url": "${detailed_report_url}"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "📊 Dashboard"
                            },
                            "url": "${dashboard_url}"
                        }
                    ]
                }
            ]
        }
    }
    
    return card

def _calc_trend(current, previous):
    """计算趋势"""
    if previous == 0:
        return {"direction": "→", "value": "0.0%", "color": "grey"}
    
    change = current - previous
    percent = (change / previous) * 100
    
    if change > 0:
        return {"direction": "↑", "value": f"+{percent:.1f}%", "color": "green"}
    elif change < 0:
        return {"direction": "↓", "value": f"{percent:.1f}%", "color": "red"}
    else:
        return {"direction": "→", "value": "0.0%", "color": "grey"}

def _score_column(title, score, trend, color):
    """生成评分列"""
    level = "优秀" if score >= 85 else "良好" if score >= 70 else "待改进"
    
    return {
        "tag": "column",
        "width": "weighted",
        "weight": 1,
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{title}**"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"<font color='{color}'>{score:.0f}/100</font>"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": level
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"<font color='{trend['color']}'>{trend['direction']} {trend['value']}</font>"
                }
            }
        ]
    }

def _metric_column(title, value):
    """生成指标列"""
    return {
        "tag": "column",
        "width": "weighted",
        "weight": 1,
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{value}**"
                }
            }
        ]
    }

def _week_trend_table(week_data):
    """生成7天趋势表格"""
    if not week_data:
        return {
            "tag": "div",
            "text": {
                "tag": "plain_text",
                "content": "暂无数据"
            }
        }
    
    # 构造 Markdown 表格
    table_md = "| 日期 | 会话数 | 完成率 | 满意度 | 健康度 |\n"
    table_md += "|------|--------|--------|--------|--------|\n"
    
    for day in week_data[-7:]:  # 最近7天
        date = day.get('date', '')
        sessions = day.get('total_sessions', 0)
        completion = day.get('task_completion_rate', 0)
        approval = day.get('approval_rate', 0)
        health = day.get('health_score', 0)
        
        table_md += f"| {date} | {sessions} | {completion:.0%} | {approval:.0%} | {health:.0f} |\n"
    
    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": table_md
        }
    }

def _signals_section(signals):
    """生成信号模块"""
    p0_count = len([s for s in signals if s.get('severity') == 'P0'])
    p1_count = len([s for s in signals if s.get('severity') == 'P1'])
    p2_count = len([s for s in signals if s.get('severity') == 'P2'])
    
    content = f"🔴 [P0] 紧急问题: {p0_count} 条\n"
    content += f"🟡 [P1] 重要问题: {p1_count} 条\n"
    content += f"🟢 [P2] 优化建议: {p2_count} 条\n\n"
    
    # 列出前3个信号
    for signal in signals[:3]:
        severity = signal.get('severity', 'P2')
        signal_type = signal.get('signal_type', '')
        description = signal.get('description', '')
        
        emoji = "🔴" if severity == "P0" else "🟡" if severity == "P1" else "🟢"
        content += f"{emoji} **{signal_type}**: {description}\n"
    
    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content
        }
    }

def _action_section(signals):
    """生成行动模块"""
    urgent = [s for s in signals if s.get('severity') == 'P0']
    important = [s for s in signals if s.get('severity') == 'P1']
    optimize = [s for s in signals if s.get('severity') == 'P2']
    
    content = "**紧急**:\n"
    for s in urgent[:2]:
        content += f"- {s.get('action_required', '无')}\n"
    
    content += "\n**重要**:\n"
    for s in important[:2]:
        content += f"- {s.get('action_required', '无')}\n"
    
    content += "\n**优化**:\n"
    for s in optimize[:2]:
        content += f"- {s.get('action_required', '无')}\n"
    
    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content
        }
    }

def main():
    """主流程"""
    config = load_config()
    if not config:
        print(json.dumps({"error": "配置未就绪"}))
        sys.exit(1)
    
    app_token = config['bitableAppToken']
    l3_daily_table = config['tables'].get('L3_每日指标汇总')
    l3_signals_table = config['tables'].get('L3_三类信号表')
    
    # 输出工作流（由 Bot 执行）
    workflow = {
        "description": "生成用户日报飞书卡片",
        "steps": [
            # Step 1: 读取今日数据
            {
                "step": 1,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l3_daily_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [
                            {
                                "field_name": "date",
                                "operator": "is",
                                "value": [datetime.now().strftime('%Y/%m/%d')]
                            }
                        ]
                    }
                },
                "save_as": "today_data"
            },
            
            # Step 2: 读取昨日数据
            {
                "step": 2,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l3_daily_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [
                            {
                                "field_name": "date",
                                "operator": "is",
                                "value": [(datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')]
                            }
                        ]
                    }
                },
                "save_as": "yesterday_data"
            },
            
            # Step 3: 读取最近7天数据
            {
                "step": 3,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l3_daily_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [
                            {
                                "field_name": "date",
                                "operator": "isGreaterEqual",
                                "value": [(datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')]
                            }
                        ]
                    },
                    "sort": [{"field_name": "date", "desc": False}]
                },
                "save_as": "week_trend"
            },
            
            # Step 4: 读取三类信号
            {
                "step": 4,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l3_signals_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [
                            {
                                "field_name": "trigger_date",
                                "operator": "is",
                                "value": [datetime.now().strftime('%Y/%m/%d')]
                            }
                        ]
                    },
                    "sort": [{"field_name": "severity", "desc": False}]
                },
                "save_as": "signals"
            },
            
            # Step 5: 生成飞书卡片
            {
                "step": 5,
                "description": "生成飞书卡片 JSON",
                "python_function": "generate_feishu_card",
                "params": {
                    "today": "${today_data[0]}",
                    "yesterday": "${yesterday_data[0]}",
                    "week_trend": "${week_trend}",
                    "signals": "${signals}",
                    "bot_name": config.get('botName', '小炸弹')
                },
                "save_as": "feishu_card"
            }
        ],
        "output": "${feishu_card}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
