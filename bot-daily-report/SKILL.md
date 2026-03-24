---
name: bot-daily-report
version: 3.0.0
description: Bot 健康度日报生成器。每日 22:00 自动推送麦肯锡风格健康度日报，包含三维度评分、三类智能信号、HTML Dashboard。
author: 陈磊 / 小炸弹 💣
tags: [bot, analytics, daily-report, dashboard, quality-monitor]
dependencies: [bot-analytics-collector]
---

# Bot Daily Report

**Bot 健康度日报生成器 v3.0**

---

## 概述

Bot Daily Report 是 Bot Quality Monitor 系统的报告生成层，负责：

- 📊 **三维度健康度计算** - 质量/效率/资源综合评分
- 📬 **麦肯锡风格日报** - 每日 22:00 自动推送飞书私信
- 🔔 **三类智能信号** - 高分低用/低分高风险/高风险任务场景
- 📈 **HTML 可视化看板** - Plotly 交互式图表

---

## 核心功能

### 1. 三维度健康度计算

**质量维度（40%）**:
- 首解率权重 50%
- (1-纠错率) 权重 30%
- 知识召回率权重 20%

**效率维度（30%）**:
- 基础分 100
- 每多一轮对话扣 15 分

**资源维度（30%）**:
- 基础分 100
- 每次失败扣 10 分

```python
health_score = quality * 0.40 + efficiency * 0.30 + resource * 0.30

# 评级
rating = "🟢优秀" if health_score >= 90 else \
         "🟡良好" if health_score >= 75 else \
         "🟠待改善" if health_score >= 60 else "🔴需关注"
```

### 2. 三类智能信号

| 信号类型 | 检测条件 | 建议 |
|----------|----------|------|
| 🌟 高分低用 Bot | 健康度≥85 且 周触发≤5 | Bot 质量很好但用得太少，建议多使用 |
| ⚠️ 低分高风险 Bot | 纠错率≥10% 或 失败≥5次 | Bot 错误率太高，建议立即优化 |
| 🔥 高风险任务场景 | 失败率≥30% 且 样本≥5 | 该场景最近失败率超过 30% |

### 3. 麦肯锡风格日报

```
📊 Bot 质量日报 (2026-03-24)

【综合健康度】82 分 🟡良好
├─ 质量: 85 分 (首解率 88%, 纠错率 3%)
├─ 效率: 80 分 (平均 2.3 轮)
└─ 资源: 78 分 (失败 2 次)

【7 天趋势】
├─ 纠错率: 3% → 2% ⬇️ (改善)
├─ 首解率: 85% → 88% ⬆️ (提升)
└─ 完成率: 92% → 95% ⬆️ (提升)

【智能信号】
🌟 小炸弹 健康度 92 分，但本周只用了 3 次
   建议：这个 Bot 很好用，可以多用

【明日行动】
1. 尝试用小炸弹处理更多任务
2. 检查忙狗的 Prompt 是否清晰
```

### 4. HTML Dashboard（5 模块）

1. **📊 综合健康度仪表盘** (Gauge Chart)
   - 0-100 得分
   - 颜色分段：红(<60) → 橙(60-75) → 浅绿(75-90) → 绿(>90)

2. **📈 7 天趋势折线图**
   - 纠错率（红线）
   - 首解率（绿线）
   - 任务完成率（蓝线）

3. **🎨 场景健康度热力图**
   - 行 = 场景分类
   - 列 = 指标维度
   - 颜色 = 健康度得分（RdYlGn 配色）

4. **🔔 三类信号卡片**
   - 从 L3_Signal_Alerts 读取
   - 按严重程度分色

5. **📋 失败案例 Top 10**
   - 从 L2 筛选 completion_status=failed
   - 展示失败类型 + 改进建议

---

## 脚本清单

| 脚本 | 大小 | 执行时间 | 功能 |
|------|------|----------|------|
| generate-signal-alerts.py | 9.4KB | 每日 21:00 | 生成三类智能信号，写入 L3_Signal_Alerts |
| generate-html-dashboard.py | 13.0KB | 每日 22:00 | 生成 Plotly 交互式 HTML 看板 |
| generate-static-dashboard.py | 7.7KB | 按需 | 生成静态 HTML（无 JS 依赖） |
| send-personalized-report.py | 5.0KB | 每日 22:00 | 推送个性化日报到飞书私信 |

---

## 定时任务配置

```bash
# 每日 21:00 生成三类信号
0 21 * * * python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-signal-alerts.py

# 每日 22:00 生成 HTML Dashboard
0 22 * * * python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-html-dashboard.py

# 每日 22:00 推送日报
0 22 * * * python3 ~/.openclaw/workspace/skills/bot-daily-report/send-personalized-report.py
```

---

## 输出文件

### HTML Dashboard
```
~/.openclaw/workspace/reports/bot-daily-{date}.html
```

### 飞书私信
- 推送到用户的飞书私聊
- 支持飞书卡片格式

---

## 配置

### 报告时间
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8"
}
```

### 健康度权重
```json
{
  "healthWeights": {
    "quality": 0.40,
    "efficiency": 0.30,
    "resource": 0.30
  }
}
```

### 信号阈值
```json
{
  "signalThresholds": {
    "highScoreLowUse": {
      "minHealthScore": 85,
      "maxWeeklyCount": 5
    },
    "lowScoreHighRisk": {
      "minCorrectionRate": 0.10,
      "minFailureCount": 5
    },
    "highRiskTask": {
      "minFailureRate": 0.30,
      "minSampleCount": 5
    }
  }
}
```

---

## L3_Signal_Alerts 表字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 统计日期 | 日期 | 信号生成日期 |
| 信号类型 | 单选 | high_score_low_use / low_score_high_risk / high_risk_task |
| 目标ID | 文本 | Bot ID 或场景名称 |
| 严重程度 | 单选 | low / medium / high |
| 触发次数 | 数字 | 该信号触发次数 |
| 建议文案 | 文本 | 具体改进建议 |

---

## 相关文件

```
bot-daily-report/
├── SKILL.md
├── send-personalized-report.py
└── scripts/
    ├── generate-signal-alerts.py
    ├── generate-html-dashboard.py
    └── generate-static-dashboard.py
```

---

## 版本历史

### v3.0.0 (2026-03-24)
- ✨ 三类智能信号自动检测
- ✨ HTML Dashboard 5 模块完整实现
- ✨ 麦肯锡风格日报格式
- ✨ 个性化报告推送

### v2.1.0 (2026-03-18)
- 初始版本

---

## 许可证

MIT License
