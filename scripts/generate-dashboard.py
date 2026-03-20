#!/usr/bin/env python3
"""
生成 HTML Dashboard（Task 5）
读取 L3 每日指标汇总 + L3_Signal_Alerts，生成交互式可视化看板
"""

import os
import sys
from datetime import datetime, timedelta, timezone

def generate_dashboard(date_str=None):
    """
    生成指定日期的 HTML Dashboard
    
    Args:
        date_str: 日期字符串，格式 YYYY-MM-DD，默认为今天
    """
    
    # 1. 确定日期
    if date_str is None:
        target_date = datetime.now(timezone(timedelta(hours=8)))
    else:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    date_str = target_date.strftime("%Y-%m-%d")
    
    print(f"[Task 5] 生成 {date_str} 的 HTML Dashboard...")
    
    # 2. 读取数据（模拟，实际应从飞书多维表格读取）
    # TODO: 替换为真实 API 调用
    today_health_score = 85.0
    yesterday_health_score = 82.0
    
    last_7_days_dates = [
        (target_date - timedelta(days=i)).strftime("%m-%d") 
        for i in range(6, -1, -1)
    ]
    last_7_days_correction_rate = [8, 7, 9, 6, 5, 4, 5]  # 模拟数据
    last_7_days_first_resolve_rate = [75, 78, 72, 80, 82, 85, 83]
    
    # 3. 生成 Plotly 图表（仪表盘 + 趋势图）
    gauge_html = f"""
    <div id="gauge"></div>
    <script>
        var data = [{{
            type: "indicator",
            mode: "gauge+number+delta",
            value: {today_health_score},
            delta: {{ reference: {yesterday_health_score}, increasing: {{ color: "green" }} }},
            title: {{ text: "综合健康度" }},
            gauge: {{
                axis: {{ range: [0, 100] }},
                bar: {{ color: "darkblue" }},
                steps: [
                    {{ range: [0, 60], color: "lightgray" }},
                    {{ range: [60, 85], color: "yellow" }},
                    {{ range: [85, 100], color: "lightgreen" }}
                ],
                threshold: {{
                    line: {{ color: "red", width: 4 }},
                    thickness: 0.75,
                    value: 80
                }}
            }}
        }}];
        var layout = {{ height: 400 }};
        Plotly.newPlot('gauge', data, layout);
    </script>
    """
    
    trend_html = f"""
    <div id="trend"></div>
    <script>
        var trace1 = {{
            x: {last_7_days_dates},
            y: {last_7_days_correction_rate},
            mode: 'lines+markers',
            name: '纠错率 (%)',
            line: {{ color: 'red', width: 2 }}
        }};
        var trace2 = {{
            x: {last_7_days_dates},
            y: {last_7_days_first_resolve_rate},
            mode: 'lines+markers',
            name: '首解率 (%)',
            line: {{ color: 'green', width: 2 }}
        }};
        var data = [trace1, trace2];
        var layout = {{
            title: '7天质量趋势',
            xaxis: {{ title: '日期' }},
            yaxis: {{ title: '百分比 (%)' }},
            hovermode: 'x unified'
        }};
        Plotly.newPlot('trend', data, layout);
    </script>
    """
    
    # 4. 组装完整 HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot 质量监控 Dashboard - {date_str}</title>
    <script src="https://cdn.plot.ly/plotly-2.18.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .chart {{
            background: white;
            padding: 30px;
            margin: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        footer {{
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
        footer a {{
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }}
        footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 Bot 质量监控 Dashboard</h1>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="chart">
            <h2>📊 综合健康度</h2>
            {gauge_html}
        </div>
        
        <div class="chart">
            <h2>📈 7天趋势</h2>
            {trend_html}
        </div>
        
        <footer>
            <p>
                <a href="https://xcnlx9hjxf3f.feishu.cn/base/Xw4Tb5C8KagMiQswkdacNfVPn8e" target="_blank">
                    📊 查看数据中台
                </a>
                &nbsp;|&nbsp;
                <a href="https://xcnlx9hjxf3f.feishu.cn/wiki/I5fVwdcRCioExIkDIXtcrqdtnUg" target="_blank">
                    📖 查看 PRD
                </a>
            </p>
            <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                Powered by OpenClaw Bot Quality Monitor v2.1.0 💣
            </p>
        </footer>
    </div>
</body>
</html>
    """
    
    # 5. 保存到本地
    output_dir = os.path.expanduser("~/.openclaw/workspace/reports")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"bot-daily-{date_str}.html")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML Dashboard 已生成：{output_path}")
    print(f"   文件大小：{len(html_content)} 字节")
    
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3.5 Task 5: 生成 HTML Dashboard")
    print("=" * 60)
    
    # 生成今天的 Dashboard
    output_path = generate_dashboard()
    
    print("\n" + "=" * 60)
    print("✅ Task 5 完成")
    print(f"打开文件：file://{output_path}")
    print("=" * 60)
