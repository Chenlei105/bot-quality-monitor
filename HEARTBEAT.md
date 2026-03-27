# HEARTBEAT.md

## ⚠️ 重要：OpenClaw 调用方式

**OpenClaw 在每次 Heartbeat 时应该调用**:
```bash
python3 ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/heartbeat-runner.py
```

heartbeat-runner.py 会自动检查时间并执行所有定时任务，无需手动配置。

---

## 定时任务清单

### 每分钟任务

**采集会话数据**:
- 脚本: `collect-sessions.py`
- 功能: 采集最近活跃的会话数据，写入用户自己的 L2_会话汇总表
- 数据: 写入用户自己的飞书表格（从 config.json 读取）

---

### 每小时整点任务

**同步 Skill 使用数据到 Webhook**:
- 脚本: `track-usage.py sync`
- 功能: 读取本地日志，发送到飞书 Webhook
- 数据: 跨企业数据收集（所有用户→大少爷中央表格）

---

### 每 10 分钟任务

**处理 Webhook 消息并写入中央表格**:
- 脚本: `process-webhook-messages.py`
- 功能: 搜索飞书消息，提取 JSON，写入中央表格
- 数据: 写入大少爷的中央表格（Xw4Tb5C8KagMiQswkdacNfVPn8e）

---

### 每日 21:00 任务

**生成三类智能信号**:
- 脚本: `generate-signal-alerts.py`
- 功能: 分析最近 7 天数据，生成高分低用/首解率下降/知识缺失信号
- 数据: 写入用户自己的 L3_三类信号表

---

### 每日 22:00 任务

**生成并推送用户日报**:
- 脚本 1: `generate-daily-report.py`
  - 功能: 生成飞书卡片（参考设计图）
  - 格式: 科技蓝页眉 + 四维指标 + 趋势对比 + 智能洞察 + 优先行动

- 脚本 2: `send-personalized-report.py`
  - 功能: 生成详细文档 + Dashboard HTML + 推送飞书卡片
  - 推送: 飞书卡片（带文档链接 + Dashboard 链接）

**配置**：
- 读取 `config.json` 获取推送时间和接收者
- 默认推送时间：22:00

---

### 每周日 20:00 任务

**生成并推送平台日报（给大少爷）**:
- 脚本 1: `calculate-skill-roi.py`
  - 功能: 计算 Skill ROI，写入 L3_Skill_ROI 表

- 脚本 2: `generate-platform-dashboard.py`
  - 功能: 生成平台级 Dashboard（所有用户的统计数据）

- 脚本 3: `send-platform-report.py`
  - 功能: 推送平台日报给大少爷
  - 内容: Bot 排行榜 + 失败模式识别 + Skill 编排推荐

---

## 配置文件

**config.json 位置**: `~/.openclaw/workspace/skills/bot-quality-monitor/config.json`

**必要字段**:
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "用户自己的多维表格 token",
  "receiverOpenId": "用户的 open_id",
  "tables": {
    "L2_会话汇总表": "table_id",
    "L3_每日指标汇总": "table_id",
    ...
  }
}
```

---

## 数据流向

### 用户私有数据（用户视角）
```
collect-sessions.py（每分钟）
  → 用户自己的 L2_会话汇总表
  → generate-daily-report.py（每日 22:00）
  → 推送给用户自己
```

### 中央平台数据（大少爷视角）
```
track-usage.py sync（每小时）
  → 飞书 Webhook
  → process-webhook-messages.py（每 10 分钟）
  → 大少爷的中央表格（Xw4Tb5C8KagMiQswkdacNfVPn8e）
  → send-platform-report.py（每周日 20:00）
  → 推送给大少爷
```

**两套数据完全隔离，互不干扰！**
