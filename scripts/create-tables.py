#!/usr/bin/env python3
"""
创建 L3_Skill_ROI 和 L3_Skill_Run 两张表
用于 v2.1.0 Skill 性价比评分和多Skill协作分析
"""

import os
import sys

# 数据中台 App Token
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"

def create_l3_skill_roi_table():
    """创建 L3_Skill_ROI 表"""
    print("[Task 6] 创建 L3_Skill_ROI 表...")
    
    from feishu_bitable_app_table import feishu_bitable_app_table
    
    result = feishu_bitable_app_table(
        action="create",
        app_token=APP_TOKEN,
        table={
            "name": "L3_Skill_ROI",
            "default_view_name": "所有Skill",
            "fields": [
                {"field_name": "Skill名称", "type": 1},  # 文本
                {"field_name": "触发次数", "type": 2},  # 数字
                {"field_name": "成功率", "type": 2, "property": {"formatter": "0.0"}},  # 数字（1位小数，百分比）
                {"field_name": "平均轮数", "type": 2, "property": {"formatter": "0.0"}},
                {"field_name": "平均纠错次数", "type": 2, "property": {"formatter": "0.00"}},
                {"field_name": "平均Token消耗", "type": 2},
                {"field_name": "ROI得分", "type": 2, "property": {"formatter": "0.0"}},
                {"field_name": "风险指数", "type": 2, "property": {"formatter": "0.0"}},
                {"field_name": "失败损失", "type": 2, "property": {"formatter": "0.0"}},
                {"field_name": "统计周期", "type": 1},  # 文本，如"2026-03-13 至 2026-03-20"
            ]
        }
    )
    
    if result.get('success'):
        table_id = result['data']['table_id']
        print(f"✅ L3_Skill_ROI 表创建成功，table_id: {table_id}")
        return table_id
    else:
        print(f"❌ 创建失败：{result.get('error')}")
        return None


def create_l3_skill_run_table():
    """创建 L3_Skill_Run 表"""
    print("[Task 7] 创建 L3_Skill_Run 表...")
    
    from feishu_bitable_app_table import feishu_bitable_app_table
    
    result = feishu_bitable_app_table(
        action="create",
        app_token=APP_TOKEN,
        table={
            "name": "L3_Skill_Run",
            "default_view_name": "所有执行记录",
            "fields": [
                {"field_name": "Run ID", "type": 1},  # 文本（session_id:skill_name）
                {"field_name": "会话ID", "type": 1},  # 文本
                {"field_name": "Skill名称", "type": 1},
                {"field_name": "协作Skill数", "type": 2},  # 数字（assists_total = skill_count - 1）
                {"field_name": "协作成本系数", "type": 2, "property": {"formatter": "0.0"}},
                {"field_name": "完成状态", "type": 3, "property": {"options": [
                    {"name": "completed"},
                    {"name": "completed_with_friction"},
                    {"name": "failed"},
                    {"name": "abandoned"}
                ]}},
                {"field_name": "会话开始时间", "type": 5},  # 日期
            ]
        }
    )
    
    if result.get('success'):
        table_id = result['data']['table_id']
        print(f"✅ L3_Skill_Run 表创建成功，table_id: {table_id}")
        return table_id
    else:
        print(f"❌ 创建失败：{result.get('error')}")
        return None


def write_test_data_roi(table_id):
    """写入测试数据到 L3_Skill_ROI"""
    print(f"[Task 6] 写入测试数据到 L3_Skill_ROI (table_id={table_id})...")
    
    from feishu_bitable_app_table_record import feishu_bitable_app_table_record
    
    test_data = {
        "Skill名称": "数据分析",
        "触发次数": 20,
        "成功率": 90.0,
        "平均轮数": 3.5,
        "平均纠错次数": 0.2,
        "平均Token消耗": 5000,
        "ROI得分": -53.8,  # 负数说明成本高于收益
        "风险指数": 12.0,
        "失败损失": 7.0,  # 2次失败 × 3.5轮 = 7轮浪费
        "统计周期": "2026-03-13 至 2026-03-20"
    }
    
    result = feishu_bitable_app_table_record(
        action="create",
        app_token=APP_TOKEN,
        table_id=table_id,
        fields=test_data
    )
    
    if result.get('success'):
        print("✅ 测试数据写入成功")
    else:
        print(f"❌ 写入失败：{result.get('error')}")


def write_test_data_run(table_id):
    """写入测试数据到 L3_Skill_Run"""
    print(f"[Task 7] 写入测试数据到 L3_Skill_Run (table_id={table_id})...")
    
    from feishu_bitable_app_table_record import feishu_bitable_app_table_record
    
    test_data = {
        "Run ID": "cli_xxx_ou_xxx_1710000000000:数据分析",
        "会话ID": "cli_xxx_ou_xxx_1710000000000",
        "Skill名称": "数据分析",
        "协作Skill数": 2,  # 共3个Skill，协作数=3-1=2
        "协作成本系数": 1.4,  # 1.0 + 2*0.2 = 1.4
        "完成状态": "completed",
        "会话开始时间": 1710000000000  # 2026-03-10 00:00:00 GMT+8
    }
    
    result = feishu_bitable_app_table_record(
        action="create",
        app_token=APP_TOKEN,
        table_id=table_id,
        fields=test_data
    )
    
    if result.get('success'):
        print("✅ 测试数据写入成功")
    else:
        print(f"❌ 写入失败：{result.get('error')}")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3.5 Task 6 & 7: 创建 L3_Skill_ROI + L3_Skill_Run 表")
    print("=" * 60)
    
    # Task 6
    roi_table_id = create_l3_skill_roi_table()
    if roi_table_id:
        write_test_data_roi(roi_table_id)
    
    print()
    
    # Task 7
    run_table_id = create_l3_skill_run_table()
    if run_table_id:
        write_test_data_run(run_table_id)
    
    print("\n" + "=" * 60)
    print("✅ Task 6 & 7 完成")
    print("=" * 60)
