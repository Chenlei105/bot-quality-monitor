---
name: bot-platform-insights
version: 5.0.0
description: Bot 平台级洞察与 Skill 优化引擎。生成全平台健康看板、Skill ROI 评分、多 Skill 编排推荐，支持 Skill 自我迭代。
author: 陈磊 / 小炸弹 💣
tags: [bot, analytics, platform, skill-roi, optimization, quality-monitor]
dependencies: [bot-analytics-collector, bot-daily-report]
---

# Bot Platform Insights

**Bot 平台级洞察引擎 v3.0**

---

## 概述

Bot Platform Insights 是 Bot Quality Monitor 系统的平台洞察层，为平台运营者提供：

- 📊 **全局生态健康看板** - Bot 排行榜 + 场景分布 + 风险预警
- 💰 **Skill ROI 评估** - 基于真实数据计算每个 Skill 的性价比
- 🔗 **Skill 编排推荐** - 发现最优组合，避免高风险链路
- 🔄 **自我迭代机制** - 失败模式识别 + 改进处方自动生成

---

## 核心功能

### 1. 全局生态健康看板

**Bot 排行榜 Top 10**:
```
排名  Bot名称      健康度  会话数  首解率
#1    小炸弹 💣    92分    156     89%
#2    忙狗        85分    98      82%
#3    杰尼龟      78分    45      75%
...
```

**场景需求分布**:
```
数据分析:    35% ████████████
文档处理:    28% █████████
健康诊断:    22% ███████
闲聊:        15% ████
```

**高风险会话列表**:
- 失败率 > 30% 的会话
- 纠错次数 > 3 的会话

### 2. Skill ROI 评估

**核心公式**:
```python
# 平均成本
avg_cost = (avg_turns - 1) * 5 + avg_corrections * 10 + (avg_tokens / 1000)

# 业务价值权重
business_value = {
    "数据分析": 10,
    "文档处理": 8,
    "健康诊断": 5,
    "闲聊": 1
}

# ROI 得分
roi_score = 100 * (success_rate * business_value - avg_cost) / avg_cost

# 风险指数
risk_index = (1 - success_rate) * 100 + avg_corrections * 10
```

**推荐动作**:
- ROI ≥ 50 且 风险 < 20 → ✅ 保留
- ROI ≥ 20 且 风险 < 50 → 🔧 优化
- ROI < 20 或 风险 ≥ 50 → ❌ 淘汰

### 3. Skill 编排推荐

基于 L3_Skill_Run 数据，分析多 Skill 协作模式：

**最优组合 Top 5**:
```
✅ 最优组合: 数据分析 + 可视化 + 文档生成
   历史成功率: 92% (26/28)
   协作成本: 1.4x
   推荐场景: 报告生成

✅ 次优组合: 飞书搜索 + 文档创建
   历史成功率: 88% (44/50)
   协作成本: 1.2x
   推荐场景: 知识整理
```

**高风险组合**:
```
⚠️ 不推荐: 数据分析 + 文档写入 (跳过可视化)
   失败率: 60% (4/10)
   原因: 用户无法验证中间结果

⚠️ 不推荐: 网络爬虫 + API 调用
   超时率: 45% (9/20)
   原因: 双重网络依赖，容易超时
```

### 4. 失败模式识别

**自动分类失败原因**:
```
失败原因分布 (过去 7 天):
├─ Prompt 不明确: 35%
├─ 权限不足: 25%
├─ 网络超时: 20%
├─ 模型能力不足: 12%
└─ 知识缺失: 8%
```

**改进处方自动生成**:
```
【问题】文档处理场景失败率 18%

【根因】
1. Prompt 不明确 (40%)
2. 权限不足 (30%)
3. 文件格式不支持 (20%)

【处方】
1. Prompt 改为: "帮我写一份 2000 字的产品 PRD，包含背景、目标、功能三个部分"
2. 检查 Bot 是否有 drive:file:write 权限
3. 限制输入文件格式为 docx/pdf/md
```

---

## 脚本清单

| 脚本 | 大小 | 执行时间 | 功能 |
|------|------|----------|------|
| calculate-skill-roi.py | 6.6KB | 每日 21:00 | 计算 Skill ROI 评分，写入 L3_Skill_ROI |
| generate-skill-recommendations.py | 7.6KB | 每周日 20:00 | 生成 Skill 编排推荐 |

---

## 定时任务配置

```bash
# 每日 21:00 计算 Skill ROI
0 21 * * * python3 ~/.openclaw/workspace/skills/bot-platform-insights/scripts/calculate-skill-roi.py

# 每周日 20:00 生成编排推荐
0 20 * * 0 python3 ~/.openclaw/workspace/skills/bot-platform-insights/scripts/generate-skill-recommendations.py
```

---

## L3_Skill_ROI 表字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Skill名称 | 文本 | 场景分类名称 |
| 调用次数 | 数字 | 过去 7 天调用次数 |
| 成功率 | 数字 | 完成率 (0-1) |
| 平均轮数 | 数字 | 平均对话轮数 |
| 平均纠错 | 数字 | 平均纠错次数 |
| 平均Token | 数字 | 平均 Token 消耗 |
| 平均成本 | 数字 | 计算得出的成本分 |
| ROI得分 | 数字 | 性价比得分 |
| 风险指数 | 数字 | 风险评估分 |
| 推荐动作 | 单选 | 保留 / 优化 / 淘汰 |

---

## L3_Skill_Run 表字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Run ID | 文本 | 运行记录唯一 ID |
| 会话ID | 文本 | 关联的会话 ID |
| Skill名称 | 文本 | 触发的 Skill 名称 |
| 协作Skill数 | 数字 | 本次会话触发的 Skill 总数 |
| 协作成本系数 | 数字 | 1.0 + (skill_count - 1) * 0.2 |
| 完成状态 | 单选 | completed / failed / abandoned |
| 会话开始时间 | 日期 | 会话开始时间戳 |

---

## 配置

### ROI 计算参数
```json
{
  "costWeights": {
    "turnCost": 5,
    "correctionCost": 10,
    "tokenCostPer1k": 1
  },
  "businessValue": {
    "数据分析": 10,
    "文档处理": 8,
    "健康诊断": 5,
    "闲聊": 1
  }
}
```

### 推荐阈值
```json
{
  "recommendThresholds": {
    "keep": { "minROI": 50, "maxRisk": 20 },
    "optimize": { "minROI": 20, "maxRisk": 50 },
    "deprecate": { "maxROI": 20, "minRisk": 50 }
  }
}
```

---

## 相关文件

```
bot-platform-insights/
├── SKILL.md
└── scripts/
    ├── calculate-skill-roi.py
    └── generate-skill-recommendations.py
```

---

## 版本历史

### v3.0.0 (2026-03-24)
- ✨ Skill ROI 评分计算
- ✨ 多 Skill 编排推荐
- ✨ 失败模式自动识别
- ✨ 改进处方自动生成

### v2.1.0 (2026-03-18)
- 初始版本

---

## 许可证

MIT License
