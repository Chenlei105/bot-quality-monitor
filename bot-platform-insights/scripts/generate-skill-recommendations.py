#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 编排推荐脚本（模块 D）
基于 L3_Skill_Run 历史数据，推荐最优 Skill 组合

输出：
- 最优组合 Top 5（成功率 >= 80% AND 样本量 >= 5）
- 高风险组合预警（失败率 >= 50% OR 协作成本 >= 2.0）
"""

import sys
from datetime import datetime, timedelta

# 添加 openclaw 模块路径
sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.8_@napi-rs+canvas@0.1.97_@types+express@5.0.6_hono@4.12.8_node-llama-cpp@3.16.2/node_modules/openclaw')

def read_skill_runs():
    """读取 L3_Skill_Run 表最近 30 天数据"""
    from tools.feishu_bitable import feishu_bitable_app_table_record
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_ms = int(thirty_days_ago.timestamp() * 1000)
    
    result = feishu_bitable_app_table_record(
        action="list",
        app_token="TlRGbhGFga92WNsxWvHc5CYWntd",
        table_id="tblx8xYKaUOSXhux",  # L3_Skill_Run
        page_size=500
    )
    
    # 过滤最近 30 天数据
    skill_runs = []
    for record in result.get('records', []):
        fields = record.get('fields', {})
        start_time = fields.get('开始时间', 0)
        if start_time >= thirty_days_ago_ms:
            skill_runs.append(fields)
    
    return skill_runs

def group_by_session(skill_runs):
    """按会话 ID 分组"""
    sessions = {}
    
    for run in skill_runs:
        session_id = run.get('会话ID', '')
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(run)
    
    # 筛选多 Skill 协作场景（skill_count >= 2）
    multi_skill_sessions = {}
    for session_id, runs in sessions.items():
        if len(runs) >= 2:
            # 按开始时间排序
            runs_sorted = sorted(runs, key=lambda x: x.get('开始时间', 0))
            multi_skill_sessions[session_id] = runs_sorted
    
    return multi_skill_sessions

def analyze_combinations(multi_skill_sessions):
    """分析 Skill 组合统计"""
    combinations = {}
    
    for session_id, runs in multi_skill_sessions.items():
        # 提取 Skill 执行顺序
        skills = [r.get('Skill名称', 'Unknown') for r in runs]
        skill_sequence = ' → '.join(skills)
        
        # 完成状态（继承会话级状态）
        completion_status = runs[0].get('完成状态', 'unknown')
        is_success = (completion_status == 'completed')
        
        # 协作成本系数
        collaboration_cost = runs[0].get('协作成本系数', 1.0)
        
        # 初始化统计
        if skill_sequence not in combinations:
            combinations[skill_sequence] = {
                'total_count': 0,
                'success_count': 0,
                'costs': []
            }
        
        # 累加统计
        stats = combinations[skill_sequence]
        stats['total_count'] += 1
        if is_success:
            stats['success_count'] += 1
        stats['costs'].append(collaboration_cost)
    
    # 计算派生指标
    for seq, stats in combinations.items():
        stats['success_rate'] = stats['success_count'] / stats['total_count']
        stats['failure_rate'] = 1 - stats['success_rate']
        stats['avg_cost'] = sum(stats['costs']) / len(stats['costs'])
    
    return combinations

def get_best_combinations(combinations):
    """筛选最优组合 Top 5"""
    best = []
    
    for seq, stats in combinations.items():
        if stats['success_rate'] >= 0.80 and stats['total_count'] >= 5:
            best.append({
                'sequence': seq,
                'success_rate': stats['success_rate'],
                'avg_cost': stats['avg_cost'],
                'total_count': stats['total_count']
            })
    
    # 按成功率降序，协作成本升序排序
    best.sort(key=lambda x: (x['success_rate'], -x['avg_cost']), reverse=True)
    
    return best[:5]

def get_risky_combinations(combinations):
    """筛选高风险组合"""
    risky = []
    
    for seq, stats in combinations.items():
        if stats['failure_rate'] >= 0.50 or stats['avg_cost'] >= 2.0:
            reason = []
            if stats['failure_rate'] >= 0.50:
                reason.append(f"失败率 {stats['failure_rate']*100:.1f}%")
            if stats['avg_cost'] >= 2.0:
                reason.append(f"协作成本 {stats['avg_cost']:.2f}")
            
            risky.append({
                'sequence': seq,
                'failure_rate': stats['failure_rate'],
                'avg_cost': stats['avg_cost'],
                'total_count': stats['total_count'],
                'reason': ' + '.join(reason)
            })
    
    # 按失败率降序排序
    risky.sort(key=lambda x: x['failure_rate'], reverse=True)
    
    return risky

def print_recommendations(best, risky):
    """打印推荐报告"""
    print("\n" + "=" * 60)
    print("📋 Skill 编排推荐报告")
    print("=" * 60)
    
    if best:
        print("\n✅ 最优组合 Top 5:")
        for i, combo in enumerate(best, 1):
            print(f"\n  {i}. {combo['sequence']}")
            print(f"     成功率: {combo['success_rate']*100:.1f}%")
            print(f"     协作成本: {combo['avg_cost']:.2f}x")
            print(f"     样本量: {combo['total_count']} 次")
    else:
        print("\n✅ 暂无符合条件的最优组合（成功率 >= 80% AND 样本量 >= 5）")
    
    if risky:
        print("\n⚠️ 高风险组合预警:")
        for i, combo in enumerate(risky, 1):
            print(f"\n  {i}. {combo['sequence']}")
            print(f"     失败率: {combo['failure_rate']*100:.1f}%")
            print(f"     协作成本: {combo['avg_cost']:.2f}x")
            print(f"     样本量: {combo['total_count']} 次")
            print(f"     ⚠️ {combo['reason']}")
            
            # 建议
            if combo['failure_rate'] >= 0.50:
                print(f"     💡 建议: 失败率过高，避免使用该组合")
            elif combo['avg_cost'] >= 2.0:
                print(f"     💡 建议: 协作成本过高，考虑拆分为更小的任务")
    else:
        print("\n⚠️ 暂无高风险组合")

def main():
    """主函数"""
    print("=" * 60)
    print("Skill 编排推荐脚本（模块 D）")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: 读取 L3_Skill_Run 数据
    print("\n[1/4] 读取 L3_Skill_Run 表（最近 30 天）...")
    skill_runs = read_skill_runs()
    print(f"✅ 读取 {len(skill_runs)} 条 Skill 运行记录")
    
    # Step 2: 按会话分组
    print("\n[2/4] 按会话分组，识别多 Skill 协作场景...")
    multi_skill_sessions = group_by_session(skill_runs)
    print(f"✅ 识别 {len(multi_skill_sessions)} 个多 Skill 协作会话")
    
    # Step 3: 分析组合统计
    print("\n[3/4] 分析 Skill 组合统计...")
    combinations = analyze_combinations(multi_skill_sessions)
    print(f"✅ 统计 {len(combinations)} 种 Skill 组合")
    
    # Step 4: 生成推荐
    print("\n[4/4] 生成推荐报告...")
    best = get_best_combinations(combinations)
    risky = get_risky_combinations(combinations)
    
    # 打印报告
    print_recommendations(best, risky)
    
    print("\n" + "=" * 60)
    print("✅ Skill 编排推荐完成！")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
