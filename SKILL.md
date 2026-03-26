---
name: bot-quality-monitor
description: Bot 健康监控系统。当用户提到"质量监控"、"健康度"、"Bot 监控"、"创建监控数据表"、或使用命令 /health、/dashboard、/diagnose、/help 时触发此 Skill。
---

# Bot Quality Monitor

**智能 Bot 健康监控系统 v4.0.0**

---

## 触发条件

当用户意图匹配以下任一情况时，激活此 Skill：

### 1. 创建数据表
- 用户说："帮我创建 Bot 质量监控数据表"
- 用户说："创建质量监控表"
- 用户说："初始化质量监控"

### 2. 命令触发
- 用户输入：`/health` 或 `/health [场景名]`
- 用户输入：`/dashboard`
- 用户输入：`/diagnose [场景名]`
- 用户输入：`/help`

### 3. 查询意图
- 用户问："Bot 健康吗？"
- 用户问："质量监控怎么看？"
- 用户问："怎么看 Bot 的状态？"
- 用户问："怎么查看 Bot 健康度？"

---

## 命令响应

### 命令 1：创建数据表

**触发语句**："帮我创建 Bot 质量监控数据表"

**处理流程**：

1. 执行 `scripts/auto-create-bitable.py` 创建飞书多维表格
2. 生成 12 张数据表
3. 输出欢迎指南（读取 `references/post-create-welcome.md`）

**回复格式**：
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

---

🔑 授权检查（重要）

请确保你的飞书机器人已开通以下权限：

| 权限 | 说明 |
|------|------|
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

### 命令 2：/health 查看健康度

**触发语句**：`/health` 或 `/health [场景名]`

**处理流程**：

1. 读取 L3_每日指标汇总表获取最新健康度数据
2. 如果有参数（场景名），读取该场景的 L2 会话汇总
3. 生成健康度报告

**回复格式（有数据）**：
```
📊 综合健康度: 82 分 (较昨日 +3)
├─ 质量维度: 85 分 (+2)
├─ 效率维度: 80 分 (+5)
└─ 资源维度: 78 分 (+1)

━━━━━━━━━━ 关键指标 ━━━━━━━━━━
📈 会话数: 156 (+12%)
✅ 完成率: 89% (+5%)
🔄 纠错率: 4% (-2%)
⏱️  平均响应: 2.3s

━━━━━━━━━━ 三类信号 ━━━━━━━━━━
🟢 高分低用: 1 个 Bot
🔴 低分高风险: 1 个 Bot  
⚠️ 高风险场景: 1 个

💡 详细分析请查看 /dashboard
```

**回复格式（无数据）**：
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

---

### 命令 3：/dashboard 获取 Dashboard

**触发语句**：`/dashboard`

**处理流程**：

1. 调用 `p0-dashboard/generate-p0-dashboard.py` 生成 HTML
2. 返回文件路径和说明

**回复格式**：
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

### 命令 4：/diagnose 诊断场景

**触发语句**：`/diagnose [场景名]`

**处理流程**：

1. 从 L2 会话汇总表读取该场景的失败记录
2. 调用 `diagnostic-engine.py` 进行根因分析
3. 生成诊断报告

**回复格式（有数据）**：
```
🔍 文档处理场景诊断

━━━━━━━━━━ 失败统计 ━━━━━━━━━━
失败率: 15% (5/33)
平均纠错次数: 2.3 次/会话

━━━━━━━━━━ 根因分析 ━━━━━━━━━━
🔸 Prompt 不明确: 60%
🔸 权限不足: 20%
🔸 模型不匹配: 15%
🔸 其他: 5%

━━━━━━━━━━ 改进建议 ━━━━━━━━━━

1. 📝 Prompt 优化
   当前: "帮我处理文档"
   建议: "帮我把这份 PDF 转为 Markdown 格式，保留原文格式"

2. 🤖 模型推荐
   当前模型: MiniMax-M2.5
   推荐: Claude Sonnet 4，成功率可达 88%

3. 🛠️ Skill 推荐
   推荐安装: docx-processor，处理效率提升 40%
```

**回复格式（无数据）**：
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

### 命令 5：/help 查看帮助

**触发语句**：`/help` 或 "帮助" 或 "怎么用"

**回复格式**：
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

/settime <时间>
   设置日报推送时间
   示例: /settime 20:00 或 /settime 9:00

/settz <时区>
   设置时区
   示例: /settz GMT+8 或 /settz UTC

/help
   显示帮助信息

━━━━━━━━━━ 日常使用 ━━━━━━━━━━

✅ 数据采集：全自动，Heartbeat 每分钟采集
✅ 健康日报：每天 22:00 自动推送（可自定义时间）
✅ 平台周报：每周日 20:00 自动推送

━━━━━━━━━━ 了解更多 ━━━━━━━━━━

安装文档: INSTALL.md
更新指南: UPDATE.md
重装手册: REINSTALL.md
用户手册: USERS_GUIDE.md
GitHub: https://github.com/Chenlei105/bot-quality-monitor
```

---

### 命令 6：/settime 设置推送时间

**触发语句**：`/settime [时间]` 或 "设置推送时间"

**处理流程**：

1. 解析用户输入的时间（支持格式：HH:MM，如 20:00、9:00）
2. 更新 config.json 中的 reportTime 字段
3. 确认设置成功

**回复格式**：
```
✅ 推送时间已设置为: 20:00

📊 每天 20:00 会自动给你推送健康度日报
⏰ 时区: GMT+8

💡 如需修改，随时输入 /settime <新时间>
   例如: /settime 9:00
```

**回复格式（参数错误）**：
```
❌ 时间格式错误

请使用 HH:MM 格式，例如：
/settime 20:00  （晚上 8 点）
/settime 9:00   （早上 9 点）
/settime 22:30  （晚上 10 点半）
```

---

### 命令 7：/settz 设置时区

**触发语句**：`/settz [时区]` 或 "设置时区"

**处理流程**：

1. 解析用户输入的时区（支持：GMT+8、UTC、PST、CST 等）
2. 更新 config.json 中的 timezone 字段
3. 确认设置成功

**回复格式**：
```
✅ 时区已设置为: GMT+8

📊 每天 22:00（北京时间）会自动给你推送健康度日报
```

**支持的时区**：
- GMT+8 / CST / 北京时间
- UTC / GMT
- PST / GMT-8（洛杉矶）
- EST / GMT-5（纽约）
- JST / GMT+9（东京）

---

## 自动任务

### 每日 22:00 日报推送

1. 调用 `scripts/generate-signal-alerts.py` 生成信号
2. 调用 `scripts/generate-html-dashboard.py` 生成 Dashboard
3. 调用 `send-personalized-report.py` 推送日报

**日报内容**：详见 USERS_GUIDE.md 第 7 章

### 每周日 20:00 周报推送

1. 调用 `scripts/calculate-skill-roi.py` 计算 ROI
2. 调用 `scripts/generate-skill-recommendations.py` 生成推荐
3. 生成平台洞察周报卡片推送给用户

---

## 数据隐私

- ✅ **完全隔离**: 您只能看到自己的 Bot 数据
- ✅ **本地存储**: 数据存在您的飞书多维表格
- ✅ **随时删除**: 卸载后可手动删除数据
- ✅ **不会泄露**: 不会将您的对话内容分享给他人

---

## 相关文件

- `scripts/auto-create-bitable.py` - 创建多维表格
- `bot-daily-report/send-personalized-report.py` - 发送日报
- `references/post-create-welcome.md` - 欢迎指南
- `USERS_GUIDE.md` - 完整用户手册

---

## 版本

v4.0.0 (2026-03-26)

---

**让您的 Bot 更智能、更健康！** 🚀