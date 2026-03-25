# Bot Quality Monitor v4.0.0 发布说明

**发布日期**: 2026-03-25  
**重大更新**: 三层 Dashboard + 自动化数据采集 + 归档机制

---

## 🎉 核心亮点

### 1. P0/P1/P2 三层 Dashboard 系统

全新的三层数据架构，满足不同时间跨度的数据分析需求：

#### P0 热数据层 - 用户个人健康度看板

- **数据范围**: 最近 7 天
- **生成时机**: 每日 22:00 自动生成
- **推送对象**: 每个用户
- **核心模块（6 个）**:
  1. 综合健康度仪表盘 (Gauge Chart)
  2. 三维度雷达图 (Radar Chart)
  3. 7 天趋势折线图 (Line Chart)
  4. 场景健康度热力图 (Heatmap)
  5. 三类智能信号卡片 (Cards)
  6. 失败案例 Top 10 + 诊断建议 (Table)

#### P1 温数据层 - 全局管理看板

- **数据范围**: 最近 30 天
- **生成时机**: 每周日 20:00 自动生成
- **推送对象**: 管理员（大少爷）
- **核心模块（5 个）**:
  1. 全局统计概览 (8 个卡片)
  2. Bot 健康度排行榜 Top 20
  3. Skill 使用排行榜 (Bar + Line Chart)
  4. 用户活跃度分析 (Pie + Line Chart)

#### P2 冷数据层 - 历史归档看板

- **数据范围**: 90 天 ~ 全年
- **生成时机**: 每月/季度/年度自动生成
- **推送对象**: 管理员 + 决策层
- **核心模块（8 个）**:
  1. 时间范围选择器
  2. Bot 成长曲线（全年健康度趋势）
  3. 季度健康度对比（柱状图 + 环比增长率）
  4. 用户生命周期分析（漏斗图）
  5. Skill 生命周期热力图
  6. 同比/环比健康度变化
  7. 长期失败模式识别
  8. 年度 Top 10 榜单

---

### 2. 自动化数据采集系统

完全自动化的 Session Hook 机制，无需手动触发：

#### 核心功能

- **Heartbeat 触发**: 每次 Heartbeat（约每分钟）自动检查新会话
- **智能去重**: 基于 `collected-sessions.json` 避免重复采集
- **场景识别引擎**: 8 种场景智能分类（健康诊断/数据分析/文档处理/技能管理/配置咨询/搜索查询/代码调试/闲聊）
- **信号检测**: 纠错信号/完成状态/满意度自动识别

#### 数据流

```
用户对话
    ↓
Heartbeat 检测新会话
    ↓
sessions_list + sessions_history
    ↓
场景识别 + 信号检测
    ↓
写入 L2_会话汇总表
    ↓
记录到 collected-sessions.json
```

---

### 3. 数据归档机制

自动归档超期数据，防止数据表膨胀：

#### 归档策略

- **L2 会话数据**: 超过 180 天 → 移至 L2_会话归档表
- **L1 消息数据**: 超过 90 天 → 移至 L1_消息归档表
- **月度汇总**: 每月 1 日自动生成 → 写入 L3_月度汇总表
- **季度汇总**: 每季度首日自动生成 → 写入 L3_季度汇总表
- **年度汇总**: 每年 1 月 1 日自动生成 → 写入 L3_年度汇总表

#### 定时任务

- **每月 1 日 02:00**: 执行归档 + 生成月度汇总
- **每季度首日 08:00**: 生成季度总结报告
- **每年 1 月 1 日 08:00**: 生成年度总结报告

---

### 4. 可视化增强

全面升级的图表库和交互体验：

#### 技术栈

- **Plotly 5.x**: 交互式图表（仪表盘/雷达图/热力图/折线图）
- **Jinja2 3.x**: HTML 模板引擎
- **Bootstrap 5**: 响应式布局
- **DataTables.js**: 可排序、可搜索的表格

#### 特性

- **独立 HTML 文件**: 可离线查看，无需服务器
- **交互式探索**: 鼠标悬停显示详情，支持缩放/平移
- **移动端适配**: 响应式布局（计划中）

---

## 📂 新增文件

```
bot-quality-monitor/
├── PROJECT_OVERVIEW.md                 # 项目总览（新增）
├── INTEGRATION_GUIDE.md                # 数据集成指南（新增）
├── RELEASE_v4.0.0.md                   # 本文档（新增）
│
├── bot-analytics-collector/
│   ├── auto-collect.py                 # Session Hook 自动采集（新增）
│   ├── scene-classifier.py             # 场景识别引擎（新增）
│   └── daily-aggregation.py            # 每日指标汇总（新增）
│
├── p0-dashboard/
│   ├── README.md                       # P0 说明文档（新增）
│   └── generate-p0-dashboard.py        # P0 Dashboard 生成（新增）
│
├── p1-dashboard/
│   └── generate-p1-dashboard.py        # P1 Dashboard 生成（新增）
│
├── p2-dashboard/
│   └── generate-p2-dashboard.py        # P2 Dashboard 生成（新增）
│
└── archive-scripts/
    └── archive-old-data.py             # 数据归档脚本（新增）
```

---

## 🗓️ 定时任务总览

| 时间 | 任务 | 脚本 |
|------|------|------|
| **每分钟** | Session Hook 采集 | HEARTBEAT.md |
| **每天 23:00** | 每日指标汇总 | daily-aggregation.py |
| **每天 22:00** | P0 Dashboard 生成 | generate-p0-dashboard.py |
| **每周日 20:00** | P1 Dashboard 生成 | generate-p1-dashboard.py |
| **每月 1 日 08:00** | P2 月度报告 | generate-p2-dashboard.py --type=monthly |
| **每季度首日 08:00** | P2 季度报告 | generate-p2-dashboard.py --type=quarterly |
| **每年 1 月 1 日 08:00** | P2 年度报告 | generate-p2-dashboard.py --type=yearly |
| **每月 1 日 02:00** | 数据归档 | archive-old-data.py |

---

## 📊 新增数据表

**App Token**: `Xw4Tb5C8KagMiQswkdacNfVPn8e`

| 表名 | Table ID | 用途 |
|------|----------|------|
| **L2_会话归档** | `tblVpIiKTryvHeKM` | 存储超过 180 天的会话数据 |
| **L1_消息归档** | `tblNz0ljUFcr5ED4` | 存储超过 90 天的消息数据 |
| **L3_月度汇总** | `tblV47g7vuPaJwda` | 每月聚合数据 |
| **L3_季度汇总** | `tblY9LPu84HVW3Oj` | 每季度聚合数据 |
| **L3_年度汇总** | `tblX1p8UtCH8kLVr` | 每年聚合数据 |

---

## ⬆️ 升级指南

### 从 v3.x 升级

#### 方法 1：Git Pull（推荐）

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main
```

#### 方法 2：重新克隆

```bash
cd ~/.openclaw/workspace/skills
mv bot-quality-monitor bot-quality-monitor.backup
git clone https://github.com/Chenlei105/bot-quality-monitor.git
cd bot-quality-monitor
./hooks/install.sh
```

### 依赖安装

v4.0 新增 Python 依赖：

```bash
pip3 install plotly jinja2
```

### 验证升级

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor

# 检查版本
cat package.json | grep version
# 应显示: "version": "4.0.0"

# 测试 P0 Dashboard 生成
python3 p0-dashboard/generate-p0-dashboard.py

# 检查生成的文件
ls -lh ~/.openclaw/workspace/reports/p0-dashboard-*.html
```

---

## 🐛 已知问题

### 1. Dashboard 数据为空

**现象**: 生成的 Dashboard 显示"暂无数据"

**原因**: L3_每日指标汇总表为空（数据采集功能刚启用）

**解决方案**: 等待自动采集积累数据（24小时后会有首日数据）

---

### 2. Plotly 图表不显示

**现象**: HTML 打开后图表区域空白

**原因**: Plotly CDN 无法访问

**解决方案**: 检查网络连接，确保能访问 `https://cdn.plot.ly/plotly-2.18.0.min.js`

---

### 3. 定时任务未触发

**现象**: 到了设定时间但 Dashboard 未生成

**原因**: Cron 任务配置问题

**解决方案**:

```bash
# 检查 Cron 配置
crontab -l | grep "bot-quality-monitor"

# 手动触发测试
/usr/bin/python3 ~/.openclaw/workspace/skills/bot-quality-monitor/p0-dashboard/generate-p0-dashboard.py
```

---

## 🔄 Breaking Changes

### 1. 数据表结构变更

v4.0 新增了 5 张归档表，原有表结构不变，**向后兼容**。

### 2. 配置文件迁移

无需手动迁移，所有配置自动继承。

### 3. API 变更

无 API 变更，所有脚本独立运行。

---

## 🙏 致谢

感谢所有使用和反馈的用户！

特别感谢：
- **大少爷（陈磊）** - 产品设计与需求梳理
- **小炸弹 💣** - 技术实现与开发

---

## 📞 支持

- **GitHub Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **GitHub Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions
- **飞书文档**: https://www.feishu.cn/docx/NCDKdMNSzorSEOxHYodcmDLtnSf

---

**让您的 Bot 更智能、更健康！** 🚀
