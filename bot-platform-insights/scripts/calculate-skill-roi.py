#!/usr/bin/env python3
"""
Skill ROI 评分计算脚本 v1.0.0
执行时间: 每日 21:00 (GMT+8)
数据来源: L2 会话汇总表
输出目标: L3_Skill_ROI 表 (tblJDP1E1fwxFadb)

ROI 计算公式:
- 平均成本 = (平均轮数 - 1) × 5 + 平均纠错次数 × 10 + (平均Token / 1000)
- ROI 得分 = 100 × (成功率 × 业务价值 - 平均成本) / 平均成本
- 风险指数 = (1 - 成功率) × 100 + 平均纠错次数 × 10
"""

import sys
import os
from datetime import datetime
from collections import defaultdict

# 多维表格配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
L2_TABLE_ID = "tbl8DXVbka7tvMGg"  # L2 会话汇总表
L3_SKILL_ROI_TABLE_ID = "tblJDP1E1fwxFadb"  # L3_Skill_ROI

# 业务价值权重表
BUSINESS_VALUE = {
    "数据分析": 10,
    "健康诊断": 5,
    "文档处理": 8,
    "技能管理": 3,
    "配置咨询": 4,
    "闲聊": 1,
    "其他": 3
}

def aggregate_by_scene(sessions):
    """按场景分类聚合统计"""
    skill_stats = defaultdict(lambda: {
        'skill_name': '',
        'total': 0,
        'success': 0,
        'turns': [],
        'corrections': [],
        'tokens': []
    })
    
    for session in sessions:
        scene = session.get('场景分类', '其他')
        stats = skill_stats[scene]
        stats['skill_name'] = scene
        stats['total'] += 1
        
        if session.get('完成状态', '') == 'completed':
            stats['success'] += 1
        
        stats['turns'].append(session.get('对话轮数', 0))
        stats['corrections'].append(session.get('纠正次数', 0))
        stats['tokens'].append(session.get('Token消耗量', 0))
    
    return dict(skill_stats)

def calculate_roi(stats):
    """
    计算 Skill ROI
    
    Args:
        stats: 包含 total, success, turns, corrections, tokens 的字典
    
    Returns:
        包含 ROI 得分和风险指数的字典
    """
    if stats['total'] == 0:
        return {
            'success_rate': 0,
            'avg_turns': 0,
            'avg_corrections': 0,
            'avg_tokens': 0,
            'avg_cost': 0,
            'roi_score': 0,
            'risk_index': 100
        }
    
    # 基础指标
    success_rate = stats['success'] / stats['total']
    avg_turns = sum(stats['turns']) / len(stats['turns']) if stats['turns'] else 0
    avg_corrections = sum(stats['corrections']) / len(stats['corrections']) if stats['corrections'] else 0
    avg_tokens = sum(stats['tokens']) / len(stats['tokens']) if stats['tokens'] else 0
    
    # 平均成本
    avg_cost = (avg_turns - 1) * 5 + avg_corrections * 10 + (avg_tokens / 1000)
    
    # 避免除零
    if avg_cost == 0:
        avg_cost = 0.1
    
    # 业务价值
    biz_value = BUSINESS_VALUE.get(stats['skill_name'], 3)
    
    # ROI 得分
    roi_score = 100 * (success_rate * biz_value - avg_cost) / avg_cost
    
    # 风险指数
    risk_index = (1 - success_rate) * 100 + avg_corrections * 10
    
    return {
        'success_rate': round(success_rate, 3),
        'avg_turns': round(avg_turns, 1),
        'avg_corrections': round(avg_corrections, 2),
        'avg_tokens': round(avg_tokens, 0),
        'avg_cost': round(avg_cost, 2),
        'roi_score': round(roi_score, 2),
        'risk_index': round(risk_index, 1),
        'business_value': biz_value
    }

def generate_roi_records(skill_stats):
    """生成 ROI 记录"""
    roi_records = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    for skill_name, stats in skill_stats.items():
        roi = calculate_roi(stats)
        
        # 性价比评级
        if roi['roi_score'] >= 50:
            roi_grade = "优秀"
        elif roi['roi_score'] >= 20:
            roi_grade = "良好"
        elif roi['roi_score'] >= 0:
            roi_grade = "一般"
        else:
            roi_grade = "待优化"
        
        # 风险等级
        if roi['risk_index'] >= 50:
            risk_level = "高风险"
        elif roi['risk_index'] >= 30:
            risk_level = "中风险"
        else:
            risk_level = "低风险"
        
        roi_records.append({
            "Skill名称": skill_name,
            "触发次数": stats['total'],
            "成功率": roi['success_rate'],
            "平均轮数": roi['avg_turns'],
            "平均纠错次数": roi['avg_corrections'],
            "平均Token消耗": int(roi['avg_tokens']),
            "平均成本": roi['avg_cost'],
            "业务价值": roi['business_value'],
            "ROI得分": roi['roi_score'],
            "性价比评级": roi_grade,
            "风险指数": roi['risk_index'],
            "风险等级": risk_level,
            "统计日期": today
        })
    
    # 按 ROI 得分降序排序
    roi_records.sort(key=lambda x: x['ROI得分'], reverse=True)
    
    return roi_records

def write_to_l3_skill_roi(records):
    """写入 L3_Skill_ROI 表"""
    if not records:
        print("⚠️ 无 ROI 记录,跳过写入")
        return
    
    print(f"📝 准备写入 {len(records)} 条 ROI 记录...")
    
    # 打印前 5 名
    print("\n🏆 ROI 排行榜 Top 5:")
    for i, record in enumerate(records[:5], 1):
        print(f"  {i}. {record['Skill名称']}: ROI {record['ROI得分']:.2f} (成功率 {record['成功率']*100:.1f}%, 风险 {record['风险指数']:.1f})")
    
    # 实际写入逻辑 (需要在 SKILL.md 中调用工具)
    # feishu_bitable_app_table_record(
    #     action="batch_create",
    #     app_token=APP_TOKEN,
    #     table_id=L3_SKILL_ROI_TABLE_ID,
    #     records=[{"fields": r} for r in records]
    # )
    
    return records

def main():
    """主函数"""
    print("=" * 60)
    print("💰 Skill ROI 评分计算脚本 v1.0.0")
    print("=" * 60)
    
    # Step 1: 读取 L2 数据 (这里需要实际调用工具)
    # 临时方案: 模拟数据
    sessions = []
    
    if not sessions:
        print("⚠️ 无会话数据,退出")
        return []
    
    print(f"✅ 读取到 {len(sessions)} 条会话记录")
    
    # Step 2: 按场景聚合
    skill_stats = aggregate_by_scene(sessions)
    print(f"✅ 聚合 {len(skill_stats)} 个场景/Skill 的数据")
    
    # Step 3: 计算 ROI
    roi_records = generate_roi_records(skill_stats)
    print(f"✅ 生成 {len(roi_records)} 条 ROI 记录")
    
    # Step 4: 写入 L3
    write_to_l3_skill_roi(roi_records)
    
    print("=" * 60)
    print("✅ ROI 计算完成")
    print("=" * 60)
    
    return roi_records

if __name__ == "__main__":
    main()
