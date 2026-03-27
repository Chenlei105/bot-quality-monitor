# Changelog

## [5.0.0] - 2026-03-27

### 🎉 重大更新

#### 核心架构重构
- ✅ **完整字段设计**：100+ 个字段覆盖所有指标（L2 35个 + L3 25个 + 信号 8个 + Skill 7个）
- ✅ **数据隔离**：用户私有数据 vs 中央平台数据完全隔离
- ✅ **Heartbeat 引擎**：自动执行所有定时任务（每分钟/每小时/每日/每周）
- ✅ **新增 L3_年度汇总表**：支持年度数据统计

#### 用户日报系统（全新）
- ✅ **飞书卡片日报**：科技蓝风格，5 大模块（执行摘要 + 用户使用 + 趋势对比 + 智能洞察 + 优先行动）
- ✅ **Dashboard HTML**：白色背景，ECharts 图表，完整交互式数据看板
- ✅ **详细文档**：Markdown 格式，自动创建飞书云文档，5 大模块完整分析
- ✅ **自动推送**：每日 22:00 自动推送（卡片 + 文档链接 + Dashboard 链接）

#### 平台日报系统（全新，给大少爷）
- ✅ **Skill ROI 计算**：自动计算所有 Skill 的性价比评分
- ✅ **平台 Dashboard**：紫色渐变背景，Bot 排行榜 + Skill 使用 Top 10 + 失败模式分布
- ✅ **自动推送**：每周日 20:00 自动推送给大少爷

#### 自动化能力
- ✅ **会话数据自动采集**：每分钟自动采集最近活跃的会话，写入用户自己的表格
- ✅ **Webhook 自动入库**：每 10 分钟自动搜索 Webhook 消息并写入中央表格
- ✅ **测试数据生成**：自动生成 70 条完整测试数据（7 天 × 10 条/天）

### 🔧 修复问题

#### P0 级别（致命问题）
1. ✅ 修复表格字段严重缺失问题（从 3 个字段 → 100+ 个字段）
2. ✅ 修复脚本硬编码中央表格 ID 问题（改为从 config.json 读取）
3. ✅ 修复缺少 L3_年度汇总表问题
4. ✅ 修复关键脚本缺失问题（generate-daily-report.py 等）

#### P1 级别（重要问题）
5. ✅ 修复字段名不一致问题（session_start vs 开始时间）
6. ✅ 修复 send-personalized-report.py 无 main 入口问题

#### P2 级别（次要问题）
7. ✅ 优化测试数据（从 3 条 → 70 条）
8. ✅ 完善 HEARTBEAT.md 配置文档

### 📦 新增脚本（11 个）

#### Batch 1: 核心基础（4 个）
- `scripts/auto-setup-v5.py` - 全自动安装脚本（100+ 字段 + 70 条测试数据）
- `scripts/collect-sessions.py` - 会话数据自动采集（修复硬编码）
- `scripts/heartbeat-runner.py` - Heartbeat 自动执行引擎
- `HEARTBEAT.md` - 完善配置文档

#### Batch 2: 用户日报（4 个）
- `scripts/generate-daily-report.py` - 飞书卡片日报生成器
- `scripts/generate-dashboard.py` - Dashboard HTML 生成器
- `scripts/generate-detailed-report.py` - 详细文档生成器
- `scripts/send-personalized-report-v5.py` - 日报推送脚本

#### Batch 3: 平台日报（3 个）
- `scripts/calculate-skill-roi.py` - Skill ROI 计算器
- `scripts/generate-platform-dashboard.py` - 平台 Dashboard 生成器
- `scripts/send-platform-report.py` - 平台日报推送脚本

### 🎨 设计参考

#### 飞书卡片（参考第一张图）
- **配色**：科技蓝 #1677FF + 红黄绿语义化
- **布局**：5 大模块垂直流动式布局
- **交互**：底部行动点（详细报告 + Dashboard 链接）

#### Dashboard HTML（参考第二张图）
- **背景**：白色 #FFFFFF + 浅灰卡片
- **图表**：ECharts 默认主题（浅色）
- **布局**：顶部指标栏 + 2x2 网格 + 底部表格

#### 平台 Dashboard
- **背景**：紫色渐变（#667eea → #764ba2）
- **卡片**：玻璃质感（backdrop-filter）
- **图表**：ECharts + 金色/银色/铜色排名

### 📊 数据流向

#### 用户私有数据
```
collect-sessions.py（每分钟）
  → 用户自己的 L2_会话汇总表
  → generate-daily-report.py（每日 22:00）
  → 推送给用户自己
```

#### 中央平台数据
```
track-usage.py sync（每小时）
  → 飞书 Webhook
  → process-webhook-messages.py（每 10 分钟）
  → 大少爷的中央表格（Xw4Tb5C8KagMiQswkdacNfVPn8e）
  → send-platform-report.py（每周日 20:00）
  → 推送给大少爷
```

### 🔗 相关链接

- GitHub: https://github.com/Chenlei105/bot-quality-monitor
- Commit e172bb4: Batch 1 核心基础修复
- Commit 4ae064c: Batch 2.1 飞书卡片生成器
- Commit 97326a7: Batch 2.2 Dashboard + 详细文档
- Commit 4173c8d: Batch 3 平台日报

---

## [4.0.1] - 2026-03-26

### 修复
- 修复三个致命问题（会话采集 + Webhook 入库 + 安装流程）
- 整理 GitHub 文件结构（删除 6 个内部文档，归档 6 个历史文档）

### 新增
- `scripts/collect-sessions.py` - 本地会话数据自动采集
- `scripts/process-webhook-messages.py` - Webhook 自动入库
- `scripts/auto-setup.py` - 一句话安装

---

## [3.0.1] - 2026-03-25

### 新增
- 三类智能信号检测（高分低用、首解率下降、知识缺失）
- P0/P1/P2 Dashboard
- Skill ROI 分析

---

**查看完整历史**: [.archive/HISTORY.md](.archive/HISTORY.md)
