#!/bin/bash
# Bot Quality Monitor - 完整表格创建脚本
# 
# 这个脚本会：
# 1. 提示用户输入 open_id
# 2. 自动调用飞书 API 创建表格
# 3. 批量创建 11 张数据表
# 4. 添加核心字段
# 5. 写入测试数据
# 6. 保存配置到 config.json
#
# 用法：
#   bash setup-tables.sh

set -e  # 遇到错误立即退出

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Bot Quality Monitor - 表格创建向导"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 获取用户 open_id
read -p "请输入你的飞书 open_id (ou_xxx): " USER_OPEN_ID

if [[ ! $USER_OPEN_ID =~ ^ou_ ]]; then
    echo "❌ 错误：open_id 格式不正确，应该以 ou_ 开头"
    exit 1
fi

echo ""
echo "开始创建表格..."
echo ""

# 临时文件存储中间结果
TMP_DIR="/tmp/bot-quality-monitor-$$"
mkdir -p "$TMP_DIR"

# Step 1: 创建多维表格
echo "📊 第 1 步：创建飞书多维表格..."
python3 << 'PYTHON_STEP1'
import os
import sys
import json

# 这里应该调用 OpenClaw 的 feishu_bitable_app 工具
# 但由于无法在脚本中直接调用，我们输出指令让用户手动执行

print("""
⚠️  需要手动执行以下步骤：

1. 在 OpenClaw 中执行：
   对你的 Bot 说："帮我执行以下操作"
   
2. Bot 需要调用工具：
   feishu_bitable_app(action="create", name="OpenClaw Bot 质量监控")
   
3. 把返回的 app_token 告诉脚本

或者，直接让 Bot 执行完整的创建流程。
""")

PYTHON_STEP1

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⚠️  脚本方案行不通"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "原因：Shell 脚本无法直接调用 OpenClaw 的飞书工具"
echo ""
echo "请使用以下方法之一："
echo ""
echo "方法 1：让 Bot 直接创建（推荐）"
echo "  对 Bot 说：'请严格按照 bot-quality-monitor/SKILL.md 中的"
echo "  第 1-6 步，逐步创建表格，每步都要实际调用工具'"
echo ""
echo "方法 2：手动创建"
echo "  1. 在飞书中手动创建多维表格"
echo "  2. 手动创建 11 张数据表"
echo "  3. 手动填写 config.json"
echo ""
echo "方法 3：等待开发者修复"
echo "  需要创建一个能直接调用 OpenClaw API 的 Python 脚本"
echo ""

# 清理临时文件
rm -rf "$TMP_DIR"
