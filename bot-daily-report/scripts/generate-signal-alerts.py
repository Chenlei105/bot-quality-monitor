#!/usr/bin/env python3
"""
三类智能信号自动生成脚本 v1.0.0
执行时间: 每日 21:00 (GMT+8)
数据来源: L2 会话汇总表 (最近 7 天)
输出目标: L3_Signal_Alerts 表 (tblVDILmtu1oYRTE)

三类信号:
1. 高分低用 Bot: health_score >= 85 AND weekly_trigger_count <= 5
2. 低分高风险 Bot: correction_rate >= 0.10 OR failure_count >= 5
3. 高风险任务场景: failure_rate >= 0.30 AND sample_count >= 5
"""

import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict

# 添加项目根目录到路径
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/bot-daily-report'))

# ========== 使用埋点 ==========
def _track_usage():
    try:
        track_script = os.path.expanduser('~/.openclaw/workspace/skills/bot-quality-monitor/scripts/track-usage.py')
        if os.path.exists(track_script):
            import subprocess
            subprocess.run([sys.executable, track_script, 'run', '{"scene": "signal_alerts"}'], 
                         capture_output=True, timeout=3)
    except:
        pass  # 静默失败，不影响正常运行

_track_usage()

# 多维表格配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
L2_TABLE_ID = "tbl8DXVbka7tvMGg"  # L2 会话汇总表
L3_SIGNAL_TABLE_ID = "tblVDILmtu1oYRTE"  # L3_Signal_Alerts

def calculate_bot_health_score(stats):
    """
    计算 Bot 综合健康度
    质量分 = 首解率×50% + (1−纠错率)×30% + 知识召回率×20%
    效率分 = max(0, 100 − (平均轮次−1)×15)
    资源分 = max(0, 100 − 失败次数×10)
    综合 = 质量×0.40 + 效率×0.30 + 资源×0.30
    """
    # 质量分
    first_resolve_rate = stats['first_resolve_count'] / stats['total'] if stats['total'] > 0 else 0
    correction_rate = stats['correction_count'] / stats['total'] if stats['total'] > 0 else 0
    knowledge_hit_rate = stats['knowledge_hit_count'] / stats['total'] if stats['total'] > 0 else 0.8
    
    quality_score = (
        first_resolve_rate * 50 +
        (1 - correction_rate) * 30 +
        knowledge_hit_rate * 20
    )
    
    # 效率分
    avg_turns = stats['total_turns'] / stats['total'] if stats['total'] > 0 else 1
    efficiency_score = max(0, 100 - (avg_turns - 1) * 15)
    
    # 资源分
    resource_score = max(0, 100 - stats['failure_count'] * 10)
    
    # 综合健康度
    health_score = quality_score * 0.40 + efficiency_score * 0.30 + resource_score * 0.30
    
    return {
        'health_score': round(health_score, 1),
        'quality_score': round(quality_score, 1),
        'efficiency_score': round(efficiency_score, 1),
        'resource_score': round(resource_score, 1),
        'correction_rate': round(correction_rate, 3),
        'first_resolve_rate': round(first_resolve_rate, 3),
        'avg_turns': round(avg_turns, 1)
    }

def read_l2_last_7_days():
    """读取 L2 表最近 7 天数据"""
    print("📊 读取 L2 最近 7 天数据...")
    
    # 计算 7 天前的时间戳
    seven_days_ago = datetime.now() - timedelta(days=7)
    seven_days_ago_ms = int(seven_days_ago.timestamp() * 1000)
    
    # 这里使用伪代码,实际需要调用 feishu_bitable_app_table_record
    # 由于在 Python 脚本中无法直接调用 OpenClaw 工具,需要通过 subprocess 调用
    # 或者改为在 SKILL.md 中执行
    
    # 临时方案: 返回模拟数据结构
    # 实际使用时,这部分应该通过 OpenClaw Skill 调用工具获取
    return {
        'records': [],
        'filter_condition': {
            "conjunction": "and",
            "conditions": [{
                "field_name": "开始时间",
                "operator": "isGreaterEqual",
                "value": [str(seven_days_ago_ms)]
            }]
        }
    }

def aggregate_bot_stats(sessions):
    """按 Bot 分组聚合统计"""
    bot_stats = defaultdict(lambda: {
        'bot_id': '',
        'bot_name': '',
        'total': 0,
        'first_resolve_count': 0,
        'correction_count': 0,
        'knowledge_hit_count': 0,
        'total_turns': 0,
        'failure_count': 0,
        'weekly_trigger_count': 0
    })
    
    for session in sessions:
        bot_id = session.get('机器人ID', '')
        bot_name = session.get('机器人名称', '')
        
        stats = bot_stats[bot_id]
        stats['bot_id'] = bot_id
        stats['bot_name'] = bot_name
        stats['total'] += 1
        stats['weekly_trigger_count'] += 1
        
        if session.get('首次解决', False):
            stats['first_resolve_count'] += 1
        
        stats['correction_count'] += session.get('纠正次数', 0)
        
        if session.get('知识库命中', False):
            stats['knowledge_hit_count'] += 1
        
        stats['total_turns'] += session.get('对话轮数', 0)
        
        if session.get('完成状态', '') == 'failed':
            stats['failure_count'] += 1
    
    return dict(bot_stats)

def aggregate_scene_stats(sessions):
    """按场景分组聚合统计"""
    scene_stats = defaultdict(lambda: {
        'scene': '',
        'total': 0,
        'failure_count': 0
    })
    
    for session in sessions:
        scene = session.get('场景分类', '未分类')
        stats = scene_stats[scene]
        stats['scene'] = scene
        stats['total'] += 1
        
        if session.get('完成状态', '') == 'failed':
            stats['failure_count'] += 1
    
    return dict(scene_stats)

def detect_signals(bot_stats, scene_stats):
    """检测三类信号"""
    signals = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 信号 1: 高分低用 Bot
    for bot_id, stats in bot_stats.items():
        scores = calculate_bot_health_score(stats)
        
        if scores['health_score'] >= 85 and stats['weekly_trigger_count'] <= 5:
            signals.append({
                "统计日期": today,
                "信号类型": "high_score_low_use",
                "目标ID": stats['bot_id'],
                "目标名称": stats['bot_name'],
                "得分/风险值": scores['health_score'],
                "触发次数": stats['weekly_trigger_count'],
                "严重程度": "low",
                "建议文案": f"{stats['bot_name']} 健康度 {scores['health_score']} 分但本周只用了 {stats['weekly_trigger_count']} 次,建议多使用高质量 Bot"
            })
    
    # 信号 2: 低分高风险 Bot
    for bot_id, stats in bot_stats.items():
        scores = calculate_bot_health_score(stats)
        
        if scores['correction_rate'] >= 0.10 or stats['failure_count'] >= 5:
            severity = "critical" if scores['correction_rate'] >= 0.20 else "high"
            signals.append({
                "统计日期": today,
                "信号类型": "low_score_high_risk",
                "目标ID": stats['bot_id'],
                "目标名称": stats['bot_name'],
                "得分/风险值": scores['correction_rate'] * 100,
                "触发次数": stats['failure_count'],
                "严重程度": severity,
                "建议文案": f"⚠️ {stats['bot_name']} 纠错率 {scores['correction_rate']*100:.1f}% 或失败 {stats['failure_count']} 次,建议立即优化或暂停使用"
            })
    
    # 信号 3: 高风险任务场景
    for scene, stats in scene_stats.items():
        if stats['total'] >= 5:
            failure_rate = stats['failure_count'] / stats['total']
            
            if failure_rate >= 0.30:
                signals.append({
                    "统计日期": today,
                    "信号类型": "high_risk_task",
                    "目标ID": scene,
                    "目标名称": scene,
                    "得分/风险值": failure_rate * 100,
                    "触发次数": stats['failure_count'],
                    "严重程度": "medium",
                    "建议文案": f"🔴 场景「{scene}」失败率 {failure_rate*100:.1f}% (样本 {stats['total']} 次),建议暂时避开或优化相关 Skill"
                })
    
    return signals

def write_to_l3_signal_alerts(signals):
    """写入 L3_Signal_Alerts 表"""
    if not signals:
        print("✅ 无信号触发,跳过写入")
        return
    
    print(f"📝 准备写入 {len(signals)} 条信号记录...")
    
    # 这里需要通过 OpenClaw Skill 调用 feishu_bitable_app_table_record
    # 临时方案: 打印数据结构
    for signal in signals:
        print(f"  - {signal['信号类型']}: {signal['建议文案']}")
    
    # 实际写入逻辑 (需要在 SKILL.md 中调用工具)
    # feishu_bitable_app_table_record(
    #     action="batch_create",
    #     app_token=APP_TOKEN,
    #     table_id=L3_SIGNAL_TABLE_ID,
    #     records=[{"fields": s} for s in signals]
    # )
    
    return signals

def main():
    """主函数"""
    print("=" * 60)
    print("🔔 三类智能信号自动生成脚本 v1.0.0")
    print("=" * 60)
    
    # Step 1: 读取 L2 数据
    l2_data = read_l2_last_7_days()
    sessions = l2_data.get('records', [])
    
    if not sessions:
        print("⚠️ 无最近 7 天数据,退出")
        return []
    
    print(f"✅ 读取到 {len(sessions)} 条会话记录")
    
    # Step 2: 按 Bot 聚合
    bot_stats = aggregate_bot_stats(sessions)
    print(f"✅ 聚合 {len(bot_stats)} 个 Bot 的数据")
    
    # Step 3: 按场景聚合
    scene_stats = aggregate_scene_stats(sessions)
    print(f"✅ 聚合 {len(scene_stats)} 个场景的数据")
    
    # Step 4: 检测信号
    signals = detect_signals(bot_stats, scene_stats)
    print(f"✅ 检测到 {len(signals)} 个信号")
    
    # Step 5: 写入 L3
    write_to_l3_signal_alerts(signals)
    
    print("=" * 60)
    print("✅ 信号生成完成")
    print("=" * 60)
    
    return signals

if __name__ == "__main__":
    main()
