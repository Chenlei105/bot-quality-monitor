---
name: bot-quality-monitor
description: Bot 健康监控系统。当用户提到"质量监控"、"健康度"、"Bot 监控"、创建数据表、或使用命令 /health、/dashboard、/diagnose、/settime、/settz、/createdemo、/help 时触发此 Skill。
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
- 用户输入：`/settime [时间]`
- 用户输入：`/settz [时区]`
- 用户输入：`/createdemo`
- 用户输入：`/help`

### 3. 查询意图
- 用户问："Bot 健康吗？"
- 用户问："质量监控怎么看？"
- 用户问："怎么看 Bot 的状态？"

---

## 工作原理

此 Skill 通过以下方式执行：

1. **Bot 解析用户输入** - 识别命令和意图
2. **调用处理脚本** - 执行 `scripts/command-handler.py` 或 `scripts/workflow.py`
3. **调用飞书工具** - 使用 `feishu_bitable_app`、`feishu_bitable_app_table_record` 等工具
4. **返回结果给用户** - 格式化输出

---

## 命令响应

### 命令 1：创建数据表

**触发语句**："帮我创建 Bot 质量监控数据表"

**执行流程**：

1. 调用 `scripts/workflow.py create_bitable_full <user_open_id>`
2. 脚本返回操作步骤：
   - 创建多维表格应用
   - 创建 12 张数据表
   - 写入测试数据（7 天模拟数据）
   - 生成 Demo 日报
3. Bot 按步骤调用飞书 API
4. 最后主动询问用户设置推送时间

**回复格式**：
```
🚀 正在创建 Bot Quality Monitor 多维表格...
📊 将创建 12 张数据表...

✅ 创建成功！

📈 正在生成测试数据（模拟过去 7 天）...
   - 已生成: 156 个会话
   - 已生成: 892 条消息
   - 已生成: 每日指标汇总

📊 正在生成 Demo 日报...
✅ Demo 日报已生成并推送给你！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Bot 质量监控日报 - DEMO 示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏃 综合健康度: 82 分
├─ 质量维度: 85 分
├─ 效率维度: 80 分
└─ 资源维度: 78 分

📈 会话数: 156 (+12%)
✅ 完成率: 89% (+5%)
🔄 纠错率: 4% (-2%)

━━━━━━━━━━ 三类信号 ━━━━━━━━━━
🟢 高分低用: 1 个 Bot
🔴 低分高风险: 1 个 Bot
⚠️ 高风险场景: 1 个

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 这是 Demo 示例，展示正式日报的样式

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 设置推送时间

你希望每天什么时候收到日报？

💡 回复格式：
   /settime 20:00  （晚上 8 点）
   /settime 9:00   （早上 9 点）
```

---

### 命令 2：/health 查看健康度

**触发语句**：`/health` 或 `/health [场景名]`

**执行流程**：

1. 调用 `scripts/command-handler.py health`
2. 返回读取 L3 数据的指令
3. Bot 调用 `feishu_bitable_app_table_record` 读取数据
4. 格式化返回结果

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

**执行流程**：

1. 调用 `scripts/workflow.py generate_dashboard`
2. Bot 调用 `bot-daily-report/scripts/generate-html-dashboard.py`
3. 返回文件路径

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
```

---

### 命令 4：/diagnose 诊断场景

**触发语句**：`/diagnose [场景名]`

**回复格式**：
```
🔍 [场景名] 场景诊断

⏳ 暂无足够数据进行分析

当该场景有 5+ 条失败记录后，会自动生成诊断报告

💡 继续使用 Bot 对话，数据会自动积累
```

---

### 命令 5：/settime 设置推送时间

**触发语句**：`/settime [时间]` 或 "设置推送时间"

**执行流程**：

1. 调用 `scripts/command-handler.py set_time <时间>`
2. 脚本验证时间格式并保存到 config.json

**回复格式**：
```
✅ 推送时间已设置为: 20:00

📊 每天 20:00 会自动给你推送健康度日报
⏰ 时区: GMT+8
```

**回复格式（错误）**：
```
❌ 时间格式错误

请使用 HH:MM 格式，例如：
/settime 20:00  （晚上 8 点）
/settime 9:00   （早上 9 点）
```

---

### 命令 6：/settz 设置时区

**触发语句**：`/settz [时区]`

**支持时区**：GMT+8、UTC、PST、EST、JST

**回复格式**：
```
✅ 时区已设置为: GMT+8
```

---

### 命令 7：/createdemo 重新生成 Demo

**触发语句**：`/createdemo` 或 "生成 Demo"

**执行流程**：

1. 调用 `scripts/generate-demo-data.py`
2. 重新生成测试数据
3. 推送 Demo 日报

---

### 命令 8：/help 查看帮助

**回复格式**：
```
📖 Bot Quality Monitor 帮助

━━━━━━━━━━ 命令列表 ━━━━━━━━━━
/health [scene]   - 查看健康度
/dashboard         - 获取 Dashboard
/diagnose <场景>    - 诊断场景
/settime <时间>    - 设置推送时间
/settz <时区>      - 设置时区
/createdemo        - 重新生成 Demo
/help              - 显示帮助

━━━━━━━━━━ 了解更多 ━━━━━━━━━━
GitHub: https://github.com/Chenlei105/bot-quality-monitor
```

---

## 配置文件

配置文件位置：`~/.openclaw/workspace/skills/bot-quality-monitor/config.json`

```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8"
}
```

---

## 数据表结构

| 表名 | 说明 |
|------|------|
| L1_消息明细 | 每条消息一行 |
| L2_会话汇总 | 每个会话一行 |
| L3_每日指标汇总 | 每日聚合数据 |
| L3_Signal_Alerts | 三类智能信号 |
| L3_Skill_ROI | Skill 性价比 |
| L3_Skill_Run | 多 Skill 协作记录 |
| L0_Skill_Usage | 使用统计 |

---

## 自动任务

- **数据采集**：Heartbeat 每分钟自动采集
- **日报推送**：每天 22:00（或用户设置的时间）
- **周报推送**：每周日 20:00

---

## 关联文件

- `scripts/command-handler.py` - 命令处理器
- `scripts/workflow.py` - 完整工作流
- `scripts/generate-demo-data.py` - 生成测试数据
- `scripts/read-health.py` - 读取健康度数据

---

## 版本

v4.0.0 (2026-03-26)

---

**让您的 Bot 更智能、更健康！** 🚀