#!/usr/bin/env python3
"""
Bot Quality Monitor - 生成测试数据
用法:
python3 scripts/generate-demo-data.py
"""

import json
import random
from datetime import datetime, timedelta

# 测试数据配置
SCENES = ["数据分析", "文档处理", "搜索查询", "代码调试", "闲聊"]
DAYS = 7
SESSIONS_PER_DAY = 20
MESSAGES_PER_SESSION = 5

def generate_demo_data():
    """生成模拟的测试数据"""
    
    print("📈 正在生成测试数据...")
    
    # 模拟过去7天的数据
    base_date = datetime.now() - timedelta(days=DAYS)
    
    sessions = []
    messages = []
    daily_stats = []
    
    for day in range(DAYS):
        current_date = base_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        day_sessions = 0
        day_messages = 0
        day_corrections = 0
        day_completed = 0
        
        for session_idx in range(SESSIONS_PER_DAY):
            session_id = f"demo_{date_str}_{session_idx}"
            scene = random.choice(SCENES)
            
            # 会话级别的数据
            session_data = {
                "session_key": session_id,
                "start_time": current_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_time": (current_date + timedelta(minutes=random.randint(5, 30))).strftime("%Y-%m-%dT%H:%M:%S"),
                "turns": random.randint(2, 10),
                "corrections": random.randint(0, 3),
                "tool_calls": random.randint(0, 5),
                "scene": scene,
                "completed": random.choice([True, True, True, False]),
                "duration_minutes": random.randint(5, 30),
            }
            sessions.append(session_data)
            day_sessions += 1
            day_corrections += session_data["corrections"]
            if session_data["completed"]:
                day_completed += 1
            
            # 消息级别的数据
            for msg_idx in range(MESSAGES_PER_SESSION):
                msg_data = {
                    "session_key": session_id,
                    "message_id": f"demo_msg_{date_str}_{session_idx}_{msg_idx}",
                    "sender_id": "demo_user",
                    "sender_name": "测试用户",
                    "content": f"这是测试消息 {msg_idx}",
                    "msg_type": "text",
                    "create_time": (current_date + timedelta(minutes=msg_idx)).strftime("%Y-%m-%dT%H:%M:%S"),
                    "scene": scene,
                    "is_correction": random.choice([False, False, False, True]),
                    "is_error": random.choice([False, False, False, True]),
                }
                messages.append(msg_data)
                day_messages += 1
        
        # 每日统计
        stats = {
            "date": date_str,
            "total_sessions": day_sessions,
            "total_messages": day_messages,
            "completion_rate": round(day_completed / day_sessions * 100, 1) if day_sessions > 0 else 0,
            "correction_rate": round(day_corrections / day_messages * 100, 1) if day_messages > 0 else 0,
            "first_solve_rate": random.uniform(75, 95),
            "avg_turns": random.randint(4, 8),
            "error_rate": random.uniform(2, 8),
            "health_score": random.randint(70, 90),
            "health_grade": random.choice(["A", "A", "B", "B", "C"]),
        }
        daily_stats.append(stats)
    
    print(f"✅ 已生成 {len(sessions)} 个会话")
    print(f"✅ 已生成 {len(messages)} 条消息")
    print(f"✅ 已生成 {len(daily_stats)} 天每日统计")
    
    return {
        "sessions": sessions,
        "messages": messages,
        "daily_stats": daily_stats
    }

if __name__ == "__main__":
    data = generate_demo_data()
    
    # 保存到文件供其他脚本使用
    with open("/tmp/bot-quality-demo-data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("📁 测试数据已保存到 /tmp/bot-quality-demo-data.json")