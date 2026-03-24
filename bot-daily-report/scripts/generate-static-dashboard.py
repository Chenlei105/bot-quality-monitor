#!/usr/bin/env python3
"""
生成静态图片版本的 HTML Dashboard
使用 Plotly 生成静态图片并嵌入 HTML
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import base64
from io import BytesIO

print("=" * 70)
print("📊 生成静态图片版 HTML Dashboard")
print("=" * 70)

# 生成仪表盘图表
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=82,
    title={'text': "综合健康度", 'font': {'size': 24}},
    delta={'reference': 80, 'increasing': {'color': "green"}},
    gauge={
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "#8bc34a"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 60], 'color': "#ffebee"},
            {'range': [60, 75], 'color': "#fff3e0"},
            {'range': [75, 90], 'color': "#e8f5e9"},
            {'range': [90, 100], 'color': "#c8e6c9"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 80
        }
    }
))
fig_gauge.update_layout(width=500, height=400)

# 转换为 base64
buffer = BytesIO()
fig_gauge.write_image(buffer, format='png')
buffer.seek(0)
gauge_base64 = base64.b64encode(buffer.read()).decode()

# 生成趋势图
fig_trend = go.Figure()
dates = ["03-18", "03-19", "03-20", "03-21", "03-22", "03-23", "03-24"]
fig_trend.add_trace(go.Scatter(
    x=dates, y=[5, 4, 3, 4, 3, 2, 3],
    mode='lines+markers', name='纠错率 (%)',
    line={'color': 'red', 'width': 2}, marker={'size': 8}
))
fig_trend.add_trace(go.Scatter(
    x=dates, y=[75, 78, 80, 83, 85, 87, 88],
    mode='lines+markers', name='首解率 (%)',
    line={'color': 'green', 'width': 2}, marker={'size': 8}
))
fig_trend.add_trace(go.Scatter(
    x=dates, y=[80, 82, 85, 87, 88, 90, 91],
    mode='lines+markers', name='任务完成率 (%)',
    line={'color': 'blue', 'width': 2}, marker={'size': 8}
))
fig_trend.update_layout(
    title='7 天趋势',
    xaxis_title='日期',
    yaxis_title='百分比 (%)',
    hovermode='x unified',
    width=800,
    height=400
)

buffer = BytesIO()
fig_trend.write_image(buffer, format='png')
buffer.seek(0)
trend_base64 = base64.b64encode(buffer.read()).decode()

# 生成热力图
fig_heatmap = go.Figure(data=go.Heatmap(
    z=[[88, 75, 90], [75, 80, 85], [58, 60, 70], [90, 85, 95]],
    x=["质量", "效率", "资源"],
    y=["数据分析", "文档处理", "健康诊断", "技能管理"],
    colorscale='RdYlGn',
    reversescale=False
))
fig_heatmap.update_layout(
    title='场景健康度热力图',
    xaxis_title='指标维度',
    yaxis_title='场景分类',
    width=600,
    height=400
)

buffer = BytesIO()
fig_heatmap.write_image(buffer, format='png')
buffer.seek(0)
heatmap_base64 = base64.b64encode(buffer.read()).decode()

# 生成 HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot 质量日报 Dashboard · {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        h1 {{
            font-size: 32px;
            margin-bottom: 30px;
            color: #1a73e8;
            border-bottom: 3px solid #1a73e8;
            padding-bottom: 15px;
        }}
        h2 {{
            font-size: 24px;
            margin: 40px 0 20px 0;
            color: #555;
        }}
        .chart-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .signals-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .signal-card {{
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid;
            background: #e8f5e9;
            border-color: #4caf50;
        }}
        .signal-card h3 {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            background: #4caf50;
            color: white;
            margin-top: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f5f5f5;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Bot 质量日报 Dashboard · {datetime.now().strftime('%Y-%m-%d')}</h1>
        
        <h2>1. 综合健康度仪表盘</h2>
        <div class="chart-container">
            <img src="data:image/png;base64,{gauge_base64}" alt="综合健康度仪表盘">
        </div>
        
        <h2>2. 📈 7 天趋势</h2>
        <div class="chart-container">
            <img src="data:image/png;base64,{trend_base64}" alt="7天趋势图">
        </div>
        
        <h2>3. 🎨 场景健康度热力图</h2>
        <div class="chart-container">
            <img src="data:image/png;base64,{heatmap_base64}" alt="场景健康度热力图">
        </div>
        
        <h2>4. 🔔 三类智能信号</h2>
        <div class="signals-container">
            <div class="signal-card">
                <h3>🟢 高分低用</h3>
                <p>小炸弹健康度 92 分但本周只用了 3 次</p>
                <span class="severity-badge">低风险</span>
            </div>
        </div>
        
        <h2>5. 📋 失败案例 Top 10</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>场景</th>
                    <th>失败类型</th>
                    <th>次数</th>
                    <th>改进建议</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>文档处理</td>
                    <td>输出为空</td>
                    <td>12</td>
                    <td>写入后验证逻辑</td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>"""

# 保存文件
output_path = f"/root/.openclaw/workspace/reports/bot-daily-static-{datetime.now().strftime('%Y-%m-%d')}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 静态版 HTML Dashboard 已生成: {output_path}")
print(f"   文件大小: {len(html_content)} 字节")
print()
print("📌 此版本将图表嵌入为 Base64 图片，可以在飞书中直接预览")
