# Bot Quality Monitor v4.0 - 项目总览

> **全自动 Bot 健康监控与优化系统**  
> 三层 Dashboard + 智能信号检测 + 自动化数据采集

---

## 📚 核心文档索引

### 用户文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **README.md** | 项目介绍 + 快速开始 | [查看](./README.md) |
| **INSTALL.md** | 安装指南（首次安装） | [查看](./INSTALL.md) |
| **UPDATE_GUIDE.md** | 更新指南（v3.x → v4.0） | [查看](./UPDATE_GUIDE.md) |
| **DATA_TRACKING.md** | 隐私说明 + 数据上报 | [查看](./scripts/DATA_TRACKING.md) |

### 开发文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **INTEGRATION_GUIDE.md** | 真实数据集成指南 | [查看](./INTEGRATION_GUIDE.md) |
| **CHANGELOG.md** | 版本历史 | [查看](./CHANGELOG.md) |
| **RELEASE_v4.0.0.md** | v4.0 发布说明 | [查看](./RELEASE_v4.0.0.md) |

### 飞书文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **PRD 产品需求文档** | 完整需求规格说明 | [飞书文档](https://www.feishu.cn/docx/LItfdgwQkovevexHxbTcFKkAnne) |
| **技术设计文档** | 数据架构 + API 设计 | [飞书文档](https://www.feishu.cn/docx/GQv3dhvFCogxRHxrZwTcLe6EnUv) |
| **Dashboard 设计方案** | P0/P1/P2 三层设计 | [飞书文档](https://www.feishu.cn/docx/NCDKdMNSzorSEOxHYodcmDLtnSf) |

---

## 🏗️ 项目架构

### 三层数据架构

```
L1 消息明细 (90天保留)
    ↓
L2 会话汇总 (180天保留)
    ↓
L3 业务智能 (永久保留)
    ├── L3_每日指标汇总
    ├── L3_Signal_Alerts (三类智能信号)
    ├── L3_Skill_ROI (Skill 性价比评分)
    └── L3_Skill_Run (多 Skill 协作记录)
```

### 三层 Dashboard

```
P0 热数据层 (最近 7 天)
    ├── 用户个人健康度看板
    ├── 6 个模块 (仪表盘/雷达图/趋势/热力图/信号/失败案例)
    └── 每日 22:00 自动生成

P1 温数据层 (最近 30 天)
    ├── 全局管理看板
    ├── 5 个模块 (概览/排行榜/Skill使用/活跃度)
    └── 每周日 20:00 自动生成

P2 冷数据层 (90天 ~ 全年)
    ├── 历史归档看板
    ├── 8 个模块 (成长曲线/季度对比/生命周期/Top10)
    └── 每月/季度/年度自动生成
```

---

## 📂 目录结构

```
bot-quality-monitor/
├── README.md                           # 项目介绍
├── PROJECT_OVERVIEW.md                 # 本文档（项目总览）
├── INSTALL.md                          # 安装指南
├── UPDATE_GUIDE.md                     # 更新指南
├── INTEGRATION_GUIDE.md                # 数据集成指南
├── CHANGELOG.md                        # 版本历史
├── package.json                        # NPM 包配置
├── SKILL.md                            # OpenClaw Skill 定义
│
├── hooks/                              # 安装/卸载钩子
│   ├── install.sh                      # 安装时自动埋点
│   └── uninstall.sh                    # 卸载时自动埋点
│
├── scripts/                            # 工具脚本
│   ├── track-usage.py                  # 使用统计埋点
│   └── DATA_TRACKING.md                # 隐私说明文档
│
├── bot-analytics-collector/            # 数据采集层
│   ├── SKILL.md                        # Skill 说明
│   ├── auto-collect.py                 # Session Hook 自动采集
│   ├── scene-classifier.py             # 场景识别引擎
│   ├── daily-aggregation.py            # 每日指标汇总
│   └── collect-with-user-id.py         # 多租户采集（旧版）
│
├── bot-daily-report/                   # 日报生成层
│   ├── SKILL.md                        # Skill 说明
│   ├── send-personalized-report.py     # 个性化日报推送
│   └── scripts/
│       ├── generate-signal-alerts.py   # 三类信号检测
│       ├── generate-html-dashboard.py  # HTML Dashboard
│       └── generate-static-dashboard.py # 静态图表
│
├── bot-platform-insights/              # 平台洞察层
│   ├── SKILL.md                        # Skill 说明
│   └── scripts/
│       ├── calculate-skill-roi.py      # Skill ROI 计算
│       └── generate-skill-recommendations.py # 编排推荐
│
├── p0-dashboard/                       # P0 热数据层
│   ├── README.md                       # 模块说明
│   └── generate-p0-dashboard.py        # P0 Dashboard 生成
│
├── p1-dashboard/                       # P1 温数据层
│   └── generate-p1-dashboard.py        # P1 Dashboard 生成
│
├── p2-dashboard/                       # P2 冷数据层
│   └── generate-p2-dashboard.py        # P2 Dashboard 生成
│
└── archive-scripts/                    # 数据归档脚本
    └── archive-old-data.py             # 自动归档（每月1日）
```

---

## 🔧 核心脚本说明

### 数据采集 (bot-analytics-collector)

| 脚本 | 功能 | 触发方式 |
|------|------|----------|
| **auto-collect.py** | Session Hook 自动采集 | Heartbeat（每分钟） |
| **scene-classifier.py** | 场景识别 + 信号检测 | auto-collect 调用 |
| **daily-aggregation.py** | 每日指标汇总 | Cron（每天 23:00） |

### Dashboard 生成

| 脚本 | 功能 | 触发方式 |
|------|------|----------|
| **generate-p0-dashboard.py** | P0 个人看板 | Cron（每天 22:00） |
| **generate-p1-dashboard.py** | P1 全局看板 | Cron（每周日 20:00） |
| **generate-p2-dashboard.py** | P2 归档看板 | Cron（每月/季度/年度） |

### 数据归档

| 脚本 | 功能 | 触发方式 |
|------|------|----------|
| **archive-old-data.py** | L1/L2 数据归档 + L3 汇总 | Cron（每月 1 日 02:00） |

---

## 🕐 定时任务总览

| 时间 | 任务 | 脚本 | 日志 |
|------|------|------|------|
| **每分钟** | Session Hook 采集 | HEARTBEAT.md | N/A (静默) |
| **每天 23:00** | 每日指标汇总 | daily-aggregation.py | `logs/daily-aggregation.log` |
| **每天 22:00** | P0 Dashboard 生成 | generate-p0-dashboard.py | `logs/p0-dashboard.log` |
| **每周日 20:00** | P1 Dashboard 生成 | generate-p1-dashboard.py | `logs/p1-dashboard.log` |
| **每月 1 日 08:00** | P2 月度报告 | generate-p2-dashboard.py | `logs/p2-monthly.log` |
| **每季度首日 08:00** | P2 季度报告 | generate-p2-dashboard.py | `logs/p2-quarterly.log` |
| **每年 1 月 1 日 08:00** | P2 年度报告 | generate-p2-dashboard.py | `logs/p2-yearly.log` |
| **每月 1 日 02:00** | 数据归档 | archive-old-data.py | `logs/data-archive.log` |
| **每天 02:00** | Skill 使用数据同步 | HEARTBEAT.md | N/A (静默) |

---

## 📊 飞书多维表格结构

**App Token**: `Xw4Tb5C8KagMiQswkdacNfVPn8e`

| 表名 | Table ID | 层级 | 数据量 | 保留期 |
|------|----------|------|--------|--------|
| **L1_消息明细** | `tblmKO3HejbWpUWe` | L1 | 大 | 90 天 |
| **L2_会话汇总** | `tblT0I1nCFhbpvGa` | L2 | 中 | 180 天 |
| **L3_每日指标汇总** | `tbldgJxU6QUSjnf6` | L3 | 小 | 永久 |
| **L3_Signal_Alerts** | `tblVDILmtu1oYRTE` | L3 | 小 | 永久 |
| **L3_Skill_ROI** | `tblvmjcMrdtSFF8D` | L3 | 小 | 永久 |
| **L3_Skill_Run** | `tblNsP1QdGRPCHXj` | L3 | 中 | 30 天 |
| **L0_Skill_Usage** | `tbllGdVAIIzITahT` | L0 | 小 | 永久 |
| **L2_会话归档** | `tblVpIiKTryvHeKM` | 归档 | 大 | 永久 |
| **L1_消息归档** | `tblNz0ljUFcr5ED4` | 归档 | 大 | 永久 |
| **L3_月度汇总** | `tblV47g7vuPaJwda` | 归档 | 小 | 永久 |
| **L3_季度汇总** | `tblY9LPu84HVW3Oj` | 归档 | 小 | 永久 |
| **L3_年度汇总** | `tblX1p8UtCH8kLVr` | 归档 | 小 | 永久 |

---

## 🔐 隐私保护

### Skill 使用统计

- **匿名 ID**: 基于机器特征的 SHA256 hash
- **不收集**: 任何对话内容、真实用户信息
- **仅收集**: 安装/使用事件、Skill 版本、OS 类型
- **一键关闭**: `export SKILL_TRACKING=off`

### Bot 质量数据

- **数据存储**: 您自己的飞书多维表格
- **访问权限**: 仅您本人可见
- **数据隔离**: 多租户架构（user_owner_id 隔离）
- **随时删除**: 删除表格即可

---

## 🚀 快速开始

### 安装

```bash
openclaw skill install bot-quality-monitor
```

或手动克隆：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Chenlei105/bot-quality-monitor.git
cd bot-quality-monitor
./hooks/install.sh
```

### 更新

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main
```

### 验证

```bash
# 检查版本
cat package.json | grep version

# 测试埋点
python3 scripts/track-usage.py run '{"scene": "test"}'

# 测试同步
python3 scripts/track-usage.py sync
```

---

## 📞 支持与反馈

- **GitHub Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **GitHub Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions
- **作者**: 陈磊 (ou_baa3525cf6cb5c0fc1ce4e26753d812d)
- **版本**: v4.0.0
- **更新日期**: 2026-03-25

---

## ✨ v4.0 新特性

### 🆕 三层 Dashboard 系统

- **P0 个人看板**: 最近 7 天，每日 22:00 推送
- **P1 全局看板**: 最近 30 天，每周日 20:00 推送
- **P2 归档看板**: 90 天 ~ 全年，每月/季度/年度推送

### 🆕 自动化数据采集

- **Session Hook**: Heartbeat 自动检测新会话
- **场景识别**: 8 种场景智能分类
- **信号检测**: 纠错/完成状态/满意度自动识别

### 🆕 数据归档机制

- **L2 会话归档**: 超过 180 天自动归档
- **L1 消息归档**: 超过 90 天自动归档
- **月度/季度/年度汇总**: 自动聚合生成

### 🆕 可视化增强

- **Plotly 交互式图表**: 仪表盘/雷达图/热力图
- **HTML Dashboard**: 独立 HTML 文件，可离线查看
- **Bootstrap 5 响应式布局**: 支持桌面和移动端

---

**让您的 Bot 更智能、更健康！** 🚀
