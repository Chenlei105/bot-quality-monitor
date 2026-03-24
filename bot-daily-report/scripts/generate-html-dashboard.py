#!/usr/bin/env python3
"""
HTML Dashboard 生成脚本 v2.1.1
生成 Plotly 交互式可视化看板

包含模块:
1. 📊 综合健康度仪表盘 (Plotly Gauge Chart)
2. 📈 7 天趋势折线图 (纠错率/首解率/任务完成率)
3. 🎨 场景健康度热力图 (行=场景，列=指标)
4. 🔔 三类信号卡片 (从 L3_Signal_Alerts 读取)
5. 📋 失败案例 Top 10 (从 L2 筛选 failed)
"""

import os
import json
from datetime import datetime, timedelta

def generate_html_dashboard(data):
    """
    生成完整的 HTML Dashboard
    
    Args:
        data: 包含以下键的字典
            - health_score: 综合健康度 (0-100)
            - trend_data: 7天趋势数据
            - heatmap_data: 场景健康度矩阵
            - signals: 三类信号列表
            - failed_cases: 失败案例 Top 10
    """
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 综合健康度仪表盘
    gauge_html = f"""
    <div id="gauge-chart"></div>
    <script>
        var gaugeData = [{{
            type: "indicator",
            mode: "gauge+number+delta",
            value: {data.get('health_score', 0)},
            title: {{ text: "综合健康度", font: {{ size: 24 }} }},
            delta: {{ reference: 80, increasing: {{ color: "green" }} }},
            gauge: {{
                axis: {{ range: [null, 100], tickwidth: 1, tickcolor: "darkblue" }},
                bar: {{ color: "{get_gauge_color(data.get('health_score', 0))}" }},
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "gray",
                steps: [
                    {{ range: [0, 60], color: "#ffebee" }},
                    {{ range: [60, 75], color: "#fff3e0" }},
                    {{ range: [75, 90], color: "#e8f5e9" }},
                    {{ range: [90, 100], color: "#c8e6c9" }}
                ],
                threshold: {{
                    line: {{ color: "red", width: 4 }},
                    thickness: 0.75,
                    value: 80
                }}
            }}
        }}]];
        
        var gaugeLayout = {{ 
            width: 500, 
            height: 400,
            margin: {{ t: 50, r: 25, l: 25, b: 25 }},
            font: {{ color: "darkblue", family: "Arial" }}
        }};
        
        Plotly.newPlot('gauge-chart', gaugeData, gaugeLayout);
    </script>
    """
    
    # 2. 7 天趋势折线图
    trend = data.get('trend_data', {})
    trend_html = f"""
    <div id="trend-chart"></div>
    <script>
        var trace1 = {{
            x: {json.dumps(trend.get('dates', []))},
            y: {json.dumps(trend.get('correction_rates', []))},
            mode: 'lines+markers',
            name: '纠错率 (%)',
            line: {{ color: 'red', width: 2 }},
            marker: {{ size: 8 }}
        }};
        
        var trace2 = {{
            x: {json.dumps(trend.get('dates', []))},
            y: {json.dumps(trend.get('first_resolve_rates', []))},
            mode: 'lines+markers',
            name: '首解率 (%)',
            line: {{ color: 'green', width: 2 }},
            marker: {{ size: 8 }}
        }};
        
        var trace3 = {{
            x: {json.dumps(trend.get('dates', []))},
            y: {json.dumps(trend.get('completion_rates', []))},
            mode: 'lines+markers',
            name: '任务完成率 (%)',
            line: {{ color: 'blue', width: 2 }},
            marker: {{ size: 8 }}
        }};
        
        var trendLayout = {{
            title: '7 天趋势',
            xaxis: {{ title: '日期' }},
            yaxis: {{ title: '百分比 (%)' }},
            hovermode: 'x unified'
        }};
        
        Plotly.newPlot('trend-chart', [trace1, trace2, trace3], trendLayout);
    </script>
    """
    
    # 3. 场景健康度热力图
    heatmap = data.get('heatmap_data', {})
    heatmap_html = f"""
    <div id="heatmap-chart"></div>
    <script>
        var heatmapData = [{{
            z: {json.dumps(heatmap.get('values', [[80, 75, 90]]))},
            x: {json.dumps(heatmap.get('metrics', ['质量', '效率', '资源']))},
            y: {json.dumps(heatmap.get('scenes', ['数据分析', '文档处理', '健康诊断']))},
            type: 'heatmap',
            colorscale: 'RdYlGn',
            reversescale: false,
            showscale: true,
            hovertemplate: '场景: %{{y}}<br>指标: %{{x}}<br>得分: %{{z}}<extra></extra>'
        }}]];
        
        var heatmapLayout = {{
            title: '场景健康度热力图',
            xaxis: {{ title: '指标维度' }},
            yaxis: {{ title: '场景分类' }}
        }};
        
        Plotly.newPlot('heatmap-chart', heatmapData, heatmapLayout);
    </script>
    """
    
    # 4. 三类信号卡片
    signals = data.get('signals', [])
    signals_html = "<div class='signals-container'>"
    for signal in signals:
        severity_class = signal.get('severity', 'low')
        signals_html += f"""
        <div class="signal-card signal-{severity_class}">
            <h3>{get_signal_icon(signal.get('type', ''))} {signal.get('type', '未知信号')}</h3>
            <p>{signal.get('message', '')}</p>
            <span class="severity-badge">{get_severity_label(severity_class)}</span>
        </div>
        """
    signals_html += "</div>"
    
    # 5. 失败案例 Top 10
    failed_cases = data.get('failed_cases', [])
    failed_html = """
    <table class="failed-table">
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
    """
    for i, case in enumerate(failed_cases[:10], 1):
        failed_html += f"""
        <tr>
            <td>{i}</td>
            <td>{case.get('scene', '')}</td>
            <td>{case.get('failure_type', '')}</td>
            <td>{case.get('count', 0)}</td>
            <td>{case.get('suggestion', '')}</td>
        </tr>
        """
    failed_html += """
        </tbody>
    </table>
    """
    
    # 组装完整 HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot 质量日报 Dashboard · {today}</title>
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background: #f5f5f5;
                padding: 20px;
                color: #333;
            }}
            
            .container {{
                max-width: 1400px;
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
            
            .section {{
                margin-bottom: 40px;
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
            }}
            
            .signal-low {{
                background: #e8f5e9;
                border-color: #4caf50;
            }}
            
            .signal-medium {{
                background: #fff3e0;
                border-color: #ff9800;
            }}
            
            .signal-high {{
                background: #ffebee;
                border-color: #f44336;
            }}
            
            .signal-critical {{
                background: #fce4ec;
                border-color: #e91e63;
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
                margin-top: 10px;
            }}
            
            .failed-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            
            .failed-table th,
            .failed-table td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            
            .failed-table th {{
                background: #f5f5f5;
                font-weight: 600;
            }}
            
            .failed-table tr:hover {{
                background: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Bot 质量日报 Dashboard · {today}</h1>
            
            <div class="section">
                <h2>1. 综合健康度仪表盘</h2>
                {gauge_html}
            </div>
            
            <div class="section">
                <h2>2. 📈 7 天趋势</h2>
                {trend_html}
            </div>
            
            <div class="section">
                <h2>3. 🎨 场景健康度热力图</h2>
                {heatmap_html}
            </div>
            
            <div class="section">
                <h2>4. 🔔 三类智能信号</h2>
                {signals_html}
            </div>
            
            <div class="section">
                <h2>5. 📋 失败案例 Top 10</h2>
                {failed_html}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def get_gauge_color(score):
    """根据得分返回仪表盘颜色"""
    if score >= 90:
        return "#4caf50"
    elif score >= 75:
        return "#8bc34a"
    elif score >= 60:
        return "#ff9800"
    else:
        return "#f44336"

def get_signal_icon(signal_type):
    """返回信号图标"""
    icons = {
        "high_score_low_use": "🟢",
        "low_score_high_risk": "🔴",
        "high_risk_task": "⚠️"
    }
    return icons.get(signal_type, "📍")

def get_severity_label(severity):
    """返回严重程度标签"""
    labels = {
        "low": "低风险",
        "medium": "中风险",
        "high": "高风险",
        "critical": "严重"
    }
    return labels.get(severity, "未知")

def main():
    """主函数"""
    print("=" * 60)
    print("📊 HTML Dashboard 生成脚本 v2.1.1")
    print("=" * 60)
    
    # 示例数据
    sample_data = {
        'health_score': 82,
        'trend_data': {
            'dates': ['03-18', '03-19', '03-20', '03-21', '03-22', '03-23', '03-24'],
            'correction_rates': [5, 4, 3, 4, 3, 2, 3],
            'first_resolve_rates': [75, 78, 80, 83, 85, 87, 88],
            'completion_rates': [80, 82, 85, 87, 88, 90, 91]
        },
        'heatmap_data': {
            'scenes': ['数据分析', '文档处理', '健康诊断', '技能管理'],
            'metrics': ['质量', '效率', '资源'],
            'values': [
                [88, 75, 90],
                [75, 80, 85],
                [58, 60, 70],
                [90, 85, 95]
            ]
        },
        'signals': [
            {
                'type': 'high_score_low_use',
                'message': '小炸弹健康度 92 分但本周只用了 3 次',
                'severity': 'low'
            }
        ],
        'failed_cases': [
            {'scene': '文档处理', 'failure_type': '输出为空', 'count': 12, 'suggestion': '写入后验证逻辑'}
        ]
    }
    
    html = generate_html_dashboard(sample_data)
    
    output_dir = os.path.expanduser('~/.openclaw/workspace/reports')
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    output_path = os.path.join(output_dir, f'bot-daily-{today}.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML Dashboard 已生成: {output_path}")
    print(f"   文件大小: {len(html)} 字节")
    print("=" * 60)

if __name__ == "__main__":
    main()
