#!/usr/bin/env python3
"""
P1 Dashboard 生成器 - 全局管理看板
数据范围: 最近 30 天
生成时机: 每周日 20:00
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
SKILL_ROI_TABLE_ID = "tblvmjcMrdtSFF8D"

def fetch_global_data():
    """
    获取全局数据（最近 30 天）
    """
    # TODO: 实际调用 feishu_bitable_app_table_record
    
    # 模拟数据
    return {
        "overview": {
            "total_users": 100,
            "total_bots": 250,
            "total_sessions": 10000,
            "total_messages": 50000,
            "avg_health_score": 82,
            "active_users": 75,
            "problem_bots": 12,
            "improvement_rate": 5  # +5%
        },
        "bot_ranking": [
            {"rank": 1, "bot_name": "小炸弹 💣", "owner": "陈磊", "health": 95, "correction_rate": 2, "first_resolve": 92, "sessions": 500},
            {"rank": 2, "bot_name": "数据助手", "owner": "张三", "health": 88, "correction_rate": 5, "first_resolve": 85, "sessions": 300},
            {"rank": 3, "bot_name": "文档机器人", "owner": "李四", "health": 82, "correction_rate": 8, "first_resolve": 78, "sessions": 250},
        ],
        "problem_bots": [
            {
                "bot_name": "客服Bot",
                "owner": "王五",
                "health": 45,
                "main_issue": "纠错率25%",
                "recommendation": "优化prompt",
                "severity": "high"
            }
        ],
        "skill_usage": {
            "skills": ["数据分析", "文档生成", "搜索查询", "健康诊断", "网络爬虫"],
            "call_counts": [1000, 800, 600, 400, 200],
            "success_rates": [85, 78, 92, 88, 45]
        },
        "user_activity": {
            "scene_distribution": {
                "labels": ["数据分析", "文档处理", "健康诊断", "搜索查询", "闲聊"],
                "values": [35, 28, 18, 12, 7]
            },
            "daily_active_users": {
                "dates": ["3/17", "3/18", "3/19", "3/20", "3/21", "3/22", "3/23"],
                "counts": [65, 70, 72, 68, 75, 78, 75]
            }
        }
    }

def generate_overview_cards_html(overview):
    """模块 A: 全局统计概览"""
    return f'''
    <div class="overview-cards">
      <div class="overview-card">
        <div class="card-label">总用户数</div>
        <div class="card-value">{overview['total_users']}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">总Bot数</div>
        <div class="card-value">{overview['total_bots']}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">总会话数</div>
        <div class="card-value">{overview['total_sessions']:,}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">总消息数</div>
        <div class="card-value">{overview['total_messages']:,}</div>
      </div>
    </div>
    
    <div class="overview-cards" style="margin-top: 20px">
      <div class="overview-card">
        <div class="card-label">平均健康度</div>
        <div class="card-value">{overview['avg_health_score']}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">活跃用户</div>
        <div class="card-value">{overview['active_users']}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">问题Bot数</div>
        <div class="card-value">{overview['problem_bots']}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">改进率</div>
        <div class="card-value">+{overview['improvement_rate']}%</div>
      </div>
    </div>
    '''

def generate_bot_ranking_table_html(bots):
    """模块 B: Bot 健康度排行榜"""
    table_html = '''
    <table class="ranking-table">
      <thead>
        <tr>
          <th>排名</th>
          <th>Bot昵称</th>
          <th>所有者</th>
          <th>健康度</th>
          <th>纠错率</th>
          <th>首解率</th>
          <th>会话数</th>
        </tr>
      </thead>
      <tbody>
    '''
    
    for bot in bots:
        health_color = '#ccffcc' if bot['health'] >= 90 else '#e6f7cc' if bot['health'] >= 75 else '#ffe6cc'
        medals = {1: '🥇', 2: '🥈', 3: '🥉'}
        rank_display = medals.get(bot['rank'], str(bot['rank']))
        
        table_html += f'''
        <tr>
          <td>{rank_display}</td>
          <td>{bot['bot_name']}</td>
          <td>{bot['owner']}</td>
          <td style="background: {health_color}; font-weight: bold">{bot['health']}</td>
          <td>{bot['correction_rate']}%</td>
          <td>{bot['first_resolve']}%</td>
          <td>{bot['sessions']}</td>
        </tr>
        '''
    
    table_html += '''
      </tbody>
    </table>
    '''
    return table_html

def generate_skill_usage_chart(skills, call_counts, success_rates):
    """模块 D: Skill 使用排行榜"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=skills,
        y=call_counts,
        name='调用次数',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=skills,
        y=success_rates,
        name='成功率 (%)',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(color='red', size=10),
        line=dict(width=2)
    ))
    
    fig.update_layout(
        title='Skill 使用排行榜',
        xaxis_title='Skill 名称',
        yaxis=dict(
            title=dict(text='调用次数', font=dict(color='blue')),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title=dict(text='成功率 (%)', font=dict(color='red')),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        legend=dict(x=0.01, y=0.99),
        height=400
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id="skill-usage", full_html=False)

def generate_user_activity_charts(activity_data):
    """模块 E: 用户活跃度分析"""
    # 场景分布饼图
    pie_fig = go.Figure(data=[go.Pie(
        labels=activity_data['scene_distribution']['labels'],
        values=activity_data['scene_distribution']['values'],
        hole=0.3,
        marker=dict(colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc'])
    )])
    
    pie_fig.update_layout(
        title='用户使用场景分布',
        height=350
    )
    
    # 每日活跃用户折线图
    line_fig = go.Figure()
    
    line_fig.add_trace(go.Scatter(
        x=activity_data['daily_active_users']['dates'],
        y=activity_data['daily_active_users']['counts'],
        mode='lines+markers',
        name='活跃用户数',
        line=dict(color='blue', width=3),
        fill='tonexty',
        fillcolor='rgba(0,100,255,0.2)'
    ))
    
    line_fig.update_layout(
        title='每日活跃用户数趋势',
        xaxis_title='日期',
        yaxis_title='用户数',
        height=350
    )
    
    return (
        pie_fig.to_html(include_plotlyjs=False, div_id="scene-pie", full_html=False),
        line_fig.to_html(include_plotlyjs=False, div_id="active-users", full_html=False)
    )

def generate_html_dashboard(global_data, output_path):
    """生成完整 P1 Dashboard"""
    
    overview_html = generate_overview_cards_html(global_data['overview'])
    ranking_html = generate_bot_ranking_table_html(global_data['bot_ranking'])
    skill_chart_html = generate_skill_usage_chart(
        global_data['skill_usage']['skills'],
        global_data['skill_usage']['call_counts'],
        global_data['skill_usage']['success_rates']
    )
    
    pie_html, line_html = generate_user_activity_charts(global_data['user_activity'])
    
    # HTML 模板
    template = Template('''
<!DOCTYPE html>
<html>
<head>
  <title>Bot Quality Monitor - P1 全局管理看板</title>
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
      max-width: 1400px;
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
    .overview-cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }
    .overview-card {
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .card-label {
      font-size: 14px;
      margin-bottom: 10px;
      opacity: 0.9;
    }
    .card-value {
      font-size: 32px;
      font-weight: bold;
    }
    .ranking-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    .ranking-table th,
    .ranking-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    .ranking-table th {
      background: #f0f0f0;
      font-weight: bold;
    }
    .ranking-table tr:hover {
      background: #f9f9f9;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="header">Bot Quality Monitor - P1 全局管理看板</h1>
    <p class="subheader">数据范围: {{ date_range }} | 管理员: 大少爷</p>
    
    <!-- 模块 A: 全局统计概览 -->
    <div class="module">
      <h3>📊 全局统计概览</h3>
      {{ overview_cards | safe }}
    </div>
    
    <!-- 模块 B: Bot 健康度排行榜 -->
    <div class="module">
      <h3>🏆 Bot 健康度排行榜 Top 20</h3>
      {{ ranking_table | safe }}
    </div>
    
    <!-- 模块 D: Skill 使用排行榜 -->
    <div class="module">
      {{ skill_chart | safe }}
    </div>
    
    <!-- 模块 E: 用户活跃度分析 -->
    <div class="row">
      <div class="col-md-6">
        <div class="module">
          {{ pie_chart | safe }}
        </div>
      </div>
      <div class="col-md-6">
        <div class="module">
          {{ line_chart | safe }}
        </div>
      </div>
    </div>
  </div>
</body>
</html>
    ''')
    
    # 计算日期范围
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    date_range = f"{thirty_days_ago.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}"
    
    # 渲染模板
    html_content = template.render(
        date_range=date_range,
        overview_cards=overview_html,
        ranking_table=ranking_html,
        skill_chart=skill_chart_html,
        pie_chart=pie_html,
        line_chart=line_html
    )
    
    # 保存到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ P1 Dashboard 已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    global_data = fetch_global_data()
    
    output_dir = os.path.expanduser("~/.openclaw/workspace/reports")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"p1-dashboard-{datetime.now().strftime('%Y%m%d')}.html")
    
    generate_html_dashboard(global_data, output_path)
    
    print(f"\n🎉 P1 Dashboard 生成完成!")
    print(f"📄 文件位置: {output_path}")
    print(f"🌐 在浏览器中打开: file://{output_path}")
