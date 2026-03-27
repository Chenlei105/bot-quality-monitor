---
name: bot-quality-monitor
description: Bot 健康监控系统。当用户提到"质量监控"、"健康度"、"Bot 监控"、创建数据表、或使用命令 /health、/dashboard、/diagnose、/settime、/settz、/createdemo、/help 时触发此 Skill。
---

# Bot Quality Monitor

**智能 Bot 健康监控系统 v5.0**

---

## 触发条件

当用户意图匹配以下任一情况时,激活此 Skill:

### 1. 安装与创建数据表

**安装 Skill（从 GitHub）**:
- 用户说: "帮我从 GitHub 安装 https://github.com/Chenlei105/bot-quality-monitor"
- 用户说: "安装 Chenlei105/bot-quality-monitor"
- ⚠️ 必须指定 GitHub，否则会去 SkillHub/ClawHub

**创建数据表**:
- 用户说: "帮我创建 Bot 质量监控数据表"
- 用户说: "创建质量监控表"
- 用户说: "初始化质量监控"

### 2. 命令触发
- 用户输入: `/health` 或 `/health [场景名]`
- 用户输入: `/dashboard`
- 用户输入: `/diagnose [场景名]`
- 用户输入: `/settime [时间]`
- 用户输入: `/settz [时区]`
- 用户输入: `/createdemo`
- 用户输入: `/help`

### 3. 查询意图
- 用户问: "Bot 健康吗?"
- 用户问: "质量监控怎么看?"
- 用户问: "怎么看 Bot 的状态?"

---

## 命令响应

### 命令 0: 安装 Skill（首次使用，从 GitHub）

**触发语句**: 
- "帮我从 GitHub 安装 https://github.com/Chenlei105/bot-quality-monitor"
- "安装 Chenlei105/bot-quality-monitor"

⚠️ **重要提示**:
- 必须明确指定 **GitHub** 或 **完整 GitHub 链接**
- ❌ 错误示例: "帮我安装 bot-quality-monitor"（会去 SkillHub/ClawHub）
- ✅ 正确示例: "从 GitHub 安装 bot-quality-monitor"

**执行流程**:
1. Bot 自动从 GitHub 克隆仓库
2. 安装到 `~/.openclaw/workspace/skills/bot-quality-monitor/`
3. 回复安装成功

**回复格式**:
```
✅ Skill 已从 GitHub 安装: bot-quality-monitor v5.0

📦 安装位置: ~/.openclaw/workspace/skills/bot-quality-monitor/
🔗 GitHub: https://github.com/Chenlei105/bot-quality-monitor

🎯 下一步: 发送 "帮我创建 Bot 质量监控数据表" 创建监控表格
```

---

### 命令 1: 创建数据表

**触发语句**: "帮我创建 Bot 质量监控数据表"

**重要说明**:
- 表格由**用户自己的 Bot**创建(不是小炸弹或其他 Bot)
- 表格创建在**用户自己的飞书空间**
- 用户完全拥有和控制这个表格
- 数据隔离: 每个用户的表格相互独立

**前置条件**: 已安装 Skill（参考命令 0）

**执行流程**:

1. 调用自动安装脚本 v5:
```bash
python3 ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/auto-setup-v5.py <user_open_id>
```

2. 脚本会输出 JSON 工作流,Bot 按步骤执行:
   - 步骤 1: 创建飞书多维表格应用
   - 步骤 2: 批量创建 12 张数据表（包含 L3_年度汇总表）
   - 步骤 3-6: 批量添加字段（100+ 个）
     - L2_会话汇总表: 35 个字段
     - L3_每日指标汇总: 25 个字段
     - L3_三类信号表: 8 个字段
     - L0_Skill_Usage: 7 个字段
   - 步骤 7: 写入完整测试数据（70 条记录，7 天 × 10 条/天）
   - 步骤 8: 保存配置到 config.json

3. Bot 逐步执行每个工具调用

4. 最后回复用户成功消息(脚本中的 success_message)

**回复格式**:
```
✅ **Bot 质量监控表格创建成功！**

📊 **表格信息**:
- 在你的飞书空间创建
- 链接: https://www.feishu.cn/base/<app_token>
- 你拥有完全控制权
- 包含 12 张数据表（含 L3_年度汇总表）

📈 **完整字段**: 100+ 个字段已添加
📊 **测试数据**: 已写入 70 条演示记录（7 天数据）

⚙️ **配置已保存**:
- 数据采集已自动开始
- 明天 22:00 将推送首份日报

🎯 **下一步**:
- 点击链接查看你的表格
- 修改推送时间: /settime 21:00

**重要**: 请把表格链接保存好,这是你的监控数据中心!
```

---

### 命令 2: /health 查看健康度

**触发语句**: `/health` 或 `/health [场景名]`

**执行流程**:

1. 调用 `scripts/command-handler.py health`
2. 返回读取 L3 数据的指令
3. Bot 调用 `feishu_bitable_app_table_record` 读取数据
4. 格式化返回结果

**回复格式(有数据)**:
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

**回复格式(无数据)**:
```
📊 综合健康度: -- 分
⏳ 暂无数据积累,请先正常使用 Bot 对话 24 小时

数据采集中...
- 已采集会话: 0
- 已采集消息: 0
- 采集状态: 运行中

💡 提示: 持续使用 Bot 对话,数据会自动积累。
    第二天 22:00 会收到第一份完整日报。
```

---

### 命令 3: /dashboard 获取 Dashboard

**触发语句**: `/dashboard`

**执行流程**:

1. 调用 `scripts/workflow.py generate_dashboard`
2. Bot 调用 `bot-daily-report/scripts/generate-html-dashboard.py`
3. 返回文件路径

**回复格式**:
```
📊 Dashboard 已生成!

📁 文件位置:
~/.openclaw/workspace/reports/p0-dashboard-YYYYMMDD.html

🔗 你可以用浏览器打开查看交互式图表:
- 综合健康度仪表盘
- 7 天趋势折线图
- 场景健康度热力图
- 三类信号卡片
- 失败案例 Top 10
```

---

### 命令 4: /diagnose 诊断场景

**触发语句**: `/diagnose [场景名]`

**回复格式**:
```
🔍 [场景名] 场景诊断

⏳ 暂无足够数据进行分析

当该场景有 5+ 条失败记录后,会自动生成诊断报告

💡 继续使用 Bot 对话,数据会自动积累
```

---

### 命令 5: /settime 设置推送时间

**触发语句**: `/settime [时间]` 或 "设置推送时间"

**执行流程**:

1. 调用 `scripts/command-handler.py set_time <时间>`
2. 脚本验证时间格式并保存到 config.json

**回复格式**:
```
✅ 推送时间已设置为: 20:00

📊 每天 20:00 会自动给你推送健康度日报
⏰ 时区: GMT+8
```

**回复格式(错误)**:
```
❌ 时间格式错误

请使用 HH:MM 格式,例如:
/settime 20:00  (晚上 8 点)
/settime 9:00   (早上 9 点)
```

---

### 命令 6: /settz 设置时区

**触发语句**: `/settz [时区]`

**支持时区**: GMT+8、UTC、PST、EST、JST

**回复格式**:
```
✅ 时区已设置为: GMT+8
```

---

### 命令 7: /createdemo 重新生成 Demo

**触发语句**: `/createdemo` 或 "生成 Demo"

**执行流程**:

1. 调用 `scripts/generate-demo-data.py`
2. 重新生成测试数据
3. 推送 Demo 日报

---

### 命令 8: /help 查看帮助

**回复格式**:
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

配置文件位置: `~/.openclaw/workspace/skills/bot-quality-monitor/config.json`

```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "<app_token>",
  "receiverOpenId": "<user_open_id>",
  "tables": {
    "L1": "<table_id>",
    "L2": "<table_id>",
    "L3_daily": "<table_id>",
    ...
  }
}
```

---

## 自动任务

- **数据采集**: Heartbeat 每分钟自动采集
- **日报推送**: 每天 22:00(或用户设置的时间)
- **周报推送**: 每周日 20:00

---

## 版本

v5.0.0 (2026-03-27)

**重大更新**:
- ✅ 完整字段设计（100+ 个字段）
- ✅ 用户日报（飞书卡片 + Dashboard + 详细文档）
- ✅ 平台日报（给大少爷，Bot 排行榜 + Skill ROI）
- ✅ Heartbeat 自动执行引擎
- ✅ 数据隔离（用户私有 vs 中央平台）

---

**让您的 Bot 更智能、更健康!** 🚀
