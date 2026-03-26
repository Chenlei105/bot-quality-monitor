#!/usr/bin/env python3
"""
Bot Quality Monitor - 生成平台视角 Demo 数据
用于展示平台级数据看板
"""

import json
import random
from datetime import datetime, timedelta

def generate_platform_demo_data():
    """生成平台视角的 Demo 数据"""
    
    # 模拟多个 Bot 的数据
    bots = [
        {"id": "bot_001", "name": "客服助手", "scene": "客户服务", "health": 78},
        {"id": "bot_002", "name": "文档小秘", "scene": "文档处理", "health": 85},
        {"id": "bot_003", "name": "代码大师", "scene": "代码调试", "health": 72},
        {"id": "bot_004", "name": "数据分析员", "scene": "数据分析", "health": 90},
        {"id": "bot_005", "name": "搜索达人", "scene": "搜索查询", "health": 68},
    ]
    
    # Skill 统计数据
    skills = [
        {"id": "docx-processor", "name": "DOCX处理", "runs": 450, "success_rate": 0.92, "roi": 85},
        {"id": "pdf-extractor", "name": "PDF提取", "runs": 320, "success_rate": 0.88, "roi": 72},
        {"id": "code-reviewer", "name": "代码审查", "runs": 280, "success_rate": 0.75, "roi": 55},
        {"id": "data-analyzer", "name": "数据分析", "runs": 520, "success_rate": 0.95, "roi": 92},
        {"id": "search-helper", "name": "搜索助手", "runs": 680, "success_rate": 0.82, "roi": 68},
    ]
    
    # 生成 7 天的每日汇总
    base_date = datetime.now() - timedelta(days=7)
    daily_stats = []
    
    for day in range(7):
        current_date = base_date + timedelta(days=day)
        daily_stats.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "total_sessions": random.randint(800, 1500),
            "total_messages": random.randint(4000, 8000),
            "avg_health": random.randint(75, 88),
            "active_bots": random.randint(15, 25),
        })
    
    result = {
        "platform_summary": {
            "total_bots": len(bots),
            "total_sessions": sum(s["total_sessions"] for s in daily_stats),
            "total_messages": sum(s["total_messages"] for s in daily_stats),
            "avg_health_score": sum(s["avg_health"] for s in daily_stats) // 7,
            "active_bots_count": daily_stats[-1]["active_bots"],
        },
        "bot_rankings": [
            {
                "rank": i + 1,
                "name": bot["name"],
                "scene": bot["scene"],
                "health": bot["health"],
                "sessions": random.randint(100, 500),
                "trend": random.choice(["up", "down", "stable"])
            }
            for i, bot in enumerate(sorted(bots, key=lambda x: x["health"], reverse=True))
        ],
        "skill_roi": [
            {
                "skill_id": s["id"],
                "skill_name": s["name"],
                "total_runs": s["runs"],
                "success_rate": s["success_rate"],
                "roi_score": s["roi"],
                "recommendation": "保留" if s["roi"] >= 70 else "优化"
            }
            for s in sorted(skills, key=lambda x: x["roi"], reverse=True)
        ],
        "daily_trend": daily_stats,
        "risk_alerts": [
            {"type": "low_usage", "bot": "搜索达人", "reason": "健康度高但使用率低"},
            {"type": "high_failure", "bot": "代码大师", "reason": "失败率偏高"},
        ]
    }
    
    return result

def format_platform_report(data):
    """格式化平台视角报告"""
    summary = data["platform_summary"]
    bots = data["bot_rankings"]
    skills = data["skill_roi"]
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 平台健康度概览 - Demo 示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 平台统计
├─ Bot 总数: {summary['total_bots']} 个
├─ 总会话数: {summary['total_sessions']:,}
├─ 总消息数: {summary['total_messages']:,}
├─ 平均健康度: {summary['avg_health_score']} 分
└─ 活跃 Bot: {summary['active_bots_count']} 个

━━━━━━━━━━ Bot 排行榜 ━━━━━━━━━━
"""
    
    for bot in bots[:5]:
        trend_emoji = "📈" if bot["trend"] == "up" else "📉" if bot["trend"] == "down" else "➡️"
        report += f"""
{bot['rank']}. {bot['name']} ({bot['scene']})
   健康度: {bot['health']} 分 {trend_emoji}
   会话数: {bot['sessions']}
"""
    
    report += """
━━━━━━━━━━ Skill ROI 排行榜 ━━━━━━━━━━
"""
    
    for s in skills:
        rec = "✅" if s["recommendation"] == "保留" else "🔧"
        report += f"""
• {s['skill_name']}
   运行次数: {s['total_runs']} | 成功率: {s['success_rate']*100:.0f}% | ROI: {s['roi_score']} {rec}
"""
    
    report += """
━━━━━━━━━━ 风险预警 ━━━━━━━━━━
"""
    
    for alert in data["risk_alerts"]:
        emoji = "🟢" if alert["type"] == "low_usage" else "🔴"
        report += f"""
{emoji} {alert['bot']}: {alert['reason']}
"""
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 这是 Demo 示例，展示平台级数据看板的样式
    实际数据会根据你的 Bot 运行情况自动生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report.strip()

if __name__ == "__main__":
    data = generate_platform_demo_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("\n" + "="*50)
    print(format_platform_report(data))