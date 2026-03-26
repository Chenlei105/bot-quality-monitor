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

**🚨 重要警告**：
- **禁止只说不做**！不要只回复"正在创建..."而不实际调用工具
- **必须实际执行**！每一步都必须真正调用 feishu_bitable_app 等工具
- **禁止编造结果**！不要假装创建成功，必须等工具返回真实结果
- **必须保存配置**！最后必须调用 write 工具保存 config.json

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

**重要说明**：
- 表格由**用户自己的 Bot**创建（不是小炸弹或其他 Bot）
- 表格创建在**用户自己的飞书空间**
- 用户完全拥有和控制这个表格
- 数据隔离：每个用户的表格相互独立

**🚨 严格执行规则（违反将导致功能失效）**：

1. **必须真正调用工具**：不要只说"正在创建"，必须实际调用 `feishu_bitable_app` 等工具
2. **必须等待工具返回**：每一步都要等工具返回结果，再进行下一步
3. **必须保存返回值**：第 1 步的 app_token 必须用于后续所有步骤
4. **必须写入配置**：第 5 步必须调用 `write` 工具保存 config.json
5. **禁止编造数据**：不要假装创建成功，必须等真实的 API 响应

**验证方法**：
- 第 1 步后，必须有真实的 app_token（类似：KMu7befnRaptOnser6ecwlpfnMf）
- 第 2 步后，必须有 11 个真实的 table_id（类似：tblXXXXXXXX）
- 第 5 步后，config.json 必须有完整内容（不能是空字符串）

---

**⚠️ 按顺序执行以下所有步骤，缺一不可！**

### 第 1 步：创建飞书多维表格

调用工具：
```
feishu_bitable_app(
  action="create",
  name="OpenClaw Bot 质量监控"
)
```

保存返回的 `app_token`（后续步骤需要）。

---

### 第 2 步：批量创建 11 张数据表

调用工具：
```
feishu_bitable_app_table(
  action="batch_create",
  app_token=<第1步返回的app_token>,
  tables=[
    {"name": "L1_消息明细表"},
    {"name": "L2_会话汇总表"},
    {"name": "L3_每日指标汇总"},
    {"name": "L3_三类信号表"},
    {"name": "L0_Skill_Usage"},
    {"name": "L3_Skill_ROI"},
    {"name": "L3_Skill_Run"},
    {"name": "L2_会话归档表"},
    {"name": "L1_消息归档表"},
    {"name": "L3_月度汇总表"},
    {"name": "L3_季度汇总表"}
  ]
)
```

保存返回的表格 ID 映射（table_id 列表）。

---

### 第 3 步：为 L2_会话汇总表 添加字段

找到 L2_会话汇总表的 table_id（从第 2 步返回结果中查找）。

依次调用：
```
feishu_bitable_app_table_field(
  action="create",
  app_token=<第1步的app_token>,
  table_id=<L2_会话汇总表的table_id>,
  field_name="session_key",
  type=1
)

feishu_bitable_app_table_field(
  action="create",
  app_token=<第1步的app_token>,
  table_id=<L2_会话汇总表的table_id>,
  field_name="round_count",
  type=2
)

feishu_bitable_app_table_field(
  action="create",
  app_token=<第1步的app_token>,
  table_id=<L2_会话汇总表的table_id>,
  field_name="total_tokens",
  type=2
)
```

---

### 第 4 步：写入 3 条测试数据

调用工具：
```
feishu_bitable_app_table_record(
  action="batch_create",
  app_token=<第1步的app_token>,
  table_id=<L2_会话汇总表的table_id>,
  records=[
    {"fields": {"session_key": "demo_session_1", "round_count": 5, "total_tokens": 2500}},
    {"fields": {"session_key": "demo_session_2", "round_count": 3, "total_tokens": 1200}},
    {"fields": {"session_key": "demo_session_3", "round_count": 8, "total_tokens": 4800}}
  ]
)
```

---

### 第 5 步：保存配置到 config.json

调用工具：
```
write(
  path="~/.openclaw/workspace/skills/bot-quality-monitor/config.json",
  content=<以下JSON内容>
)
```

JSON 内容（**必须填入实际值**）：
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "<第1步返回的app_token>",
  "receiverOpenId": "<从消息上下文获取的user_open_id>",
  "tables": {
    "L1": "<L1_消息明细表的table_id>",
    "L2": "<L2_会话汇总表的table_id>",
    "L3_daily": "<L3_每日指标汇总的table_id>",
    "L3_signals": "<L3_三类信号表的table_id>",
    "L0_usage": "<L0_Skill_Usage的table_id>",
    "L3_roi": "<L3_Skill_ROI的table_id>",
    "L3_run": "<L3_Skill_Run的table_id>",
    "L2_archive": "<L2_会话归档表的table_id>",
    "L1_archive": "<L1_消息归档表的table_id>",
    "L3_monthly": "<L3_月度汇总表的table_id>",
    "L3_quarterly": "<L3_季度汇总表的table_id>"
  }
}
```

---

### 第 6 步：回复用户成功消息

回复用户：
```
✅ **Bot 质量监控表格创建成功！**

📊 **表格信息**：
- 在你的飞书空间创建
- 链接：https://www.feishu.cn/base/<第1步的app_token>
- 你拥有完全控制权
- 包含 12 张数据表（11 张 + 默认表）

📈 **测试数据**：已写入 3 条演示记录

⚙️ **配置已保存**：
- 数据采集已自动开始
- 明天 22:00 将推送首份日报

🎯 **下一步**：
- 点击链接查看你的表格
- 修改推送时间：/settime 21:00

**重要**：请把表格链接保存好，这是你的监控数据中心！
```
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

### L1_消息明细表

存储每条消息的详细信息

| 字段名 | 类型 | 说明 |
|--------|------|------|
| session_key | 文本 | 会话 ID |
| message_id | 文本 | 消息 ID |
| sender_id | 文本 | 发送者 ID |
| scene | 单选 | 场景分类 |
| is_correction | 复选框 | 是否包含纠错信号 |
| create_time | 日期 | 创建时间 |

### L2_会话汇总表

存储每个会话的汇总数据，支持四维指标体系

| 字段名 | 类型 | 说明 |
|--------|------|------|
| session_key | 文本 | 会话 ID |
| scene | 单选 | 场景分类 |
| turns | 数字 | 对话轮数 |
| corrections | 数字 | 纠错次数 |
| completed | 复选框 | 是否完成 |
| duration_minutes | 数字 | 会话时长（分钟） |
| task_resolution | 单选 | 任务解决状态（已解决/未解决/进行中） |
| satisfaction_score | 数字 | 满意度评分（0-100） |
| token_total | 数字 | 单次任务总 Token |
| is_unexpected_interrupt | 复选框 | 非预期中断标记 |
| complexity | 单选 | 任务复杂度（简单/中等/复杂） |
| response_time_ms | 数字 | 响应时长（毫秒） |

### L3_每日指标汇总

存储每日的聚合指标，支持四维健康分计算

| 字段名 | 类型 | 说明 |
|--------|------|------|
| date | 文本 | 日期 |
| total_sessions | 数字 | 会话数 |
| total_messages | 数字 | 消息数 |
| completion_rate | 数字 | 完成率 |
| correction_rate | 数字 | 纠错率 |
| health_score | 数字 | 综合健康分 |
| health_grade | 文本 | 健康等级 |
| task_resolution_rate | 数字 | 任务解决率 |
| avg_satisfaction | 数字 | 平均满意度 |
| avg_task_duration | 数字 | 平均任务时长 |
| avg_token_per_task | 数字 | 平均 Token 消耗 |
| interrupt_rate | 数字 | 非预期中断率 |
| p99_response_time | 数字 | P99 响应时长 |
| quality_score | 数字 | 质量维度得分 |
| efficiency_score | 数字 | 效率维度得分 |
| resource_score | 数字 | 资源维度得分 |

### 其他数据表

| 表名 | 说明 |
|------|------|
| L3_Signal_Alerts | 三类智能信号 |
| L3_Skill_ROI | Skill 性价比 |
| L3_Skill_Run | 多 Skill 协作记录 |
| L0_Skill_Usage | 使用统计 |
| L2_会话归档 | 会话归档 |
| L1_消息归档 | 消息归档 |
| L3_月度汇总 | 月度聚合 |
| L3_季度汇总 | 季度聚合 |
| L3_年度汇总 | 年度聚合 |

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