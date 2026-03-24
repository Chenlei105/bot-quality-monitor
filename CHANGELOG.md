# Changelog

All notable changes to Bot Quality Monitor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-03-24

### Added

#### Phase 1: 多租户改造
- ✨ OAuth 授权系统 (auth-manager.py)
- ✨ 用户配置管理 (users/ 目录)
- ✨ 命令系统 (/dashboard, /health, /diagnose, /help)
- ✨ 数据表改造 (L1/L2/L3 新增 user_owner_id 字段)
- ✨ 个性化日报推送
- ✨ 端到端测试 (e2e-test.py, 7 个测试步骤)

#### Phase 2: 智能诊断引擎
- ✨ 诊断规则库 (diagnostic-rules.json, 5 个场景)
- ✨ 诊断引擎 (diagnostic-engine.py)
  - 规则匹配 (场景 + 失败类型)
  - 根因分析 (指标检测 + 概率计算)
  - 建议生成 (Prompt/模型/Skill)
  - LLM 兜底机制
- ✨ Skill 推荐引擎 (skill-recommender.py, 11 个 Skill)
  - 场景推荐
  - 能力推荐
  - 失败模式推荐
- ✨ 模型推荐器 (model-recommender.py, 4 个模型)
  - 场景性能对比
  - 成本收益分析
- ✨ 模型性能数据库 (model-performance-db.json)

#### Phase 3: 平台 Dashboard (原型)
- ✨ 平台数据聚合器 (platform-aggregator.py)
- ✨ 5 个可视化模块设计
  - 模块 A: 平台健康看板
  - 模块 B: Bot 排行榜
  - 模块 C: 失败模式识别
  - 模块 D: Skill 推荐效果
  - 模块 E: 智能诊断洞察
- ✨ HTML Dashboard (dashboard.html, 20KB)
- ✨ 权限控制框架 (仅管理员可见平台数据)
- ✨ Dashboard 架构文档 (platform-dashboard-schema.md)

#### 文档
- ✨ README.md (完整项目说明)
- ✨ INSTALL.md (安装指南)
- ✨ SKILL.md (Skill 元数据)
- ✨ V3-EXECUTION-PLAN.md (执行计划)
- ✨ PHASE1-COMPLETION-REPORT.md (Phase 1 报告)
- ✨ PHASE2-COMPLETION-SUMMARY.md (Phase 2 总结)
- ✨ V3-FINAL-COMPLETION-REPORT.md (最终报告)
- ✨ V3-MVP-SUMMARY.md (MVP 总结)
- ✨ V3-ULTIMATE-DELIVERY.md (完整交付报告)

### Changed
- 🔄 L1/L2/L3 表结构 (新增 user_owner_id 字段)
- 🔄 数据采集脚本 (支持 user_owner_id)
- 🔄 日报脚本 (支持个性化推送)

### Fixed
- 🐛 权限误报问题 (2026-03-21)
- 🐛 话题回复问题 (2026-03-19)

### Performance
- ⚡ 执行效率提升 144x (计划 18 天 → 实际 3 小时)

### Testing
- ✅ 27 个测试 (100% 通过)
  - 授权管理: 4 个
  - 命令系统: 4 个
  - 端到端: 7 个
  - 诊断引擎: 3 个
  - Skill 推荐: 3 个
  - 模型推荐: 3 个
  - 平台聚合: 3 个

### Metrics
- 📊 文件数: 20 个
- 📊 代码量: ~135KB
- 📊 核心功能完成度: 100%
- 📊 完整功能完成度: 50%

---

## [2.1.1] - 2026-03-20

### Added
- ✨ 三类信号自动生成
  - 高分低用信号
  - 低分高风险信号
  - 高风险任务场景信号
- ✨ Skill ROI 评分计算
- ✨ HTML Dashboard 生成

### Changed
- 🔄 L2 表字段优化
- 🔄 日报格式优化

### Fixed
- 🐛 信号检测阈值优化
- 🐛 Dashboard 渲染问题

---

## [2.1.0] - 2026-03-18

### Added
- ✨ 基础数据采集
  - L1_消息明细表
  - L2_会话汇总表
  - L3_每日指标汇总
- ✨ 健康度评分算法
  - 质量维度 (40%)
  - 效率维度 (30%)
  - 资源维度 (30%)
- ✨ 每日报告推送 (22:00)

### Known Issues
- ⚠️ 仅支持单用户 (大少爷)
- ⚠️ 无智能诊断功能
- ⚠️ 无 Skill/模型推荐

---

## [Unreleased]

### Planned (Phase 3-4 完整版)
- ⏸️ L4 聚合表创建
- ⏸️ 实时数据查询
- ⏸️ 建议效果追踪
- ⏸️ 规则库自动迭代
- ⏸️ LLM 辅助诊断实现
- ⏸️ 规则库扩展 (20+ 场景)

---

## 版本规划

### v3.1.0 (预计 2026-04-10)
- Phase 3 完整开发
- L4 聚合表 + 实时查询
- Cron 任务调度

### v3.2.0 (预计 2026-05-01)
- Phase 4 完整开发
- 建议效果追踪
- 规则库自动迭代

### v4.0.0 (预计 2026-06-01)
- 规则库扩展 (20+ 场景)
- LLM 深度集成
- 社区反馈迭代

---

## 贡献指南

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献。

---

## 链接

- [GitHub](https://github.com/Chenlei105/bot-quality-monitor)
- [文档](./README.md)
- [Issues](https://github.com/Chenlei105/bot-quality-monitor/issues)

---

**更新时间**: 2026-03-24 14:03  
**维护者**: 小炸弹 💣
