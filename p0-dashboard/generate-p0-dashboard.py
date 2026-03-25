#!/usr/bin/env python3
"""
P0 Dashboard 生成器 - 用户个人健康度看板
数据范围: 最近 7 天
生成时机: 每日 22:00
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import plotly.graph_objects as go
from jinja2 import Template
import json

# 配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
L3_TABLE_ID = "tbldgJxU6QUSjnf6"
SIGNALS_TABLE_ID = "tblVDILmtu1oYRTE"
L2_TABLE_ID = "tblT0I1nCFhbpvGa"

def fetch_user_data(user_owner_id):
    """
    获取用户最近 7 天的数据
    """
    # TODO: 这里需要调用 feishu_bitable_app_table_record 工具
    # 暂时返回模拟数据用于测试
    
    # 实际代码（需要在 OpenClaw 环境中调用）:
    # from openclaw_tools import feishu_bitable_app_table_record
    # 
    # seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    # today = datetime.now().strftime('%Y-%m-%d')
    # 
    # l3_data = feishu_bitable_app_table_record(
    #     action="list",
    #     app_token=APP_TOKEN,
    #     table_id=L3_TABLE_ID,
    #     filter={
    #         "conjunction": "and",
    #         "conditions": [
    #             {"field_name": "user_owner_id", "operator": "is", "value": [user_owner_id]},
    #             {"field_name": "date", "operator": "isGreaterEqual", "value": [seven_days_ago]},
    #             {"field_name": "date", "operator": "isLessEqual", "value": [today]}
    #         ]
    #     }
    # )
    
    # 模拟数据
    return {
        "latest_score": {
            "health_score": 82,
            "quality_score": 85,
            "efficiency_score": 75,
            "resource_score": 90,
            "health_rating": "🟢优秀"
        },
        "yesterday_score": {
            "health_score": 78
        },
        "trend_data": {
            "dates": ["3/18", "3/19", "3/20", "3/21", "3/22", "3/23", "3/24"],
            "correction_rates": [12, 10, 8, 9, 7, 8, 8],
            "first_resolve_rates": [70, 72, 75, 73, 77, 76, 75],
            "completion_rates": [75, 78, 80, 82, 85, 83, 80]
        },
        "scene_heatmap": {
            "scenes": ["数据分析", "文档处理", "健康诊断", "闲聊"],
            "dimensions": ["质量", "效率", "资源", "综合"],
            "scores": [
                [90, 75, 85, 85],
                [78, 65, 70, 72],
                [88, 82, 90, 87],
                [60, 70, 95, 72]
            ]
        },
        "signals": [
            {"type": "high-score-low-use", "icon": "🌟", "title": "高分低用 Bot", "count": 1, "status": "提示"},
            {"type": "low-score-high-risk", "icon": "⚠️", "title": "低分高风险 Bot", "count": 0, "status": "正常"},
            {"type": "high-risk-scene", "icon": "🔥", "title": "高风险任务场景", "count": 1, "status": "警告"}
        ],
        "failures": [
            {
                "scene": "文档处理",
                "failure_count": 3,
                "failure_reason": "prompt 未指定格式",
                "diagnosis": {
                    "problem": "用户要求\"生成一份报告\"，但未指定格式，Bot 生成的格式不符合预期，导致用户纠错 2 次。",
                    "current_prompt": "帮我生成一份报告",
                    "optimized_prompt": "帮我生成一份 Markdown 格式的报告，包含以下章节:\\n1. 背景\\n2. 数据分析\\n3. 结论",
                    "expected_effect": "减少纠错次数，提升首解率"
                }
            },
            {
                "scene": "数据分析",
                "failure_count": 2,
                "failure_reason": "模型处理慢",
                "diagnosis": {
                    "problem": "数据分析任务平均耗时 8.5 秒，超过用户耐心阈值（5 秒），导致用户中途放弃。",
                    "current_model": "claude-sonnet-4-5（慢但质量高）",
                    "recommended_model": "deepseek-reasoner（快且成本低）",
                    "expected_effect": "响应速度提升 70%，用户放弃率下降 50%"
                }
            }
        ]
    }

def generate_gauge_chart(health_score, yesterday_score):
    """模块 1: 综合健康度仪表盘"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=health_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "综合健康度", 'font': {'size': 24}},
        delta={'reference': yesterday_score, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 60], 'color': '#ffcccc'},
                {'range': [60, 75], 'color': '#ffe6cc'},
                {'range': [75, 90], 'color': '#e6f7cc'},
                {'range': [90, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"},
        height=300
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id="gauge", full_html=False)

def generate_radar_chart(quality, efficiency, resource):
    """模块 2: 三维度雷达图"""
    categories = ['质量', '效率', '资源']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[quality, efficiency, resource],
        theta=categories,
        fill='toself',
        name='今日',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="三维度健康度",
        height=350
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="radar", full_html=False)

def generate_trend_chart(dates, correction_rates, first_resolve_rates, completion_rates):
    """模块 3: 7 天趋势折线图"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=correction_rates,
        mode='lines+markers',
        name='纠错率',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=first_resolve_rates,
        mode='lines+markers',
        name='首解率',
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=completion_rates,
        mode='lines+markers',
        name='完成率',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title="7 天趋势",
        xaxis_title="日期",
        yaxis_title="百分比 (%)",
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        height=350
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="trend", full_html=False)

def generate_heatmap(scenes, dimensions, scores):
    """模块 4: 场景健康度热力图"""
    fig = go.Figure(data=go.Heatmap(
        z=scores,
        x=dimensions,
        y=scenes,
        colorscale='RdYlGn',
        text=scores,
        texttemplate="%{text}",
        textfont={"size": 16},
        colorbar=dict(title="分数")
    ))
    
    fig.update_layout(
        title="场景健康度热力图",
        xaxis_title="维度",
        yaxis_title="场景",
        height=350
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="heatmap", full_html=False)

def generate_signal_cards_html(signals):
    """模块 5: 三类智能信号卡片"""
    cards_html = '<div class="signals-container">\n'
    
    for signal in signals:
        cards_html += f'''
        <div class="signal-card {signal['type']}">
          <div class="signal-icon">{signal['icon']}</div>
          <div class="signal-title">{signal['title']}</div>
          <div class="signal-count">{signal['count']} 个</div>
          <div class="signal-status">{signal['status']}</div>
        </div>
        '''
    
    cards_html += '</div>\n'
    return cards_html

def generate_failure_table_html(failures):
    """模块 6: 失败案例表格"""
    table_html = '''
    <table class="failure-cases-table">
      <thead>
        <tr>
          <th>#</th>
          <th>场景</th>
          <th>失败次数</th>
          <th>主要原因</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
    '''
    
    for idx, case in enumerate(failures, 1):
        diagnosis = case['diagnosis']
        table_html += f'''
        <tr class="case-row" onclick="toggleDetails('case-{idx}')">
          <td>{idx}</td>
          <td>{case['scene']}</td>
          <td>{case['failure_count']}</td>
          <td>{case['failure_reason']}</td>
          <td><button>查看诊断</button></td>
        </tr>
        <tr id="case-{idx}-details" class="details-row" style="display:none">
          <td colspan="5">
            <div class="diagnosis-panel">
              <h4>🔧 诊断建议</h4>
              <div class="diagnosis-section">
                <strong>问题描述：</strong>
                <p>{diagnosis['problem']}</p>
              </div>
              <div class="diagnosis-section">
                <strong>优化方案：</strong>
                <pre>
当前 prompt（有问题）:
{diagnosis.get('current_prompt', 'N/A')}

优化后 prompt（推荐）:
{diagnosis.get('optimized_prompt', diagnosis.get('recommended_model', 'N/A'))}
                </pre>
              </div>
              <div class="diagnosis-section">
                <strong>预期效果：</strong>
                <p>{diagnosis['expected_effect']}</p>
              </div>
            </div>
          </td>
        </tr>
        '''
    
    table_html += '''
      </tbody>
    </table>
    '''
    return table_html

def generate_html_dashboard(user_data, output_path):
    """生成完整 HTML Dashboard"""
    
    # 生成图表
    gauge_html = generate_gauge_chart(
        user_data['latest_score']['health_score'],
        user_data['yesterday_score']['health_score']
    )
    
    radar_html = generate_radar_chart(
        user_data['latest_score']['quality_score'],
        user_data['latest_score']['efficiency_score'],
        user_data['latest_score']['resource_score']
    )
    
    trend_html = generate_trend_chart(
        user_data['trend_data']['dates'],
        user_data['trend_data']['correction_rates'],
        user_data['trend_data']['first_resolve_rates'],
        user_data['trend_data']['completion_rates']
    )
    
    heatmap_html = generate_heatmap(
        user_data['scene_heatmap']['scenes'],
        user_data['scene_heatmap']['dimensions'],
        user_data['scene_heatmap']['scores']
    )
    
    signal_cards_html = generate_signal_cards_html(user_data['signals'])
    failure_table_html = generate_failure_table_html(user_data['failures'])
    
    # HTML 模板
    template = Template('''
<!DOCTYPE html>
<html>
<head>
  <title>Bot Quality Monitor - P0 个人健康度看板</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.plot.ly/plotly-2.18.0.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f5f5f5;
      padding: 20px;
    }
    .container {
      max-width: 1200px;
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .header {
      text-align: center;
      margin-bottom: 10px;
      color: #333;
    }
    .subheader {
      text-align: center;
      color: #666;
      margin-bottom: 30px;
    }
    .module {
      margin: 30px 0;
      padding: 20px;
      background: #fafafa;
      border-radius: 8px;
    }
    .module h3 {
      margin-bottom: 20px;
      color: #333;
    }
    .signals-container {
      display: flex;
      gap: 20px;
      margin: 20px 0;
    }
    .signal-card {
      flex: 1;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      color: white;
    }
    .signal-card.high-score-low-use {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .signal-card.low-score-high-risk {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .signal-card.high-risk-scene {
      background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    .signal-icon {
      font-size: 48px;
      margin-bottom: 10px;
    }
    .signal-title {
      font-size: 16px;
      margin-bottom: 10px;
    }
    .signal-count {
      font-size: 32px;
      font-weight: bold;
      margin: 10px 0;
    }
    .signal-status {
      font-size: 14px;
      opacity: 0.9;
    }
    .failure-cases-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    .failure-cases-table th,
    .failure-cases-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    .failure-cases-table th {
      background: #f0f0f0;
      font-weight: bold;
    }
    .case-row {
      cursor: pointer;
      transition: background 0.2s;
    }
    .case-row:hover {
      background: #f9f9f9;
    }
    .details-row {
      background: #fafafa;
    }
    .diagnosis-panel {
      padding: 20px;
    }
    .diagnosis-section {
      margin: 15px 0;
    }
    .diagnosis-section strong {
      display: block;
      margin-bottom: 5px;
      color: #333;
    }
    .diagnosis-section pre {
      background: white;
      padding: 15px;
      border-left: 4px solid #667eea;
      border-radius: 4px;
    }
    button {
      background: #667eea;
      color: white;
      border: none;
      padding: 5px 15px;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover {
      background: #5568d3;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="header">Bot Quality Monitor - P0 个人健康度看板</h1>
    <p class="subheader">Bot: 小炸弹 💣 | 日期: {{ date }} | 综合评分: {{ health_score }} {{ rating }}</p>
    
    <!-- 模块 1: 综合健康度仪表盘 -->
    <div class="module">
      {{ gauge_chart | safe }}
    </div>
    
    <!-- 模块 2 + 3: 三维度雷达图 + 趋势图 -->
    <div class="row">
      <div class="col-md-6">
        <div class="module">
          {{ radar_chart | safe }}
        </div>
      </div>
      <div class="col-md-6">
        <div class="module">
          {{ trend_chart | safe }}
        </div>
      </div>
    </div>
    
    <!-- 模块 4: 场景健康度热力图 -->
    <div class="module">
      {{ heatmap_chart | safe }}
    </div>
    
    <!-- 模块 5: 三类智能信号卡片 -->
    <div class="module">
      <h3>三类智能信号</h3>
      {{ signal_cards | safe }}
    </div>
    
    <!-- 模块 6: 失败案例表格 -->
    <div class="module">
      <h3>失败案例 Top 10 + 诊断建议</h3>
      {{ failure_table | safe }}
    </div>
  </div>
  
  <script>
    function toggleDetails(caseId) {
      const row = document.getElementById(caseId + '-details');
      row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
    }
  </script>
</body>
</html>
    ''')
    
    # 渲染模板
    html_content = template.render(
        date=datetime.now().strftime('%Y-%m-%d'),
        health_score=user_data['latest_score']['health_score'],
        rating=user_data['latest_score']['health_rating'],
        gauge_chart=gauge_html,
        radar_chart=radar_html,
        trend_chart=trend_html,
        heatmap_chart=heatmap_html,
        signal_cards=signal_cards_html,
        failure_table=failure_table_html
    )
    
    # 保存到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ P0 Dashboard 已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    # 测试生成（使用模拟数据）
    user_owner_id = "ou_baa3525cf6cb5c0fc1ce4e26753d812d"
    
    user_data = fetch_user_data(user_owner_id)
    
    output_dir = os.path.expanduser("~/.openclaw/workspace/reports")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"p0-dashboard-{datetime.now().strftime('%Y%m%d')}.html")
    
    generate_html_dashboard(user_data, output_path)
    
    print(f"\n🎉 P0 Dashboard 生成完成!")
    print(f"📄 文件位置: {output_path}")
    print(f"🌐 在浏览器中打开: file://{output_path}")
