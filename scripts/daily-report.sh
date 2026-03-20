#!/bin/bash
# Bot 质量监控每日日报任务包装脚本（v2.1.0）
# 每日 22:00 执行（建议用 cron 定时）
# 
# 使用方式：
#   crontab -e
#   0 22 * * * /root/.openclaw/workspace/skills/bot-quality-monitor-v15/heartbeat-daily-report.sh

set -e  # 遇到错误立即退出

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$HOME/.openclaw/workspace/logs/bot-daily-report.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

echo "========================================" >> "$LOG_FILE"
echo "Bot 质量监控每日日报任务" >> "$LOG_FILE"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Step 1：生成三类信号（21:00 应已执行，这里再确认一次）
echo "[Step 1] 生成三类信号..." >> "$LOG_FILE"
python3 "$SCRIPT_DIR/generate-signal-alerts.py" >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 三类信号生成成功" >> "$LOG_FILE"
else
    echo "❌ 三类信号生成失败，但继续执行" >> "$LOG_FILE"
fi

# Step 2：生成日报（调用 bot-daily-report Skill）
echo "[Step 2] 生成日报..." >> "$LOG_FILE"
# TODO: 实际调用 bot-daily-report Skill
# 示例：openclaw run bot-daily-report --today
echo "⏳ 日报生成功能待实现（需 Skill 安装）" >> "$LOG_FILE"

# Step 3：生成 HTML Dashboard（可选）
if [ "$ENABLE_HTML_DASHBOARD" = "true" ]; then
    echo "[Step 3] 生成 HTML Dashboard..." >> "$LOG_FILE"
    python3 "$SCRIPT_DIR/generate-html-dashboard.py" >> "$LOG_FILE" 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ HTML Dashboard 生成成功" >> "$LOG_FILE"
    else
        echo "❌ HTML Dashboard 生成失败" >> "$LOG_FILE"
    fi
else
    echo "[Step 3] HTML Dashboard 已禁用（ENABLE_HTML_DASHBOARD=false）" >> "$LOG_FILE"
fi

echo "========================================" >> "$LOG_FILE"
echo "✅ 每日日报任务执行完成" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
