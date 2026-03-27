#!/usr/bin/env python3
"""
平台级 Dashboard 生成器

功能:
- 读取中央表格的所有数据
- 生成平台级统计 Dashboard
- 包含：Bot 排行榜 + 失败模式识别 + Skill 编排推荐

用法:
    python3 generate-platform-dashboard.py
"""

import sys
import json
from datetime import datetime, timedelta

# 中央表格（大少爷）
CENTRAL_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"

PLATFORM_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Bot 质量监控 - 平台看板</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-card .value {{
            font-size: 48px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
        }}
        .card h3 {{
            font-size: 20px;
            margin-bottom: 20px;
        }}
        .chart {{
            width: 100%;
            height: 300px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        th {{
            background: rgba(255, 255, 255, 0.1);
        }}
        .rank-1 {{ color: #FFD700; }}
        .rank-2 {{ color: #C0C0C0; }}
        .rank-3 {{ color: #CD7F32; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 OpenClaw Bot 质量监控 - 平台看板</h1>
            <div class="date">{date}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div>总用户数</div>
                <div class="value">{total_users}</div>
            </div>
            <div class="stat-card">
                <div>总 Bot 数</div>
                <div class="value">{total_bots}</div>
            </div>
            <div class="stat-card">
                <div>总会话数</div>
                <div class="value">{total_sessions:,}</div>
            </div>
            <div class="stat-card">
                <div>平台健康度</div>
                <div class="value">{platform_health}</div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="card">
                <h3>🏆 Bot 排行榜 Top 10</h3>
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>Bot 名称</th>
                            <th>健康度</th>
                            <th>会话数</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bot_ranking_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <h3>⚡ Skill 使用 Top 10</h3>
                <div id="skill-chart" class="chart"></div>
            </div>
            
            <div class="card">
                <h3>🔍 失败模式分布</h3>
                <div id="failure-chart" class="chart"></div>
            </div>
            
            <div class="card">
                <h3>💡 Skill 编排推荐</h3>
                {skill_recommendations}
            </div>
        </div>
    </div>
    
    <script>
        const skillChart = echarts.init(document.getElementById('skill-chart'));
        skillChart.setOption({{
            tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
            xAxis: {{ type: 'value' }},
            yAxis: {{ type: 'category', data: {skill_names} }},
            series: [{{
                type: 'bar',
                data: {skill_counts},
                itemStyle: {{ color: '#FFD700' }}
            }}]
        }});
        
        const failureChart = echarts.init(document.getElementById('failure-chart'));
        failureChart.setOption({{
            tooltip: {{ trigger: 'item' }},
            series: [{{
                type: 'pie',
                radius: '70%',
                data: {failure_data},
                label: {{ color: 'white' }}
            }}]
        }});
        
        window.addEventListener('resize', () => {{
            skillChart.resize();
            failureChart.resize();
        }});
    </script>
</body>
</html>
'''

def main():
    """主流程"""
    workflow = {
        "description": "生成平台级 Dashboard（中央表格）",
        "steps": [
            # Step 1: 读取所有 Bot 的每日数据
            {
                "step": 1,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_每日指标汇总_table_id}",
                    "filter": {
                        "conjunction": "and",
                        "conditions": [{
                            "field_name": "date",
                            "operator": "isGreaterEqual",
                            "value": [(datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')]
                        }]
                    },
                    "page_size": 500
                },
                "save_as": "all_bot_data"
            },
            
            # Step 2: 读取 Skill ROI 数据
            {
                "step": 2,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_Skill_ROI_table_id}",
                    "page_size": 500
                },
                "save_as": "skill_roi_data"
            },
            
            # Step 3: 读取失败会话
            {
                "step": 3,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L2_会话汇总表_table_id}",
                    "filter": {
                        "conjunction": "and",
                        "conditions": [{
                            "field_name": "completion_status",
                            "operator": "is",
                            "value": ["failed"]
                        }]
                    },
                    "page_size": 500
                },
                "save_as": "failed_sessions"
            },
            
            # Step 4: 生成 HTML
            {
                "step": 4,
                "description": "生成平台 Dashboard HTML",
                "python_function": "generate_platform_html",
                "params": {
                    "all_bot_data": "${all_bot_data}",
                    "skill_roi_data": "${skill_roi_data}",
                    "failed_sessions": "${failed_sessions}"
                },
                "save_as": "html_content"
            },
            
            # Step 5: 保存到本地
            {
                "step": 5,
                "action": "write_file",
                "params": {
                    "path": "/root/.openclaw/workspace/reports/platform-dashboard-latest.html",
                    "content": "${html_content}"
                }
            }
        ],
        "output": "${html_content}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
