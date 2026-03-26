#!/usr/bin/env python3
"""
P2 Dashboard 生成器 - 历史归档看板
数据范围: 90 天 ~ 全年
生成时机: 每月/季度/年度
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

def fetch_archive_data(report_type='monthly'):
    """
    获取归档数据
    report_type: monthly/quarterly/yearly
    """
    # TODO: 实际调用 feishu_bitable_app_table_record
    
    # 模拟数据
    return {
        "report_type": report_type,
        "bot_growth_curve": {
            "bots": ["小炸弹 💣", "数据助手", "文档机器人"],
            "months": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "scores": {
                "小炸弹 💣": [75, 78, 82, 85, 88, 91],
                "数据助手": [70, 72, 75, 78, 80, 82],
                "文档机器人": [65, 68, 70, 72, 75, 78]
            }
        },
        "quarterly_comparison": {
            "quarters": ["Q1", "Q2"],
            "avg_scores": [75, 82],
            "growth_rates": [None, 9.3]
        },
        "comparison_stats": {
            "month_vs_last": {"change": 5, "from": 82, "to": 87},
            "quarter_vs_last": {"change": 8, "from": 78, "to": 86},
            "year_vs_last": {"change": 12, "from": 70, "to": 82}
        },
        "leaderboard": {
            "most_popular_skill": {"name": "数据分析", "count": 10000, "success_rate": 85},
            "most_stable_bot": {"name": "小炸弹 💣", "avg_health": 92, "volatility": 2},
            "fastest_growth_user": {"name": "张三", "duration": "3个月", "improvement": 30}
        }
    }

def generate_bot_growth_curve(data):
    """模块 B: Bot 成长曲线"""
    fig = go.Figure()
    
    for bot in data['bots']:
        fig.add_trace(go.Scatter(
            x=data['months'],
            y=data['scores'][bot],
            mode='lines+markers',
            name=bot,
            line=dict(width=2),
            hovertemplate='<b>%{fullData.name}</b><br>月份: %{x}<br>健康度: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Bot 成长曲线(全年健康度趋势)',
        xaxis_title='月份',
        yaxis_title='健康度得分',
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
        height=400
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id="growth", full_html=False)

def generate_quarterly_comparison(data):
    """模块 C: 季度健康度对比"""
    fig = go.Figure()
    
    # 柱状图
    fig.add_trace(go.Bar(
        x=data['quarters'],
        y=data['avg_scores'],
        name='平均健康度',
        marker_color=['#ffcc99', '#e6f7cc'],
        text=data['avg_scores'],
        textposition='outside'
    ))
    
    # 折线图(环比增长率)
    if len(data['growth_rates']) > 1:
        fig.add_trace(go.Scatter(
            x=data['quarters'][1:],
            y=[r for r in data['growth_rates'][1:] if r is not None],
            name='环比增长率(%)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='red', width=2, dash='dash'),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title='季度健康度对比',
        xaxis_title='季度',
        yaxis=dict(
            title=dict(text='平均健康度'),
            range=[0, 100]
        ),
        yaxis2=dict(
            title=dict(text='环比增长率(%)'),
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    return fig.to_html(include_plotlyjs=False, div_id="quarterly", full_html=False)

def generate_comparison_cards_html(stats):
    """模块 F: 同比/环比健康度变化"""
    month_change = stats['month_vs_last']
    quarter_change = stats['quarter_vs_last']
    year_change = stats['year_vs_last']
    
    return f'''
    <div class="comparison-cards">
      <div class="comparison-card">
        <div class="card-header">本月 vs 上月</div>
        <div class="card-body">
          <span class="value change-up">+{month_change['change']} ↑</span>
          <span class="detail">({month_change['from']} → {month_change['to']})</span>
        </div>
      </div>
      
      <div class="comparison-card">
        <div class="card-header">本季 vs 上季</div>
        <div class="card-body">
          <span class="value change-up">+{quarter_change['change']} ↑</span>
          <span class="detail">({quarter_change['from']} → {quarter_change['to']})</span>
        </div>
      </div>
      
      <div class="comparison-card">
        <div class="card-header">今年 vs 去年</div>
        <div class="card-body">
          <span class="value change-up">+{year_change['change']} ↑</span>
          <span class="detail">({year_change['from']} → {year_change['to']})</span>
        </div>
      </div>
    </div>
    '''

def generate_leaderboard_html(leaderboard):
    """模块 H: 年度 Top 10 榜单"""
    return f'''
    <div class="leaderboard-section">
      <div class="leaderboard">
        <h4>🔥 最受欢迎 Skill</h4>
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>Skill 名称</th>
              <th>调用次数</th>
              <th>成功率</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🥇 1</td>
              <td>{leaderboard['most_popular_skill']['name']}</td>
              <td>{leaderboard['most_popular_skill']['count']:,}</td>
              <td>{leaderboard['most_popular_skill']['success_rate']}%</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="leaderboard">
        <h4>💎 最稳定 Bot</h4>
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>Bot 昵称</th>
              <th>平均健康度</th>
              <th>波动幅度</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🥇 1</td>
              <td>{leaderboard['most_stable_bot']['name']}</td>
              <td>{leaderboard['most_stable_bot']['avg_health']}</td>
              <td>±{leaderboard['most_stable_bot']['volatility']}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="leaderboard">
        <h4>🚀 最快成长用户</h4>
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>用户</th>
              <th>成长周期</th>
              <th>健康度提升</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🥇 1</td>
              <td>{leaderboard['fastest_growth_user']['name']}</td>
              <td>{leaderboard['fastest_growth_user']['duration']}</td>
              <td>+{leaderboard['fastest_growth_user']['improvement']}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    '''

def generate_html_dashboard(archive_data, output_path):
    """生成完整 P2 Dashboard"""
    
    # 生成图表
    growth_curve_html = generate_bot_growth_curve(archive_data['bot_growth_curve'])
    quarterly_comparison_html = generate_quarterly_comparison(archive_data['quarterly_comparison'])
    comparison_cards_html = generate_comparison_cards_html(archive_data['comparison_stats'])
    leaderboard_html = generate_leaderboard_html(archive_data['leaderboard'])
    
    # HTML 模板
    template = Template('''
<!DOCTYPE html>
<html>
<head>
  <title>Bot Quality Monitor - P2 历史归档看板</title>
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
    .comparison-cards {
      display: flex;
      gap: 20px;
      margin: 20px 0;
    }
    .comparison-card {
      flex: 1;
      padding: 20px;
      border-radius: 8px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-align: center;
    }
    .card-header {
      font-size: 14px;
      margin-bottom: 10px;
    }
    .card-body .value {
      font-size: 32px;
      font-weight: bold;
    }
    .change-up {
      color: #00ff00;
    }
    .detail {
      display: block;
      font-size: 14px;
      margin-top: 5px;
      opacity: 0.8;
    }
    .leaderboard-section {
      margin-top: 20px;
    }
    .leaderboard {
      margin: 20px 0;
    }
    .leaderboard h4 {
      color: #333;
      margin-bottom: 10px;
    }
    .leaderboard table {
      width: 100%;
      border-collapse: collapse;
    }
    .leaderboard th,
    .leaderboard td {
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    .leaderboard th {
      background: #f0f0f0;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="header">Bot Quality Monitor - P2 历史归档看板</h1>
    <p class="subheader">数据范围: {{ date_range }} | {{ report_type_display }}</p>
    
    <!-- 模块 B: Bot 成长曲线 -->
    <div class="module">
      {{ growth_curve | safe }}
    </div>
    
    <!-- 模块 C: 季度健康度对比 -->
    <div class="module">
      {{ quarterly_comparison | safe }}
    </div>
    
    <!-- 模块 F: 同比/环比健康度变化 -->
    <div class="module">
      <h3>📈 同比/环比健康度变化</h3>
      {{ comparison_cards | safe }}
    </div>
    
    <!-- 模块 H: 年度 Top 10 榜单 -->
    <div class="module">
      <h3>🏆 年度 Top 10 榜单</h3>
      {{ leaderboard | safe }}
    </div>
  </div>
</body>
</html>
    ''')
    
    # 确定日期范围和报告类型
    today = datetime.now()
    if archive_data['report_type'] == 'monthly':
        date_range = (today.replace(day=1) - timedelta(days=1)).strftime('%Y年%m月')
        report_type_display = "月度归档报告"
    elif archive_data['report_type'] == 'quarterly':
        date_range = f"{today.year}年 Q{(today.month-1)//3 + 1}"
        report_type_display = "季度总结报告"
    else:
        date_range = f"{today.year}年"
        report_type_display = "年度总结报告"
    
    # 渲染模板
    html_content = template.render(
        date_range=date_range,
        report_type_display=report_type_display,
        growth_curve=growth_curve_html,
        quarterly_comparison=quarterly_comparison_html,
        comparison_cards=comparison_cards_html,
        leaderboard=leaderboard_html
    )
    
    # 保存到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ P2 Dashboard 已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='生成 P2 历史归档 Dashboard')
    parser.add_argument('--type', choices=['monthly', 'quarterly', 'yearly'], default='monthly',
                       help='报告类型 (monthly/quarterly/yearly)')
    
    args = parser.parse_args()
    
    archive_data = fetch_archive_data(args.type)
    
    output_dir = os.path.expanduser("~/.openclaw/workspace/reports")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"p2-dashboard-{args.type}-{datetime.now().strftime('%Y%m%d')}.html")
    
    generate_html_dashboard(archive_data, output_path)
    
    print(f"\n🎉 P2 Dashboard 生成完成!")
    print(f"📄 文件位置: {output_path}")
    print(f"🌐 在浏览器中打开: file://{output_path}")
