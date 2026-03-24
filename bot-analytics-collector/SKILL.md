---
name: bot-analytics-collector
version: 3.0.0
description: Bot 对话数据自动采集器。实时采集用户与 Bot 的对话数据，识别纠错信号、满意度、意图分类，写入 L1/L2 数据层。
author: 陈磊 / 小炸弹 💣
tags: [bot, analytics, data-collection, quality-monitor]
dependencies: []
---

# Bot Analytics Collector

**Bot 对话数据自动采集器 v3.0**

---

## 概述

Bot Analytics Collector 是 Bot Quality Monitor 系统的数据采集层，负责：

- 📥 **实时消息采集** - 捕获每条用户消息和 Bot 回复
- 🔍 **智能信号识别** - 自动识别纠错信号、满意度、首次解决
- 🏷️ **意图自动分类** - 数据分析 / 文档处理 / 健康诊断 / 闲聊
- 📊 **双层数据写入** - L1 消息明细 + L2 会话汇总

---

## 核心功能

### 1. 会话边界识别

```
规则: 相邻消息时间戳差 ≤ 15分钟 = 同一会话

session_id = f"{bot_id}_{user_id}_{首条消息时间戳毫秒}"
示例: cli_a922b6c0b8b89bd1_ou_abc123_1710748800000
```

### 2. 纠错信号识别

**强纠错信号（权重 2x）**:
```
不对 | 错了 | 错的 | 不是这个 | 重新来 | 重做 | 全错了 | 你理解错了 | 不是我的意思
```

**普通纠错信号（权重 1x）**:
```
再来一遍 | 重新 | 不对啊 | 这不对 | 不是 | 不行 | 换一个 | 不要这样
```

### 3. 满意度信号识别

**正向信号**:
```
好的 | 收到 | 谢谢 | OK | 👍 | ✅ | 牛 | 厉害 | 完美 | 就是这个
```

**负向信号**:
```
不行 | 太差了 | 没用 | 垃圾 | 算了
```

### 4. 首次解决率判定

✅ **算首次解决**:
- 用户在 Bot 回复后无追问，会话自然结束
- 用户发出正向满意度信号
- 无纠错信号

❌ **不算首次解决**:
- 用户发出追问信号
- 用户发出纠错信号
- 用户说"收到，但是..."

### 5. Skill Run 拆分

当会话触发多个 Skill 时，同步拆分到 L3_Skill_Run 表：

```python
skill_count = len(skill_triggered)
collaboration_cost = 1.0 + (skill_count - 1) * 0.2
key_path = skill_count >= 2
```

---

## 数据处理流程（7步）

| Step | 名称 | 说明 |
|------|------|------|
| 1 | 会话边界识别 | 相邻消息时间戳差 ≤ 15分钟 = 同一会话 |
| 2 | 意图分类 | 关键词匹配：数据分析/文档处理/健康诊断/闲聊 |
| 3 | 纠错信号识别 | 强信号词（权重2x）+ 普通信号词（权重1x） |
| 4 | 满意度信号识别 | 扫描最后一条用户消息，判断正向/负向/中性 |
| 5 | 首次解决率判定 | 无纠错 + 正向满意度 = 首解成功 |
| 6 | 写入 L1 | 每条消息写入消息明细表（幂等去重） |
| 7 | 写入 L2 + L3 | 会话汇总 + Skill Run 拆分 |

---

## L1 消息明细表字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| message_id | 文本 | 飞书消息 ID（全局唯一） |
| session_id | 文本 | 会话 ID |
| bot_id | 文本 | 机器人 ID |
| sender_id | 人员 | 发送者 open_id |
| channel_type | 单选 | group / p2p / bot_push |
| intent_label | 单选 | 意图分类标签 |
| correction_signal | 复选框 | 是否包含纠错信号 |
| response_ms | 数字 | 响应耗时（毫秒） |
| token_count | 数字 | Token 消耗 |

---

## L2 会话汇总表字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| session_id | 文本 | 会话 ID（主键） |
| scene_category | 单选 | 场景分类 |
| turn_count | 数字 | 对话轮数 |
| completion_status | 单选 | completed / failed / abandoned |
| correction_count | 数字 | 纠错次数 |
| first_resolve | 复选框 | 是否首次解决 |
| skill_count | 数字 | 触发 Skill 数量 |
| collaboration_cost | 数字 | 协作成本系数 |
| key_path | 复选框 | 是否关键路径 |
| user_owner_id | 人员 | 数据所有者 open_id |

---

## 配置

### 数据中台连接

```json
{
  "bitableAppToken": "Xw4Tb5C8KagMiQswkdacNfVPn8e",
  "tables": {
    "L1": "tblmKO3HejbWpUWe",
    "L2": "tblT0I1nCFhbpvGa",
    "L3_Skill_Run": "tblGOfgzbcle1C4N"
  }
}
```

### 会话切割参数

```json
{
  "sessionTimeoutMs": 900000,
  "minTurnsForSession": 1
}
```

---

## 隐私保护

- ✅ 分类标签（如「数据分析」「正向满意度」）
- ✅ 统计数字（纠错次数、Token 数量、响应耗时）
- ⚠️ 消息前 100 字摘要（可配置关闭）
- ❌ 消息原文（不存储）
- ❌ 用户真实姓名（只存 open_id）

---

## 相关文件

- `collect-with-user-id.py` - 带用户 ID 的采集脚本

---

## 版本历史

### v3.0.0 (2026-03-24)
- ✨ 新增 user_owner_id 字段支持多租户
- ✨ 新增 Skill Run 拆分逻辑
- ✨ 新增协作成本系数计算

### v2.1.0 (2026-03-18)
- 初始版本

---

## 许可证

MIT License
