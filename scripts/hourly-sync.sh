#!/bin/bash
# Skill 使用数据每小时同步脚本
# 由 HEARTBEAT.md 触发执行

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SYNC_FILE="$HOME/.openclaw/workspace/logs/skill-usage-sync.json"

# 获取当前时间
CURRENT_MINUTE=$(date +%M)
CURRENT_HOUR=$(date +%H)

# 只在整点执行（每小时 00 分）
if [ "$CURRENT_MINUTE" != "00" ]; then
    # 不是整点，静默退出
    exit 0
fi

# 整点执行同步
echo "[$(date)] Hourly sync triggered at $CURRENT_HOUR:00"

# 1. 调用 track-usage.py sync 生成待同步文件
python3 "$SKILL_DIR/scripts/track-usage.py" sync

# 2. 检查是否有待同步文件
if [ ! -f "$SYNC_FILE" ]; then
    echo "[$(date)] No data to sync"
    exit 0
fi

# 3. 读取待同步文件内容
SYNC_DATA=$(cat "$SYNC_FILE")
APP_TOKEN=$(echo "$SYNC_DATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['app_token'])")
TABLE_ID=$(echo "$SYNC_DATA" | python3 -c "import sys, json; print(json.load(sys.stdin)['table_id'])")
RECORDS_JSON=$(echo "$SYNC_DATA" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)['records']))")

echo "[$(date)] Syncing to $APP_TOKEN/$TABLE_ID"
echo "[$(date)] Records count: $(echo "$RECORDS_JSON" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")"

# 4. 调用飞书 API 上报（通过 OpenClaw Agent）
# 这里返回执行指令，由 Heartbeat 调用 feishu_bitable_app_table_record
echo "SYNC_READY:$APP_TOKEN:$TABLE_ID:$RECORDS_JSON"
