#!/bin/bash
# Bot Quality Monitor - 安装钩子
# 在 Skill 安装时自动触发，上报安装事件

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPORTS_DIR="/root/.openclaw/workspace/reports"

echo "[install] Bot Quality Monitor v4.0.0 安装中..."
echo "[install] 正在检查 Python 依赖..."

# 自动安装 Python 依赖
python3 -c "import plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[install] 安装 plotly..."
    pip3 install plotly
else
    echo "[install] ✓ plotly 已安装"
fi

python3 -c "import jinja2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[install] 安装 jinja2..."
    pip3 install jinja2
else
    echo "[install] ✓ jinja2 已安装"
fi

# 创建 reports 目录
if [ ! -d "$REPORTS_DIR" ]; then
    echo "[install] 创建 reports 目录..."
    mkdir -p "$REPORTS_DIR"
else
    echo "[install] ✓ reports 目录已存在"
fi

# 创建 config.json 如果不存在
if [ ! -f "$SKILL_DIR/config.json" ]; then
    echo "[install] 创建配置文件模板..."
    cat > "$SKILL_DIR/config.json" << EOF
{
  "bitableAppToken": "",
  "receiverOpenId": "",
  "tables": {
    "L1": "",
    "L2": "",
    "L3_daily": "",
    "L3_signals": "",
    "L3_roi": "",
    "L3_run": "",
    "L0_usage": "",
    "L2_archive": "",
    "L1_archive": "",
    "L3_monthly": "",
    "L3_quarterly": "",
    "L3_yearly": ""
  },
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "healthWeights": {
    "quality": 0.40,
    "efficiency": 0.30,
    "resource": 0.30
  },
  "signalThresholds": {
    "highScoreLowUse": {
      "minHealthScore": 85,
      "maxWeeklyCount": 5
    },
    "lowScoreHighRisk": {
      "minCorrectionRate": 0.10,
      "minFailureCount": 5
    }
  },
  "businessValue": {
    "数据分析": 10,
    "文档处理": 8,
    "健康诊断": 5,
    "搜索查询": 4,
    "代码调试": 6,
    "闲聊": 1,
    "其他": 3
  }
}
EOF
else
    echo "[install] ✓ 配置文件已存在"
fi

# 调用埋点脚本
echo "[install] 正在上报匿名安装统计..."
python3 "$SKILL_DIR/scripts/track-usage.py" install '{"source": "github"}'

echo "[install] 统计已记录到本地日志"
echo "[install] 下次 sync 时将同步到服务器"
echo ""
echo "[install] 正在安装子 Skill..."
# 自动安装子 Skill 到 skills 根目录
SUB_SKILLS=("bot-analytics-collector" "bot-daily-report" "bot-platform-insights")
# 获取 skills 根目录（当前 Skill 的上级目录就是 skills 根目录）
PARENT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
# 当前 Skill 目录
SKILL_PARENT="$SKILL_DIR"

install_failed=()
for skill in "${SUB_SKILLS[@]}"; do
    if [ ! -d "$PARENT_DIR/$skill" ]; then
        echo "[install]   安装 $skill..."
        if [ -d "$SKILL_PARENT/$skill" ]; then
            cp -R "$SKILL_PARENT/$skill" "$PARENT_DIR/$skill"
            if [ $? -eq 0 ]; then
                echo "[install]   ✓ $skill 安装成功"
            else
                echo "[install]   ✗ $skill 安装失败"
                install_failed+=("$skill")
            fi
        else
            echo "[install]   ✗ $skill 源不存在，跳过"
            install_failed+=("$skill")
        fi
    else
        echo "[install]   ✓ $skill 已存在，跳过"
    fi
done

echo ""
echo "🎉 安装完成！"
if [ ${#install_failed[@]} -eq 0 ]; then
    echo "✅ 所有 Skill 安装成功："
    echo "   • bot-quality-monitor (主系统)"
    echo "   • bot-analytics-collector (数据采集)"
    echo "   • bot-daily-report (日报生成)"
    echo "   • bot-platform-insights (平台洞察)"
    echo ""
    echo "下一步："
    echo "   对你的 Bot 说：帮我创建 Bot 质量监控数据表"
    echo "   Bot 会全自动创建多维表格和配置，10 秒搞定！"
    echo "   然后静待每天 22:00 接收健康度日报"
else
    echo "⚠️  部分 Skill 安装失败，请检查后重试"
    echo "   失败: ${install_failed[*]}"
fi
echo ""
