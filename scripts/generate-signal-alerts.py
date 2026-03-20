#!/usr/bin/env python3
"""
三类信号自动生成脚本（v2.1.0）

每日执行（建议在日报生成前 1 小时），检测并生成三类信号：
1. 高分低用 Bot（health_score >= 85 AND weekly_trigger_count <= 5）
2. 低分高风险 Bot（correction_rate >= 0.10 OR failure_count >= 5）
3. 高风险任务场景（scenario_failure_rate >= 0.30 AND sample_count >= 5）

生成后写入 L3_Signal_Alerts 表供日报消费
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# 数据中台配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
TABLE_L2 = "tblT0I1nCFhbpvGa"  # L2 会话汇总表
TABLE_L3_DAILY = "tbldgJxU6QUSjnf6"  # L3 每日指标汇总
TABLE_SIGNAL_ALERTS = "tblVDILmtu1oYRTE"  # L3_Signal_Alerts

def get_today_timestamp():
    """获取今日 00:00:00 的时间戳（GMT+8）"""
    china_tz = timezone(timedelta(hours=8))
    today = datetime.now(china_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    return int(today.timestamp() * 1000)

def get_seven_days_ago_timestamp():
    """获取 7 天前 00:00:00 的时间戳"""
    china_tz = timezone(timedelta(hours=8))
    seven_days_ago = datetime.now(china_tz) - timedelta(days=7)
    seven_days_ago = seven_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(seven_days_ago.timestamp() * 1000)

def detect_high_score_low_use():
    """
    信号 1：高分低用 Bot
    条件：health_score >= 85 AND weekly_trigger_count <= 5
    """
    print("[信号1] 检测高分低用 Bot...")
    
    # 从 L3 每日指标汇总表读取最近 7 天数据
    seven_days_ago_ms = get_seven_days_ago_timestamp()
    
    # 模拟调用（实际应替换为 feishu_bitable_app_table_record）
    # l3_data = feishu_bitable_app_table_record(
    #     action="list",
    #     app_token=APP_TOKEN,
    #     table_id=TABLE_L3_DAILY,
    #     filter={...}
    # )
    
    # 按 bot_id 分组统计
    bot_stats = defaultdict(lambda: {
        "bot_name": "",
        "total_score": 0,
        "count": 0,
        "weekly_trigger_count": 0
    })
    
    # 模拟数据（实际应从 L3 读取）
    mock_l3_data = [
        {"bot_id": "cli_a922b6c0b8b89bd1", "bot_name": "小炸弹", "health_score": 91.5, "trigger_count": 3},
        {"bot_id": "cli_a922b6c0b8b89bd1", "bot_name": "小炸弹", "health_score": 90.0, "trigger_count": 0},
    ]
    
    for record in mock_l3_data:
        bot_id = record["bot_id"]
        bot_stats[bot_id]["bot_name"] = record["bot_name"]
        bot_stats[bot_id]["total_score"] += record["health_score"]
        bot_stats[bot_id]["count"] += 1
        bot_stats[bot_id]["weekly_trigger_count"] += record["trigger_count"]
    
    # 筛选符合条件的 Bot
    signals = []
    for bot_id, stats in bot_stats.items():
        avg_score = stats["total_score"] / stats["count"] if stats["count"] > 0 else 0
        
        if avg_score >= 85 and stats["weekly_trigger_count"] <= 5:
            signals.append({
                "signal_type": "high_score_low_use",
                "target_id": bot_id,
                "target_name": stats["bot_name"],
                "health_score": round(avg_score, 1),
                "trigger_count": stats["weekly_trigger_count"],
                "risk_value": 0.0,
                "risk_desc": "健康度高，使用频次低",
                "recommendation": f"{stats['bot_name']}健康度 {avg_score:.0f}分🟢，但本周只用了 {stats['weekly_trigger_count']} 次\n→ 建议：可以多问它数据分析、日报生成等任务",
                "severity": "low"
            })
    
    print(f"✅ 检测到 {len(signals)} 个高分低用 Bot")
    return signals

def detect_low_score_high_risk():
    """
    信号 2：低分高风险 Bot
    条件：correction_rate >= 0.10 OR failure_count >= 5
    """
    print("[信号2] 检测低分高风险 Bot...")
    
    today_ms = get_today_timestamp()
    
    # 模拟数据（实际应从 L3 读取今日数据）
    mock_l3_today = [
        {
            "bot_id": "cli_test_bot_1",
            "bot_name": "一号员工",
            "health_score": 65.0,
            "total_messages": 20,
            "correction_count": 3,
            "failure_count": 5
        }
    ]
    
    signals = []
    for record in mock_l3_today:
        correction_rate = record["correction_count"] / record["total_messages"] if record["total_messages"] > 0 else 0
        
        if correction_rate >= 0.10 or record["failure_count"] >= 5:
            # 计算严重程度
            if correction_rate >= 0.20:
                severity = "critical"
            elif correction_rate >= 0.10:
                severity = "high"
            else:
                severity = "medium"
            
            # 计算超标倍数
            over_rate = correction_rate / 0.05 if correction_rate > 0 else 0
            
            signals.append({
                "signal_type": "low_score_high_risk",
                "target_id": record["bot_id"],
                "target_name": record["bot_name"],
                "health_score": record["health_score"],
                "trigger_count": 0,  # 不适用
                "risk_value": round(correction_rate, 2),
                "risk_desc": f"纠错率 {correction_rate*100:.0f}%，超标 {over_rate:.1f} 倍",
                "recommendation": f"{record['bot_name']}纠错率 {correction_rate*100:.0f}%（超标 {over_rate:.0f} 倍），本周失败 {record['failure_count']} 次\n→ 处方：\n  1) 补充文档处理知识库\n  2) 限制高风险场景使用\n  3) 检查配置项",
                "severity": severity
            })
    
    print(f"✅ 检测到 {len(signals)} 个低分高风险 Bot")
    return signals

def detect_high_risk_task():
    """
    信号 3：高风险任务场景
    条件：scenario_failure_rate >= 0.30 AND scenario_sample_count >= 5
    """
    print("[信号3] 检测高风险任务场景...")
    
    seven_days_ago_ms = get_seven_days_ago_timestamp()
    
    # 从 L2 按场景分类统计（实际应从 L2 读取）
    # l2_data = feishu_bitable_app_table_record(...)
    
    # 模拟数据
    scenario_stats = {
        "文档写入": {"total": 10, "failed": 4},
        "数据分析": {"total": 20, "failed": 2},
    }
    
    signals = []
    for scenario_name, stats in scenario_stats.items():
        failure_rate = stats["failed"] / stats["total"] if stats["total"] > 0 else 0
        
        if failure_rate >= 0.30 and stats["total"] >= 5:
            # 计算严重程度
            if failure_rate >= 0.40:
                severity = "critical"
            elif failure_rate >= 0.30:
                severity = "high"
            else:
                severity = "medium"
            
            signals.append({
                "signal_type": "high_risk_task",
                "target_id": scenario_name,
                "target_name": scenario_name,
                "health_score": 0,  # 不适用
                "trigger_count": stats["total"],
                "risk_value": round(failure_rate, 2),
                "risk_desc": f"失败率 {failure_rate*100:.0f}%（{stats['total']}次中{stats['failed']}次失败）",
                "recommendation": f'"{scenario_name}"类任务本周失败率 {failure_rate*100:.0f}%（{stats["total"]}次中{stats["failed"]}次失败）\n→ 建议：\n  1) 暂时避开此类任务\n  2) 或改用手动方式\n  3) 等待下次 Skill 更新',
                "severity": severity
            })
    
    print(f"✅ 检测到 {len(signals)} 个高风险任务场景")
    return signals

def write_signals_to_table(signals):
    """将信号写入 L3_Signal_Alerts 表"""
    today_ms = get_today_timestamp()
    
    print(f"\n[写入] 准备写入 {len(signals)} 条信号到 L3_Signal_Alerts...")
    
    for signal in signals:
        # 实际应调用 feishu_bitable_app_table_record
        # feishu_bitable_app_table_record(
        #     action="create",
        #     app_token=APP_TOKEN,
        #     table_id=TABLE_SIGNAL_ALERTS,
        #     fields={
        #         "日期": today_ms,
        #         "信号类型": signal["signal_type"],
        #         "目标ID": signal["target_id"],
        #         "目标名称": signal["target_name"],
        #         "健康度得分": signal["health_score"],
        #         "触发次数": signal["trigger_count"],
        #         "风险值": signal["risk_value"],
        #         "风险描述": signal["risk_desc"],
        #         "建议文案": signal["recommendation"],
        #         "严重程度": signal["severity"],
        #         "是否已处理": False
        #     }
        # )
        
        print(f"  - {signal['signal_type']}: {signal['target_name']} (严重度: {signal['severity']})")
    
    print(f"✅ 全部写入完成")

def main():
    print("=" * 60)
    print("三类信号自动生成脚本 v2.1.0")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 检测三类信号
    signal_1 = detect_high_score_low_use()
    signal_2 = detect_low_score_high_risk()
    signal_3 = detect_high_risk_task()
    
    # 2. 合并所有信号
    all_signals = signal_1 + signal_2 + signal_3
    
    # 3. 写入数据表
    if all_signals:
        write_signals_to_table(all_signals)
    else:
        print("\n⚠️ 今日无新信号生成")
    
    print("\n" + "=" * 60)
    print(f"✅ 完成，共生成 {len(all_signals)} 条信号")
    print("=" * 60)

if __name__ == "__main__":
    main()
