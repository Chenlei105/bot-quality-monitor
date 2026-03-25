#!/bin/bash
# Bot Quality Monitor - 安装钩子
# 在 Skill 安装时自动触发，上报安装事件

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[install] Bot Quality Monitor 安装成功！"
echo "[install] 正在上报匿名安装统计..."

# 调用埋点脚本
python3 "$SKILL_DIR/scripts/track-usage.py" install '{"source": "github"}'

echo "[install] 统计已记录到本地日志"
echo "[install] 下次 sync 时将同步到服务器"
echo ""
echo "🎉 安装完成！开始使用："
echo "   1. 授权飞书权限（将自动触发）"
echo "   2. 明天 22:00 接收第一份健康度日报"
echo ""
