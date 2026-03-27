#!/usr/bin/env python3
"""
平台日报推送脚本（给大少爷）

功能:
1. 调用 calculate-skill-roi.py 计算 Skill ROI
2. 调用 generate-platform-dashboard.py 生成平台 Dashboard
3. 生成飞书卡片（平台级统计）
4. 推送给大少爷

用法:
    python3 send-platform-report.py
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DAZHAOYE_OPEN_ID = "ou_baa3525cf6cb5c0fc1ce4e26753d812d"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def run_script(script_name):
    """执行脚本"""
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / script_name)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            log(f"脚本执行失败: {script_name}")
            return None
    except:
        return None

def main():
    """主流程"""
    log("=" * 60)
    log("平台日报推送任务开始（给大少爷）")
    log("=" * 60)
    
    # 1. 计算 Skill ROI
    log("Step 1: 计算 Skill ROI...")
    roi_workflow = run_script("calculate-skill-roi.py")
    
    # 2. 生成平台 Dashboard
    log("Step 2: 生成平台 Dashboard...")
    dashboard_workflow = run_script("generate-platform-dashboard.py")
    
    # 3. 输出推送工作流
    workflow = {
        "description": "推送平台日报给大少爷",
        "steps": [
            # Step 1: 执行 ROI 计算
            {
                "step": 1,
                "workflow": roi_workflow
            },
            
            # Step 2: 执行 Dashboard 生成
            {
                "step": 2,
                "workflow": dashboard_workflow,
                "save_as": "dashboard_html"
            },
            
            # Step 3: 上传 Dashboard 到飞书云文档
            {
                "step": 3,
                "tool": "feishu_drive_file",
                "params": {
                    "action": "upload",
                    "file_path": "/root/.openclaw/workspace/reports/platform-dashboard-latest.html"
                },
                "save_as": "dashboard_url"
            },
            
            # Step 4: 生成平台卡片
            {
                "step": 4,
                "description": "生成平台统计卡片",
                "action": "generate_platform_card",
                "save_as": "platform_card"
            },
            
            # Step 5: 推送给大少爷
            {
                "step": 5,
                "tool": "message",
                "params": {
                    "action": "send",
                    "channel": "feishu",
                    "target": f"user:{DAZHAOYE_OPEN_ID}",
                    "message": json.dumps({
                        "msg_type": "interactive",
                        "card": {
                            "header": {
                                "template": "purple",
                                "title": {
                                    "tag": "plain_text",
                                    "content": "🏆 OpenClaw 平台周报"
                                }
                            },
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": "**📊 平台级统计数据**"
                                    }
                                },
                                {
                                    "tag": "hr"
                                },
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": "${platform_summary}"
                                    }
                                },
                                {
                                    "tag": "hr"
                                },
                                {
                                    "tag": "action",
                                    "actions": [{
                                        "tag": "button",
                                        "text": {
                                            "tag": "plain_text",
                                            "content": "📊 查看 Dashboard"
                                        },
                                        "type": "primary",
                                        "url": "${dashboard_url}"
                                    }]
                                }
                            ]
                        }
                    }, ensure_ascii=False)
                }
            }
        ],
        "success_message": f"✅ 平台日报已推送给大少爷"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))
    
    log("=" * 60)
    log("平台日报推送任务结束")
    log("=" * 60)

if __name__ == "__main__":
    main()
