#!/usr/bin/env python3
"""
用户日报推送脚本 v5.0

功能:
1. 调用 generate-daily-report.py 生成飞书卡片
2. 调用 generate-detailed-report.py 生成详细文档
3. 调用 generate-dashboard.py 生成 Dashboard HTML
4. 推送飞书卡片（带文档链接 + Dashboard 链接）

用法:
    python3 send-personalized-report-v5.py
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"
SCRIPT_DIR = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/scripts"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def load_config():
    """加载配置"""
    try:
        if not CONFIG_PATH.exists():
            return None
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return None

def run_script(script_name):
    """执行脚本并获取输出"""
    script_path = SCRIPT_DIR / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            log(f"脚本执行失败: {script_name}")
            log(f"错误: {result.stderr}")
            return None
    except Exception as e:
        log(f"执行 {script_name} 异常: {e}")
        return None

def main():
    """主流程"""
    log("=" * 60)
    log("用户日报推送任务开始")
    log("=" * 60)
    
    # 1. 加载配置
    config = load_config()
    if not config:
        log("配置未就绪，跳过推送")
        return
    
    receiver_open_id = config.get('receiverOpenId')
    if not receiver_open_id:
        log("未配置接收者 open_id，跳过推送")
        return
    
    # 2. 生成飞书卡片
    log("Step 1: 生成飞书卡片...")
    card_workflow = run_script("generate-daily-report.py")
    
    # 3. 生成详细文档
    log("Step 2: 生成详细文档...")
    doc_workflow = run_script("generate-detailed-report.py")
    
    # 4. 生成 Dashboard HTML
    log("Step 3: 生成 Dashboard HTML...")
    dashboard_workflow = run_script("generate-dashboard.py")
    
    # 5. 输出推送工作流（由 Bot 执行）
    workflow = {
        "description": "推送用户日报",
        "steps": [
            # Step 1: 执行飞书卡片工作流
            {
                "step": 1,
                "description": "执行飞书卡片生成工作流",
                "workflow": card_workflow,
                "save_as": "feishu_card"
            },
            
            # Step 2: 执行详细文档工作流
            {
                "step": 2,
                "description": "执行详细文档生成工作流",
                "workflow": doc_workflow,
                "save_as": "doc_url"
            },
            
            # Step 3: 执行 Dashboard 工作流
            {
                "step": 3,
                "description": "执行 Dashboard 生成工作流",
                "workflow": dashboard_workflow,
                "save_as": "dashboard_html"
            },
            
            # Step 4: 上传 Dashboard HTML 到飞书云文档
            {
                "step": 4,
                "description": "上传 Dashboard HTML",
                "tool": "feishu_drive_file",
                "params": {
                    "action": "upload",
                    "file_path": str(Path.home() / ".openclaw/workspace/reports/dashboard-latest.html"),
                    "folder_token": config.get('reportFolderToken')  # 可选
                },
                "save_as": "dashboard_url"
            },
            
            # Step 5: 推送飞书卡片
            {
                "step": 5,
                "description": "推送飞书卡片到用户",
                "tool": "message",
                "params": {
                    "action": "send",
                    "channel": "feishu",
                    "target": f"user:{receiver_open_id}",
                    "message": "${feishu_card}",  # 卡片 JSON
                    "extra_params": {
                        "detailed_report_url": "${doc_url}",
                        "dashboard_url": "${dashboard_url}"
                    }
                }
            }
        ],
        "success_message": f"✅ 日报已推送给用户: {receiver_open_id}"
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))
    
    log("=" * 60)
    log("用户日报推送任务结束")
    log("=" * 60)

if __name__ == "__main__":
    main()
