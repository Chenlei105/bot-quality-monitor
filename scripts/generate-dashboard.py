#!/usr/bin/env python3
"""
Dashboard HTML 生成器

功能:
- 读取 L3_每日指标汇总表
- 生成白色背景的 Dashboard HTML
- 使用 ECharts 图表库
- 参考第二张设计图的布局

布局:
- 顶部指标栏（4 个 Scorecard）
- 左侧：用户使用趋势图 + 场景分布
- 右侧：近7天对比表格 + Bad Case 列表
- 底部：Skill 使用统计表格

配色:
- 背景: 白色 #FFFFFF
- 卡片: 白色 + 浅灰边框
- 图表: ECharts 默认主题（浅色）

用法:
    python3 generate-dashboard.py
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bot_name} 健康看板</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #FFFFFF;
            color: #333;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            color: #1677FF;
            margin-bottom: 10px;
        }}
        .header .date {{
            color: #666;
            font-size: 14px;
        }}
        
        /* 顶部指标栏 */
        .scorecard-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .scorecard {{
            background: white;
            border: 1px solid #E5E5E5;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .scorecard .title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
        .scorecard .value {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .scorecard .trend {{
            font-size: 14px;
        }}
        .scorecard.blue .value {{ color: #1677FF; }}
        .scorecard.green .value {{ color: #52C41A; }}
        .scorecard.orange .value {{ color: #FAAD14; }}
        .scorecard.purple .value {{ color: #722ED1; }}
        .trend.up {{ color: #52C41A; }}
        .trend.down {{ color: #FF4D4F; }}
        
        /* 主内容区 */
        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border: 1px solid #E5E5E5;
            border-radius: 8px;
            padding: 20px;
        }}
        .card h3 {{
            font-size: 16px;
            margin-bottom: 20px;
            color: #333;
        }}
        .chart {{
            width: 100%;
            height: 300px;
        }}
        
        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #E5E5E5;
        }}
        th {{
            background: #F5F5F5;
            font-weight: 600;
            color: #333;
        }}
        tr:hover {{
            background: #FAFAFA;
        }}
        
        /* Bad Case 列表 */
        .case-item {{
            padding: 10px;
            border-left: 3px solid #FF4D4F;
            background: #FFF1F0;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        .case-item .title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .case-item .desc {{
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 {bot_name} 健康看板</h1>
        <div class="date">{date}</div>
    </div>
    
    <!-- 顶部指标栏 -->
    <div class="scorecard-row">
        <div class="scorecard blue">
            <div class="title">综合健康度</div>
            <div class="value">{health_score}</div>
            <div class="trend {health_trend_class}">{health_trend}</div>
        </div>
        <div class="scorecard green">
            <div class="title">质量得分</div>
            <div class="value">{quality_score}</div>
            <div class="trend {quality_trend_class}">{quality_trend}</div>
        </div>
        <div class="scorecard orange">
            <div class="title">效率得分</div>
            <div class="value">{efficiency_score}</div>
            <div class="trend {efficiency_trend_class}">{efficiency_trend}</div>
        </div>
        <div class="scorecard purple">
            <div class="title">资源得分</div>
            <div class="value">{resource_score}</div>
            <div class="trend {resource_trend_class}">{resource_trend}</div>
        </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="main-grid">
        <!-- 左上：用户使用趋势 -->
        <div class="card">
            <h3>📈 用户使用趋势（7天）</h3>
            <div id="trend-chart" class="chart"></div>
        </div>
        
        <!-- 右上：近7天对比表格 -->
        <div class="card">
            <h3>📊 近7天数据对比</h3>
            <table>
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>会话数</th>
                        <th>完成率</th>
                        <th>健康度</th>
                    </tr>
                </thead>
                <tbody>
                    {week_table_rows}
                </tbody>
            </table>
        </div>
        
        <!-- 左下：场景分布 -->
        <div class="card">
            <h3>🎯 场景分布</h3>
            <div id="scene-chart" class="chart"></div>
        </div>
        
        <!-- 右下：Top 5 Bad Case -->
        <div class="card">
            <h3>🔍 Top 5 Bad Case</h3>
            {bad_cases}
        </div>
    </div>
    
    <!-- 底部：Skill 使用统计 -->
    <div class="card">
        <h3>⚡ Skill 使用统计</h3>
        <table>
            <thead>
                <tr>
                    <th>Skill 名称</th>
                    <th>调用次数</th>
                    <th>成功率</th>
                    <th>平均耗时</th>
                </tr>
            </thead>
            <tbody>
                {skill_table_rows}
            </tbody>
        </table>
    </div>
    
    <script>
        // 用户使用趋势图
        const trendChart = echarts.init(document.getElementById('trend-chart'));
        trendChart.setOption({{
            tooltip: {{ trigger: 'axis' }},
            legend: {{ data: ['会话数', '完成率'] }},
            xAxis: {{ type: 'category', data: {week_dates} }},
            yAxis: [
                {{ type: 'value', name: '会话数' }},
                {{ type: 'value', name: '完成率', max: 100 }}
            ],
            series: [
                {{
                    name: '会话数',
                    type: 'line',
                    data: {session_data},
                    smooth: true,
                    itemStyle: {{ color: '#1677FF' }}
                }},
                {{
                    name: '完成率',
                    type: 'line',
                    yAxisIndex: 1,
                    data: {completion_data},
                    smooth: true,
                    itemStyle: {{ color: '#52C41A' }}
                }}
            ]
        }});
        
        // 场景分布图
        const sceneChart = echarts.init(document.getElementById('scene-chart'));
        sceneChart.setOption({{
            tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
            xAxis: {{ type: 'value' }},
            yAxis: {{ type: 'category', data: {scene_names} }},
            series: [{{
                type: 'bar',
                data: {scene_counts},
                itemStyle: {{ color: '#1677FF' }}
            }}]
        }});
        
        // 响应式
        window.addEventListener('resize', () => {{
            trendChart.resize();
            sceneChart.resize();
        }});
    </script>
</body>
</html>
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
    
    # 输出工作流
    workflow = {
        "description": "生成 Dashboard HTML",
        "steps": [
            # Step 1: 读取最近7天数据
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
                            "operator": "isGreaterEqual",
                            "value": [(datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')]
                        }]
                    },
                    "sort": [{"field_name": "date", "desc": False}]
                },
                "save_as": "week_data"
            },
            
            # Step 2: 读取最近30天会话（分析场景）
            {
                "step": 2,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": app_token,
                    "table_id": l2_table,
                    "filter": {
                        "conjunction": "and",
                        "conditions": [{
                            "field_name": "session_start",
                            "operator": "isGreaterEqual",
                            "value": [(datetime.now() - timedelta(days=30)).timestamp() * 1000]
                        }]
                    }
                },
                "save_as": "sessions"
            },
            
            # Step 3: 生成 HTML
            {
                "step": 3,
                "description": "生成 Dashboard HTML",
                "python_function": "generate_html",
                "params": {
                    "week_data": "${week_data}",
                    "sessions": "${sessions}",
                    "bot_name": config.get('botName', '小炸弹')
                },
                "save_as": "html_content"
            },
            
            # Step 4: 保存到本地
            {
                "step": 4,
                "description": "保存 HTML 文件",
                "action": "write_file",
                "params": {
                    "path": str(Path.home() / ".openclaw/workspace/reports/dashboard-latest.html"),
                    "content": "${html_content}"
                }
            }
        ],
        "output": "${html_content}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
