#!/usr/bin/env python3
"""
Skill ROI 计算器

功能:
- 读取中央表格的 L3_Skill_Run 数据
- 计算每个 Skill 的 ROI（性价比评分）
- 写入 L3_Skill_ROI 表

ROI 计算公式:
ROI = (成功率 × 0.4) + (时间节省 × 0.3) + (用户满意度 × 0.3)

用法:
    python3 calculate-skill-roi.py
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 中央表格（大少爷）
CENTRAL_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"

def main():
    """主流程"""
    # 输出工作流（由 Bot 执行）
    workflow = {
        "description": "计算 Skill ROI（中央表格）",
        "steps": [
            # Step 1: 读取最近 30 天的 Skill 运行数据
            {
                "step": 1,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_Skill_Run_table_id}",  # 需要先获取
                    "filter": {
                        "conjunction": "and",
                        "conditions": [{
                            "field_name": "run_time",
                            "operator": "isGreaterEqual",
                            "value": [(datetime.now() - timedelta(days=30)).timestamp() * 1000]
                        }]
                    },
                    "page_size": 500
                },
                "save_as": "skill_runs"
            },
            
            # Step 2: Python 计算 ROI
            {
                "step": 2,
                "description": "计算每个 Skill 的 ROI",
                "python_logic": """
def calculate_roi(skill_runs):
    # 按 Skill 分组
    skill_groups = {}
    for run in skill_runs:
        skill_name = run.get('skill_name', '')
        if skill_name not in skill_groups:
            skill_groups[skill_name] = []
        skill_groups[skill_name].append(run)
    
    # 计算 ROI
    roi_data = []
    for skill_name, runs in skill_groups.items():
        total_runs = len(runs)
        success_runs = len([r for r in runs if r.get('status') == 'success'])
        total_duration = sum(r.get('duration_ms', 0) for r in runs)
        avg_duration = total_duration / total_runs if total_runs > 0 else 0
        
        # 成功率
        success_rate = success_runs / total_runs if total_runs > 0 else 0
        
        # 时间节省（与手动操作对比，假设手动需要 5 分钟）
        manual_time = 5 * 60 * 1000  # 5 分钟
        time_saved = (manual_time - avg_duration) / manual_time if avg_duration < manual_time else 0
        
        # 用户满意度（基于纠错率，假设纠错率越低满意度越高）
        correction_rate = sum(r.get('correction_count', 0) for r in runs) / total_runs if total_runs > 0 else 0
        satisfaction = 1 - correction_rate
        
        # ROI 计算
        roi_score = (success_rate * 0.4) + (time_saved * 0.3) + (satisfaction * 0.3)
        roi_score = round(roi_score * 100, 2)  # 转换为 0-100 分
        
        roi_data.append({
            'skill_name': skill_name,
            'total_runs': total_runs,
            'success_rate': round(success_rate * 100, 2),
            'avg_duration_ms': round(avg_duration),
            'roi_score': roi_score,
            'last_updated': int(datetime.now().timestamp() * 1000)
        })
    
    return roi_data
                """,
                "input": "${skill_runs}",
                "save_as": "roi_data"
            },
            
            # Step 3: 清空旧数据
            {
                "step": 3,
                "description": "清空 L3_Skill_ROI 表（避免重复）",
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "list",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_Skill_ROI_table_id}",
                    "page_size": 500
                },
                "save_as": "old_records"
            },
            {
                "step": 4,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_delete",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_Skill_ROI_table_id}",
                    "record_ids": "${extract_record_ids(old_records)}"
                }
            },
            
            # Step 4: 写入新数据
            {
                "step": 5,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": "${L3_Skill_ROI_table_id}",
                    "records": "${roi_data}"
                }
            }
        ],
        "success_message": f"✅ Skill ROI 计算完成！共 {len('${roi_data}')} 个 Skill"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
