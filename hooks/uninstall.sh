#!/bin/bash
# Bot Quality Monitor - 卸载钩子
# 在 Skill 卸载时自动触发，上报卸载事件

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARENT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SUB_SKILLS=("bot-analytics-collector" "bot-daily-report" "bot-platform-insights")

echo "[uninstall] 正在卸载 Bot Quality Monitor..."
echo "[uninstall] 正在上报匿名卸载统计..."

# 调用埋点脚本
python3 "$SKILL_DIR/scripts/track-usage.py" uninstall '{"source": "github"}'

echo "[uninstall] 统计已记录"
echo ""
echo "[uninstall] 正在卸载子 Skill..."

for skill in "${SUB_SKILLS[@]}"; do
    if [ -d "$PARENT_DIR/$skill" ]; then
        echo "[uninstall]   正在卸载 $skill..."
        rm -rf "$PARENT_DIR/$skill"
        echo "[uninstall]   ✓ $skill 已卸载"
    else
        echo "[uninstall]   ✓ $skill 不存在，跳过"
    fi
done

echo ""
echo "👋 卸载完成！感谢使用 Bot Quality Monitor"
echo "   如有问题或建议，欢迎反馈：https://github.com/Chenlei105/bot-quality-monitor"
echo "   注意：飞书多维表格不会自动删除，如需完全清理请手动删除"
echo ""
