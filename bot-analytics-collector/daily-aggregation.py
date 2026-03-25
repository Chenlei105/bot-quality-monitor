#!/usr/bin/env python3
"""
每日指标汇总脚本
从 L2_会话汇总表聚合数据，生成 L3_每日指标汇总

执行时间：每日 23:00（在日报生成前）
"""

import sys
import os
from datetime import datetime, timedelta
import json

# 配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
L2_TABLE_ID = "tblT0I1nCFhbpvGa"  # L2_会话汇总
L3_TABLE_ID = "tbldgJxU6QUSjnf6"  # L3_每日指标汇总

def log(message):
    """输出日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def aggregate_daily_metrics():
    """
    聚合今日指标
    
    从 L2 表读取今天的所有会话记录，按 user_owner_id + bot_id 分组聚合
    """
    log("开始聚合今日指标...")
    
    # 计算日期范围（今天 00:00 到 23:59）
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    today_ts = int(today.timestamp() * 1000)
    tomorrow_ts = int(tomorrow.timestamp() * 1000)
    
    today_str = today.strftime('%Y-%m-%d')
    
    log(f"聚合日期: {today_str}")
    log(f"时间范围: {today_ts} ~ {tomorrow_ts}")
    
    # TODO: 调用 feishu_bitable_app_table_record 读取今日数据
    # 
    # l2_records = feishu_bitable_app_table_record(
    #     action="list",
    #     app_token=APP_TOKEN,
    #     table_id=L2_TABLE_ID,
    #     filter={
    #         "conjunction": "and",
    #         "conditions": [
    #             {"field_name": "session_start", "operator": "isGreaterEqual", "value": [today_ts]},
    #             {"field_name": "session_start", "operator": "isLess", "value": [tomorrow_ts]}
    #         ]
    #     },
    #     page_size=500
    # )
    
    # 模拟数据（实际应从 L2 表读取）
    l2_records = {
        "records": [
            {
                "fields": {
                    "用户所有者ID": "ou_baa3525cf6cb5c0fc1ce4e26753d812d",
                    "bot_id": "cli_a922b6c0b8b89bd1",
                    "bot_name": "小炸弹 💣",
                    "scene_type": "数据分析",
                    "turn_count": 2,
                    "correction_count": 0,
                    "completion_status": "completed",
                    "first_resolve": True,
                    "satisfaction_signal": "positive"
                }
            }
        ]
    }
    
    # 按 user_owner_id + bot_id 分组聚合
    aggregated = {}
    
    for record in l2_records['records']:
        fields = record['fields']
        
        user_id = fields.get('用户所有者ID', 'unknown')
        bot_id = fields.get('bot_id', 'unknown')
        key = f"{user_id}:{bot_id}"
        
        if key not in aggregated:
            aggregated[key] = {
                "user_owner_id": user_id,
                "bot_id": bot_id,
                "bot_name": fields.get('bot_name', ''),
                "date": today_str,
                "session_count": 0,
                "total_turns": 0,
                "total_corrections": 0,
                "completed_count": 0,
                "failed_count": 0,
                "first_resolve_count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "scene_distribution": {}
            }
        
        agg = aggregated[key]
        
        # 累加指标
        agg['session_count'] += 1
        agg['total_turns'] += fields.get('turn_count', 0)
        agg['total_corrections'] += fields.get('correction_count', 0)
        
        if fields.get('completion_status') == 'completed':
            agg['completed_count'] += 1
        elif fields.get('completion_status') == 'failed':
            agg['failed_count'] += 1
        
        if fields.get('first_resolve'):
            agg['first_resolve_count'] += 1
        
        if fields.get('satisfaction_signal') == 'positive':
            agg['positive_count'] += 1
        elif fields.get('satisfaction_signal') == 'negative':
            agg['negative_count'] += 1
        
        # 场景分布
        scene = fields.get('scene_type', '其他')
        agg['scene_distribution'][scene] = agg['scene_distribution'].get(scene, 0) + 1
    
    # 计算衍生指标
    for key, agg in aggregated.items():
        agg['correction_rate'] = (
            agg['total_corrections'] / agg['total_turns'] 
            if agg['total_turns'] > 0 else 0
        )
        agg['completion_rate'] = (
            agg['completed_count'] / agg['session_count'] 
            if agg['session_count'] > 0 else 0
        )
        agg['first_resolve_rate'] = (
            agg['first_resolve_count'] / agg['session_count'] 
            if agg['session_count'] > 0 else 0
        )
        
        # 三维度得分
        quality_score = (1 - agg['correction_rate']) * 50 + agg['first_resolve_rate'] * 50
        efficiency_score = min(100, (agg['total_turns'] / agg['session_count']) * 20) if agg['session_count'] > 0 else 0
        resource_score = 80  # 简化计算，实际应根据 token 消耗
        
        agg['quality_score'] = round(quality_score, 2)
        agg['efficiency_score'] = round(efficiency_score, 2)
        agg['resource_score'] = round(resource_score, 2)
        
        # 健康度总分
        agg['health_score'] = round(
            quality_score * 0.4 + efficiency_score * 0.3 + resource_score * 0.3,
            2
        )
        
        # 健康度评级
        if agg['health_score'] >= 90:
            agg['health_rating'] = '优秀'
        elif agg['health_score'] >= 75:
            agg['health_rating'] = '良好'
        elif agg['health_score'] >= 60:
            agg['health_rating'] = '及格'
        else:
            agg['health_rating'] = '需改进'
    
    log(f"聚合完成: {len(aggregated)} 条记录")
    
    # TODO: 写入 L3 表
    # for key, agg in aggregated.items():
    #     feishu_bitable_app_table_record(
    #         action="create",
    #         app_token=APP_TOKEN,
    #         table_id=L3_TABLE_ID,
    #         fields={
    #             "date": agg['date'],
    #             "user_owner_id": agg['user_owner_id'],
    #             "bot_id": agg['bot_id'],
    #             "bot_name": agg['bot_name'],
    #             "session_count": agg['session_count'],
    #             "correction_rate": agg['correction_rate'],
    #             "completion_rate": agg['completion_rate'],
    #             "first_resolve_rate": agg['first_resolve_rate'],
    #             "quality_score": agg['quality_score'],
    #             "efficiency_score": agg['efficiency_score'],
    #             "resource_score": agg['resource_score'],
    #             "health_score": agg['health_score'],
    #             "health_rating": agg['health_rating']
    #         }
    #     )
    
    log("✅ 每日指标汇总完成")
    
    return aggregated

def main():
    """
    主流程
    """
    log("=" * 60)
    log("Bot Quality Monitor - 每日指标汇总任务开始")
    log("=" * 60)
    
    try:
        aggregated = aggregate_daily_metrics()
        
        # 打印汇总结果
        for key, agg in aggregated.items():
            log(f"\n用户: {agg['user_owner_id']}")
            log(f"  Bot: {agg['bot_name']}")
            log(f"  会话数: {agg['session_count']}")
            log(f"  健康度: {agg['health_score']} ({agg['health_rating']})")
            log(f"  纠错率: {agg['correction_rate']*100:.1f}%")
            log(f"  完成率: {agg['completion_rate']*100:.1f}%")
            log(f"  首解率: {agg['first_resolve_rate']*100:.1f}%")
        
        log("=" * 60)
        log("✅ 每日指标汇总任务完成")
        log("=" * 60)
        
    except Exception as e:
        log(f"❌ 每日指标汇总任务失败: {str(e)}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
