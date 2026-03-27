# 📘 Bot Quality Monitor 完整用户手册

**从安装到日常使用，一本书搞定！**

---

## 📋 目录

1. [快速开始](#1-快速开始)
2. [命令行安装](#2-命令行安装)
3. [创建数据表](#3-创建数据表)
4. [初始化配置](#4-初始化配置)
5. [Demo 体验](#5-demo-体验)
6. [日常使用](#6-日常使用)
7. [日报推送](#7-日报推送)
8. [卸载与重装](#8-卸载与重装)
9. [常见问题](#9-常见问题)

---

## 1. 快速开始

### 只需要 4 步

```bash
# 第 1 步：克隆
cd ~/.openclaw/workspace/skills
git clone https://github.com/Chenlei105/bot-quality-monitor.git

# 第 2 步：安装
cd bot-quality-monitor
./hooks/install.sh

# 第 3 步：创建数据表
# 对你的 Bot 说：帮我创建 Bot 质量监控数据表

# 第 4 步：体验
# 输入 /health 查看健康度
```

**全程 2 分钟搞定！**

---

## 2. 命令行安装

### 完整命令

```bash
# 进入 Skills 目录
cd ~/.openclaw/workspace/skills

# 克隆最新代码
git clone https://github.com/Chenlei105/bot-quality-monitor.git

# 进入目录
cd bot-quality-monitor

# 执行安装脚本（会自动安装依赖、子 Skill、显示功能介绍）
./hooks/install.sh
```

### 安装输出示例

```
[install] Bot Quality Monitor v5.0.0 安装中...
[install] 正在检查 Python 依赖...
[install] ✓ plotly 已安装
[install] ✓ jinja2 已安装
[install] ✓ reports 目录已存在
[install] ✓ 配置文件已存在
[install] 正在上报匿名安装统计...
[install] 统计已记录到本地日志
[install] 正在安装子 Skill...
[install]   ✓ bot-analytics-collector 已存在
[install]   ✓ bot-daily-report 已存在
[install]   ✓ bot-platform-insights 已存在

🎉 安装完成！
✅ 所有 Skill 安装成功：
   • bot-quality-monitor (主系统)
   • bot-analytics-collector (数据采集)
   • bot-daily-report (日报生成)
   • bot-platform-insights (平台洞察)

📊 安装这个 Skill 能干什么：
   ✅ 自动采集对话数据，统计 Bot 运行情况
   ✅ 每日生成健康度日报（综合评分 + 趋势图）
   ✅ 智能预警：高分低用、低分高风险、高风险场景
   ✅ 给出具体优化建议（Prompt/模型/Skill）
   ✅ 交互式 HTML Dashboard，一目了然
   ✅ 每周生成平台洞察周报，帮你持续优化 Bot

下一步：
   对你的 Bot 说：帮我创建 Bot 质量监控数据表
   Bot 会全自动创建多维表格和配置，10 秒搞定！
   然后静待每天 22:00 接收健康度日报
```

---

## 3. 创建数据表

### 用户对话

**你（用户）对 Bot 说：**

```
帮我创建 Bot 质量监控数据表
```

---

**Bot 回复：**

```
🚀 正在创建 Bot Quality Monitor 多维表格...
📊 将创建 12 张数据表...
✅ 创建成功！

🎉 Bot Quality Monitor 安装完成！

✅ 已完成
- L1 消息明细表
- L2 会话汇总表
- L3 每日指标汇总
- L3 Signal Alerts（信号预警）
- L3 Skill ROI（Skill 性价比）
- L3 Skill Run（Skill 运行记录）
- L0 Skill Usage（使用统计）
- L1/L2 归档表
- L3 月度/季度/年度汇总表

📋 配置已保存到 config.json
⏰ 定时任务已设置（通过 OpenClaw Heartbeat）
```

---

## 4. 初始化配置

### Bot 继续输出欢迎指南

```
🔑 授权检查（重要）

请确保你的飞书机器人已开通以下权限：

| 权限 | 是否已授权 |
|------|-----------|
| ✅ 云文档 - 查看和编辑 | 读写多维表格 |
| ✅ 消息 - 发送消息 | 推送日报到你私信 |
| ✅ 通讯录 - 读取用户信息 | 识别用户身份 |

如果授权失败/数据不采集：
/openclaw feishu reauthorize
重新授权后重启 OpenClaw 即可。

---

📊 数据采集说明

采集什么？
- 每条消息的统计信息：轮次数、纠错次数、Token 消耗、响应时间
- 意图分类标签：数据分析/文档处理/搜索查询/代码调试/闲聊
- 不会采集消息原文（默认不采集）

隐私保护
- ✅ 数据完全隔离，只存在你的飞书多维表格里
- ✅ 不会将你的对话内容分享给任何第三方
- ✅ 随时可以删除数据（删除多维表格即可）
- ✅ 可以关闭匿名统计（设置 export SKILL_TRACKING=off）

---

🔄 接下来做什么？

1️⃣ 正常使用 Bot
数据采集全自动，你不用做任何事。Heartbeat 每分钟自动采集新对话。

2️⃣ 试试这些命令

| 命令 | 效果 | 示例 |
|------|------|------|
| /health | 查看当前健康度评分 | /health |
| /dashboard | 获取 HTML Dashboard 链接 | /dashboard |
| /diagnose <场景> | 诊断特定场景问题 | /diagnose 文档处理 |
| /help | 查看帮助 | /help |

3️⃣ 等待日报
每天 22:00（GMT+8）会自动给你发私信推送健康度日报

---

💡 提示：现在输入 /health 试试吧！
```

---

## 5. Demo 体验

### 试试这些命令

#### 命令 1：/health 查看健康度

**你输入：**
```
/health
```

**Bot 回复：**
```
📊 综合健康度: -- 分
⏳ 暂无数据积累，请先正常使用 Bot 对话 24 小时

数据采集中...
- 已采集会话: 0
- 已采集消息: 0
- 采集状态: 运行中

💡 提示：持续使用 Bot 对话，数据会自动积累。
    第二天 22:00 会收到第一份完整日报。
```

> 📝 **说明**：刚开始没有数据是正常的，只要正常使用 Bot，Heartbeat 每分钟会自动采集对话数据。

---

#### 命令 2：/dashboard 获取 Dashboard

**你输入：**
```
/dashboard
```

**Bot 回复：**
```
📊 Dashboard 已生成！

📁 文件位置：
~/.openclaw/workspace/reports/p0-dashboard-YYYYMMDD.html

🔗 你可以用浏览器打开查看交互式图表：
- 综合健康度仪表盘
- 7 天趋势折线图
- 场景健康度热力图
- 三类信号卡片
- 失败案例 Top 10

⏳ 目前暂无数据，明天会有完整展示。
```

---

#### 命令 3：/diagnose 诊断场景

**你输入：**
```
/diagnose 文档处理
```

**Bot 回复：**
```
🔍 文档处理场景诊断

⏳ 暂无足够数据进行分析

当该场景有 5+ 条失败记录后，会自动生成诊断报告：
- 失败率统计
- 根因分析（Prompt 不明确 / 权限不足 / 模型不匹配等）
- 改进建议

💡 提示：继续使用 Bot 对话，数据会自动积累。
```

---

#### 命令 4：/help 查看帮助

**你输入：**
```
/help
```

**Bot 回复：**
```
📖 Bot Quality Monitor 帮助

━━━━━━━━━━ 命令列表 ━━━━━━━━━━

/health [scene]
   查看整体或特定场景的健康度
   示例: /health 或 /health 文档处理

/dashboard
   获取 HTML Dashboard 链接
   用浏览器打开可查看交互式图表

/diagnose <场景>
   诊断特定场景的问题
   示例: /diagnose 文档处理

/help
   显示帮助信息

━━━━━━━━━━ 日常使用 ━━━━━━━━━━

✅ 数据采集：全自动，Heartbeat 每分钟采集
✅ 健康日报：每天 22:00 自动推送
✅ 平台周报：每周日 20:00 自动推送

━━━━━━━━━━ 了解更多 ━━━━━━━━━━

安装文档: INSTALL.md
更新指南: UPDATE.md
重装手册: REINSTALL.md
GitHub: https://github.com/Chenlei105/bot-quality-monitor
```

---

## 6. 日常使用

### 正常使用即可

数据采集是**全自动**的，你不需要做任何操作：

1. **正常使用 Bot** - 像平常一样和 Bot 对话
2. **Heartbeat 每分钟** - 自动采集新对话的统计信息
3. **数据写入飞书** - 自动写入你创建的多维表格

### 查看数据

直接去飞书多维表格查看：
- **云空间 → 多维表格 → Bot Quality Monitor**
- 查看 L1 消息明细、L2 会话汇总等表

---

## 7. 日报推送

### 自动推送

每天 **22:00（GMT+8）**，Bot 会自动给你发私信：

```
📊 Bot 质量监控日报 - 2026-03-27

━━━━━━━━━━ 综合健康度 ━━━━━━━━━━
🏃 健康度: 82 分 (较昨日 +3)
├─ 质量维度: 85 分
├─ 效率维度: 80 分
└─ 资源维度: 78 分

━━━━━━━━━━ 关键指标 ━━━━━━━━━━
📈 会话数: 156 (+12%)
✅ 完成率: 89% (+5%)
🔄 纠错率: 4% (-2%)
⏱️  平均响应: 2.3s

━━━━━━━━━━ 三类信号 ━━━━━━━━━━

🟢 高分低用
Bot: 小爱同学 - 健康度 90 分，但本周只用了 2 次
💡 建议: 增加使用场景

🔴 低分高风险
Bot: 客服助手 - 纠错率 12%，失败次数 8 次
💡 建议: 检查 Prompt 清晰度，考虑切换模型

⚠️ 高风险场景
文档处理 - 失败率 18%，主要问题：Prompt 不明确
💡 建议: 优化 Prompt，或安装相关 Skill

━━━━━━━━━━ 改进建议 ━━━━━━━━━━

1. 📝 Prompt 优化
   场景: 文档处理
   问题: Prompt 太模糊，导致 Bot 理解偏差
   示例: "帮我处理" → "帮我把这份 PDF 转为 Markdown 格式"

2. 🤖 模型推荐
   场景: 代码调试
   当前成功率: 75%
   推荐: Claude Sonnet 4，成功率可达 88%

3. 🛠️ Skill 推荐
   场景: 文档处理
   推荐: docx-processor Skill，处理效率提升 40%

━━━━━━━━━━ Dashboard ━━━━━━━━━━
📁 ~/.openclaw/workspace/reports/p0-dashboard-20260327.html
用浏览器打开查看完整交互式图表

━━━━━━━━━━ 明天见 ━━━━━━━━━━
💡 持续使用 Bot，数据会自动积累，健康度会更准确！
```

---

## 8. 卸载与重装

### 卸载流程

#### 第一步：删除飞书多维表格（先做！）

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./hooks/delete-bitable.sh
```

或手动去飞书删除：飞书 → 云空间 → 多维表格 → 删除

#### 第二步：卸载 Skill

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./hooks/uninstall.sh

# 删除本地目录
cd ..
rm -rf bot-quality-monitor bot-analytics-collector bot-daily-report bot-platform-insights
```

---

### 重装流程

```bash
# 克隆
cd ~/.openclaw/workspace/skills
git clone https://github.com/Chenlei105/bot-quality-monitor.git
cd bot-quality-monitor

# 安装
./hooks/install.sh

# 创建数据表
# 对 Bot 说：帮我创建 Bot 质量监控数据表
```

---

## 9. 常见问题

### Q1: 安装后数据没有采集？

**检查**：
1. `/openclaw feishu reauthorize` - 重新授权
2. 重启 OpenClaw
3. 检查日志：`~/.openclaw/workspace/logs/bot-analytics-error.log`

### Q2: 没有收到日报？

**检查**：
1. `receiverOpenId` 在 `config.json` 中是否正确
2. 飞书机器人是否有发送私信权限

### Q3: Dashboard 显示暂无数据？

**原因**：数据采集需要时间积累
**解决**：等待 24 小时后会有首日数据

### Q4: 如何关闭匿名统计？

```bash
export SKILL_TRACKING=off
```

### Q5: 怎么更新到最新版本？

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main
./hooks/install.sh
```

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **GitHub Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions
- **提交问题**: https://github.com/Chenlei105/bot-quality-monitor/issues/new

---

**让您的 Bot 更智能、更健康！** 🚀

---

*版本: 5.0.0 | 更新时间: 2026-03-27 | 作者: 陈磊 / 小炸弹 💣*