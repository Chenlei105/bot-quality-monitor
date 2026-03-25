# Bot Quality Monitor v4.0

**全自动 Bot 健康监控与优化系统** - P0/P1/P2 三层 Dashboard + 智能信号检测

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/Chenlei105/bot-quality-monitor/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📊 使用统计

本 Skill 包含匿名使用统计功能，帮助我们改进产品。

**我们收集什么**：
- 事件类型（安装/运行）
- Skill 版本
- 匿名用户标识（机器特征的 hash，无法追溯真实身份）
- 操作系统类型

**我们不收集**：
- 任何对话内容
- 真实用户 ID 或个人信息
- 文件内容或敏感数据

**如何关闭**：
```bash
export SKILL_TRACKING=off
```

---

## 概述

Bot Quality Monitor 是一个全自动的 Bot 健康监控与优化系统，为您的 Bot 提供：

- 📊 **自动健康监控** - 每日采集对话数据，生成三维度健康度报告
- 🔔 **智能预警提示** - 自动识别问题 (高分低用、低分高风险、高风险场景)
- 💡 **明确改进建议** - 基于真实数据生成 Skill ROI 评分和编排推荐
- 📈 **可视化 Dashboard** - Plotly 交互式图表展示 Bot 健康状况

---

## 架构

```
用户对话
    ↓
bot-analytics-collector (数据采集层)
    ↓
L1 消息明细 / L2 会话汇总
    ↓
bot-daily-report (报告生成层)
    ├─ 三维度健康度计算
    ├─ 三类智能信号检测
    └─ HTML Dashboard 生成
    ↓
bot-platform-insights (平台洞察层)
    ├─ Skill ROI 评分
    └─ 多 Skill 编排推荐
    ↓
每日 22:00 推送日报
```

---

## Skill 组成

| Skill | 版本 | 说明 |
|-------|------|------|
| **bot-quality-monitor** | v4.0.0 | 元包（一键安装入口） |
| **bot-analytics-collector** | v4.0.0 | 数据采集层：消息采集 + 会话切割 + 信号识别 |
| **bot-daily-report** | v4.0.0 | 报告生成层：健康度日报 + HTML Dashboard + 智能信号 |
| **bot-platform-insights** | v4.0.0 | 平台洞察层：Skill ROI + 编排推荐 + 失败模式识别 |

---

## 快速开始

### 安装

```bash
openclaw skill install bot-quality-monitor
```

### 配置

安装完成后，**对你的 Bot 说一句话**：
> 帮我创建 Bot 质量监控数据表

Bot 会全自动完成：
1. 创建飞书多维表格应用
2. 自动创建 12 张数据表
3. 自动生成完整配置
4. 设置好定时任务

**全程 10 秒，不需要你做任何其他操作！**

### 查看日报

每日 22:00 自动推送健康度日报到您的飞书私信。

---

## 核心功能

### 三维度健康度评分

**质量维度（40%）**:
- 首解率 (越高越好)
- 纠错率 (越低越好)
- 知识召回率

**效率维度（30%）**:
- 任务完成率
- 响应速度
- 对话轮数

**资源维度（30%）**:
- API 成功率
- Token 消耗
- 错误率

```
综合健康度 = 质量×0.40 + 效率×0.30 + 资源×0.30

评级: ≥90 🟢优秀 / ≥75 🟡良好 / ≥60 🟠待改善 / <60 🔴需关注
```

### 三类智能信号

| 信号类型 | 检测条件 | 建议 |
|----------|----------|------|
| 🌟 高分低用 Bot | 健康度≥85 且 周触发≤5 | Bot 质量很好但用得太少 |
| ⚠️ 低分高风险 Bot | 纠错率≥10% 或 失败≥5次 | Bot 错误率太高，需要优化 |
| 🔥 高风险任务场景 | 失败率≥30% 且 样本≥5 | 该场景失败率过高 |

### Skill ROI 评分

基于真实运行数据，计算每个 Skill 的性价比：

```python
ROI得分 = 100 × (成功率×业务价值 - 平均成本) / 平均成本

推荐动作:
- ROI ≥ 50 → ✅ 保留
- ROI ≥ 20 → 🔧 优化
- ROI < 20 → ❌ 淘汰
```

---

## 数据表结构

| 表名 | 层级 | 说明 |
|------|------|------|
| **L0_Skill_Usage** | 统计层 | Skill 使用统计 |
| **L1_消息明细表** | 原始层 | 每条消息一行，保留原始记录 |
| **L2_会话汇总表** | 加工层 | 每个会话一行，指标计算 |
| **L3_每日指标汇总** | 应用层 | Bot 排行榜数据 |
| **L3_Signal_Alerts** | 应用层 | 三类智能信号 |
| **L3_Skill_ROI** | 应用层 | Skill 性价比评分 |
| **L3_Skill_Run** | 应用层 | 多 Skill 协作记录 |
| **L2_会话归档** | 归档层 | 超过 180 天的会话归档 |
| **L1_消息归档** | 归档层 | 超过 90 天的消息归档 |
| **L3_月度汇总** | 聚合层 | 每月聚合数据 |
| **L3_季度汇总** | 聚合层 | 每季度聚合数据 |
| **L3_年度汇总** | 聚合层 | 每年聚合数据 |

---

## 定时任务

所有定时任务通过 **OpenClaw 原生 Heartbeat** 自动触发，**无需手动配置 crontab**：

| 时间 | 任务 |
|------|------|
| 每分钟 | Session Hook 自动采集对话数据 |
| 每日 21:00 | 生成三类信号 + 计算 Skill ROI |
| 每日 22:00 | 生成日报 + HTML Dashboard + 推送 |
| 每日 02:00 | Skill 使用数据同步 |
| 每周日 20:00 | 生成 Skill 编排推荐 |
| 每月 1 日 02:00 | 数据归档（L1/L2 超期数据） |

---

## 隐私保护

- ✅ 数据完全隔离，只有您能看到
- ✅ 数据存在您自己的飞书多维表格
- ✅ 不存储消息原文，只存储统计数据
- ✅ 随时可删除所有数据

---

## 版本历史

### v4.0.0 (2026-03-25)
- 🚀 P0/P1/P2 三层 Dashboard 系统
- 🚀 自动化数据采集（Session Hook）
- 🚀 数据归档机制（L1/L2 超期归档）
- 🚀 场景识别引擎（8 种场景智能分类）
- 🚀 月度/季度/年度汇总报告
- 🚀 Plotly 交互式图表
- 🚀 完全自动化，无需手动触发

### v3.0.0 (2026-03-24)
- ✨ 三层数据架构（L1/L2/L3）
- ✨ 三类智能信号自动检测
- ✨ Skill ROI 评分计算
- ✨ 多 Skill 编排推荐
- ✨ HTML 可视化 Dashboard
- ✨ 麦肯锡风格日报

### v2.1.0 (2026-03-18)
- 初始版本

---

## 贡献者

- **陈磊** - 产品设计
- **小炸弹 💣** - 技术实现

---

## 许可证

MIT License

---

## 相关链接

### 文档

- **项目总览**: [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- **安装指南**: [INSTALL.md](./INSTALL.md)
- **更新指南**: [UPDATE_GUIDE.md](./UPDATE_GUIDE.md)
- **集成指南**: [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
- **发布说明**: [RELEASE_v4.0.0.md](./RELEASE_v4.0.0.md)

### GitHub

- **仓库**: https://github.com/Chenlei105/bot-quality-monitor
- **Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions

### 飞书文档

- **PRD 产品需求**: https://www.feishu.cn/docx/LItfdgwQkovevexHxbTcFKkAnne
- **技术设计**: https://www.feishu.cn/docx/GQv3dhvFCogxRHxrZwTcLe6EnUv
- **Dashboard 设计**: https://www.feishu.cn/docx/NCDKdMNSzorSEOxHYodcmDLtnSf

---

**让您的 Bot 更智能、更健康！** 🚀
