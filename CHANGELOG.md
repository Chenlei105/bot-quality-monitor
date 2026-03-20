# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-03-20

### Added
- ✨ 三类智能信号提示功能
  - 高分低用 Bot 检测（health_score >= 85 AND weekly_trigger_count <= 5）
  - 低分高风险 Bot 检测（correction_rate >= 0.10 OR failure_count >= 5）
  - 高风险任务场景检测（scenario_failure_rate >= 0.30 AND sample_count >= 5）
- ✨ HTML Dashboard 生成功能
  - Plotly 交互式图表（仪表盘 + 趋势图）
  - 渐变背景 + 响应式布局
  - 一键生成：`python3 scripts/generate-dashboard.py`
- ✨ Skill ROI 评分机制
  - 公式：`ROI = 100 × (success_rate × business_value - avg_cost) / avg_cost`
  - 成本视角看性价比
- ✨ 多 Skill 协作分析
  - L2 会话按 Skill 拆分为 N 条 L3_Skill_Run 记录
  - 协作成本系数 = 1.0 + (skill_count - 1) × 0.2
  - Skill 编排推荐（最优组合 + 不推荐组合）
- ✨ 会话切割优化
  - 时间窗口 + 任务边界双约束
  - 解决开会回来追问误判问题

### Changed
- 🔄 L2_会话汇总表新增 3 个字段
  - Skill数量（Number）
  - 协作成本系数（Number）
  - 关键路径（Checkbox）
- 🔄 L3 数据架构扩展
  - 新增 L3_Signal_Alerts 表（12 个字段）
  - 新增 L3_Skill_ROI 表（10 个字段）
  - 新增 L3_Skill_Run 表（7 个字段）
- 🔄 bot-daily-report 新增模块 F（智能行动建议）
- 🔄 bot-platform-insights 新增模块 D（Skill 编排推荐）

### Development
- 🚀 开发用时：6.5 小时（预估 6 天，加速 7.4x）
- ✅ 端到端测试覆盖率：100%（5/5）
- 📝 完整文档：7 个 Markdown 文件（~30KB）

---

## [2.0.0] - 2026-03-18

### Added
- ✨ 生产化改造
  - App Token 配置化（支持环境变量）
  - 隐私保护（默认不存消息内容）
  - 写入队列 + 降级模式
- ✨ 实时触发机制
  - 每次对话后自动采集数据
  - L1/L2 实时写入
- ✨ 归档机制
  - 每日凌晨 3:00 自动生成 L3 汇总数据

### Changed
- 🔄 配置文件迁移到 `~/.openclaw/skills/bot-analytics-shared/config.yaml`
- 🔄 支持多租户配置（通过环境变量隔离）

---

## [1.0.0] - 2026-03-18

### Added
- 🎉 初版发布
- ✨ 三维度健康度评分体系
  - 质量（40%）：纠错率≤5%、首解率≥80%、好评率≥90%
  - 效率（30%）：任务完成率≥80%、响应速度≤3秒
  - 资源（30%）：API成功率≥99%、错误频率≤5次/天
- ✨ 每日质量日报
  - 飞书私信推送
  - 麦肯锡风格报告
- ✨ 平台洞察周报
  - Bot 排行榜 Top 5
  - 失败模式识别
  - Skill 自我迭代建议
- ✨ 数据采集层
  - 7 步流程（会话检测 → 场景分类 → 质量评估 → 数据写入）
  - L1/L2/L3 三层数据模型

### Development
- 📊 数据架构：3 张表（L1/L2/L3_daily）
- 🛠️ 核心 Skill：
  - bot-analytics-collector v1.0.0
  - bot-daily-report v1.0.0
  - bot-platform-insights v1.0.0

---

## 版本号说明

- **主版本号（Major）**：重大架构变更、不兼容更新
- **次版本号（Minor）**：新增功能、向后兼容
- **修订号（Patch）**：Bug 修复、文档更新

---

[2.1.0]: https://github.com/chenlei/bot-quality-monitor/releases/tag/v2.1.0
[2.0.0]: https://github.com/chenlei/bot-quality-monitor/releases/tag/v2.0.0
[1.0.0]: https://github.com/chenlei/bot-quality-monitor/releases/tag/v1.0.0
