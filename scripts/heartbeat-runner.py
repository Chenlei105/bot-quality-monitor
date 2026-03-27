#!/usr/bin/env python3
"""
Heartbeat 自动执行引擎 v1.0

功能:
- 每次 Heartbeat 时被 OpenClaw 调用
- 检查当前时间并执行对应的定时任务
- 支持每分钟/每小时/每日/每周任务

定时任务:
- 每分钟: collect-sessions.py（采集会话数据）
- 每小时整点: track-usage.py sync（同步到 Webhook）
- 每 10 分钟: process-webhook-messages.py（处理 Webhook 消息）
- 每日 21:00: generate-signal-alerts.py（生成三类信号）
- 每日 22:00: generate-daily-report.py + send-personalized-report.py（生成并推送日报）
- 每周日 20:00: 平台日报

用法:
    在 OpenClaw 的 Heartbeat 中调用
    python3 heartbeat-runner.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 脚本目录
SCRIPT_DIR = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/scripts"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[Heartbeat] [{timestamp}] {message}")

def run_script(script_name, args=None):
    """执行脚本"""
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        log(f"⚠️ 脚本不存在: {script_name}")
        return False
    
    try:
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        log(f"▶️ 执行: {script_name}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            log(f"✅ {script_name} 执行成功")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            log(f"❌ {script_name} 执行失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        log(f"⏱️ {script_name} 执行超时（5分钟）")
        return False
    except Exception as e:
        log(f"❌ {script_name} 执行异常: {e}")
        return False

def main():
    """主流程"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    log("=" * 60)
    log(f"Heartbeat 任务检查: {now.strftime('%Y-%m-%d %H:%M:%S')} (周{weekday+1})")
    log("=" * 60)
    
    tasks_executed = []
    
    # ======== 每分钟任务 ========
    log("🔍 检查每分钟任务...")
    if run_script("collect-sessions.py"):
        tasks_executed.append("采集会话数据")
    
    # ======== 每小时整点任务 ========
    if minute == 0:
        log("🔍 检查每小时任务...")
        if run_script("track-usage.py", ["sync"]):
            tasks_executed.append("同步 Skill 使用数据到 Webhook")
    
    # ======== 每 10 分钟任务 ========
    if minute in [0, 10, 20, 30, 40, 50]:
        log("🔍 检查每 10 分钟任务...")
        if run_script("process-webhook-messages.py"):
            tasks_executed.append("处理 Webhook 消息并写入中央表格")
    
    # ======== 每日 21:00 任务 ========
    if hour == 21 and minute == 0:
        log("🔍 检查每日 21:00 任务...")
        if run_script("generate-signal-alerts.py"):
            tasks_executed.append("生成三类智能信号")
    
    # ======== 每日 22:00 任务 ========
    if hour == 22 and minute == 0:
        log("🔍 检查每日 22:00 任务...")
        if run_script("generate-daily-report.py"):
            tasks_executed.append("生成用户日报")
        if run_script("send-personalized-report.py"):
            tasks_executed.append("推送用户日报")
    
    # ======== 每周日 20:00 任务 ========
    if weekday == 6 and hour == 20 and minute == 0:
        log("🔍 检查每周日 20:00 任务...")
        if run_script("calculate-skill-roi.py"):
            tasks_executed.append("计算 Skill ROI")
        if run_script("generate-platform-dashboard.py"):
            tasks_executed.append("生成平台 Dashboard")
        if run_script("send-platform-report.py"):
            tasks_executed.append("推送平台日报给大少爷")
    
    # ======== 汇总 ========
    log("=" * 60)
    if tasks_executed:
        log(f"✅ 本次 Heartbeat 执行了 {len(tasks_executed)} 个任务:")
        for task in tasks_executed:
            log(f"  - {task}")
    else:
        log("⏭️ 本次 Heartbeat 无定时任务需要执行")
    log("=" * 60)

if __name__ == "__main__":
    main()
