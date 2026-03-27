#!/usr/bin/env python3
"""
详细文档生成器

功能:
- 生成飞书文档（Markdown 格式）
- 包含完整的分析报告
- 支持 Bad Case 汇总
- 输出 JSON 工作流

文档结构:
1. 执行摘要
2. 核心指标
3. 问题分析
4. Bad Case 汇总
5. 优化建议

用法:
    python3 generate-detailed-report.py
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"

MARKDOWN_TEMPLATE = '''# {bot_name} 健康报告 - {date}

## 一、执行摘要

**综合健康度**: {health_score}/100 ({health_level})
**质量维度**: {quality_score}/100 ({quality_level})
**效率维度**: {efficiency_score}/100 ({efficiency_level})
**资源维度**: {resource_score}/100 ({resource_level})

---

## 二、核心指标

### 2.1 质量指标

- **任务完成率**: {completion_rate:.1%}
- **首次解决率**: {first_resolve_rate:.1%}
- **纠错率**: {correction_rate:.1%}
- **知识命中率**: {knowledge_hit_rate:.1%}

### 2.2 效率指标

- **平均响应时长**: {avg_response_ms:.0f}ms
- **超时率**: {timeout_rate:.1%}
- **API 成功率**: {api_success_rate:.1%}

### 2.3 资源指标

- **总 Token 消耗**: {total_tokens:,}
- **平均每会话 Token**: {avg_tokens_per_session:.0f}
- **总成本**: ${total_cost_usd:.4f}
- **平均每会话成本**: ${avg_cost_per_session:.4f}

---

## 三、问题分析

{problem_analysis}

---

## 四、Bad Case 汇总

{bad_cases}

---

## 五、优化建议

{recommendations}

---

**报告生成时间**: {generation_time}
**数据周期**: 最近 7 天
'''

def load_config():
    """加载配置"""
    try:
        if not CONFIG_PATH.exists():
            return None
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return None

def main():
    """主流程"""
    config = load_config()
    if not config:
        print(json.dumps({"error": "配置未就绪"}))
        sys.exit(1)
    
    app_token = config['bitableAppToken']
    l2_table = config['tables'].get('L2_会话汇总表')
    l3_daily_table = config['tables'].get('L3_每日指标汇总')
    l3_signals_table = config['tables'].get('L3_三类信号表')
    
    # 输出工作流
    workflow = {
        "description": "生成详细文档（飞书云文档）",
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
                        "conditions": [{
                            "field_name": "date",
                            "operator": "is",
                            "value": [datetime.now().strftime('%Y/%m/%d')]
                        }]
                    }
                },
                "save_as": "today_data"
            },
            
            # Step 2: 读取最近 Bad Case（失败会话）
            {
                "step": 2,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l2_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [
                            {
                                "field_name": "completion_status",
                                "operator": "is",
                                "value": ["failed"]
                            },
                            {
                                "field_name": "session_start",
                                "operator": "isGreaterEqual",
                                "value": [(datetime.now() - timedelta(days=7)).timestamp() * 1000]
                            }
                        ]
                    },
                    "page_size": 20
                },
                "save_as": "bad_cases"
            },
            
            # Step 3: 读取三类信号
            {
                "step": 3,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l3_signals_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [{
                            "field_name": "trigger_date",
                            "operator": "is",
                            "value": [datetime.now().strftime('%Y/%m/%d')]
                        }]
                    }
                },
                "save_as": "signals"
            },
            
            # Step 4: 生成 Markdown
            {
                "step": 4,
                "description": "生成 Markdown 文档",
                "python_function": "generate_markdown",
                "params": {
                    "today_data": "${today_data[0]}",
                    "bad_cases": "${bad_cases}",
                    "signals": "${signals}",
                    "bot_name": config.get('botName', '小炸弹')
                },
                "save_as": "markdown_content"
            },
            
            # Step 5: 创建飞书云文档
            {
                "step": 5,
                "tool": "feishu_create_doc",
                "params": {
                    "title": f"{config.get('botName', '小炸弹')} 健康报告 - {datetime.now().strftime('%Y-%m-%d')}",
                    "markdown": "${markdown_content}",
                    "folder_token": config.get('reportFolderToken')  # 可选
                },
                "save_as": "doc_url"
            }
        ],
        "output": "${doc_url}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
