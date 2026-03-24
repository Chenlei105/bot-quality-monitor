# Bot Quality Monitor 安装指南

**5 分钟快速上手，让你的 Bot 更智能！**

---

## 📋 前提条件

- ✅ 已安装 OpenClaw（[安装指南](https://docs.openclaw.ai)）
- ✅ 已配置飞书机器人（或其他支持的平台）
- ✅ 飞书账号（企业版或个人版均可）

---

## 🚀 快速安装

### 方式一：一键安装（推荐）

```bash
openclaw skill install bot-quality-monitor
```

安装完成后，所有子 Skill 会自动安装：
- `bot-analytics-collector` - 数据采集
- `bot-daily-report` - 日报生成
- `bot-platform-insights` - 平台洞察

### 方式二：从 GitHub 安装

```bash
# 克隆仓库
git clone https://github.com/Chenlei105/bot-quality-monitor.git

# 复制到 OpenClaw skills 目录
cp -r bot-quality-monitor ~/.openclaw/workspace/skills/
cp -r bot-quality-monitor/bot-analytics-collector ~/.openclaw/workspace/skills/
cp -r bot-quality-monitor/bot-daily-report ~/.openclaw/workspace/skills/
cp -r bot-quality-monitor/bot-platform-insights ~/.openclaw/workspace/skills/
```

---

## ⚙️ 首次配置

### Step 1: 创建数据中台

首次使用时，需要创建飞书多维表格来存储数据：

1. 打开飞书，创建一个新的多维表格
2. 记下表格的 App Token（从 URL 获取，格式如 `Xw4Tb5C8KagMiQswkdacNfVPn8e`）
3. 在表格中创建以下数据表：

| 表名 | 用途 |
|------|------|
| L1_消息明细表 | 存储每条消息 |
| L2_会话汇总表 | 存储会话汇总 |
| L3_每日指标汇总 | Bot 排行榜 |
| L3_Signal_Alerts | 智能信号 |
| L3_Skill_ROI | Skill 性价比 |
| L3_Skill_Run | 多 Skill 协作记录 |

> 💡 **提示**：可以让 Bot 帮你自动创建这些表，只需说"帮我创建 Bot 质量监控的数据表"

### Step 2: 配置连接信息

编辑配置文件 `~/.openclaw/workspace/skills/bot-quality-monitor/config.json`：

```json
{
  "bitableAppToken": "你的多维表格AppToken",
  "tables": {
    "L1": "L1表的TableID",
    "L2": "L2表的TableID",
    "L3_daily": "L3每日指标的TableID",
    "L3_signals": "L3信号的TableID",
    "L3_roi": "L3 ROI的TableID",
    "L3_run": "L3 Skill Run的TableID"
  },
  "reportTime": "22:00",
  "timezone": "GMT+8"
}
```

### Step 3: 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下定时任务
# 每日 21:00 生成信号和 ROI
0 21 * * * python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-signal-alerts.py
0 21 * * * python3 ~/.openclaw/workspace/skills/bot-platform-insights/scripts/calculate-skill-roi.py

# 每日 22:00 生成日报和 Dashboard
0 22 * * * python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-html-dashboard.py
```

---

## ✅ 验证安装

### 检查 Skill 是否安装成功

```bash
openclaw skill list | grep bot
```

应该看到：
```
bot-quality-monitor      v3.0.0  智能 Bot 健康监控系统
bot-analytics-collector  v3.0.0  Bot 对话数据采集器
bot-daily-report         v3.0.0  Bot 健康度日报生成器
bot-platform-insights    v3.0.0  Bot 平台级洞察引擎
```

### 测试数据采集

与你的 Bot 进行一次对话，然后检查多维表格的 L1 表是否有新数据。

### 手动触发日报

```bash
python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-signal-alerts.py
```

---

## 📊 日常使用

### 查看日报

每天 22:00 会自动收到飞书私信推送的日报，包含：
- 📊 综合健康度评分
- 📈 7 天趋势图
- 🔔 三类智能信号
- 💡 改进建议

### 查看 Dashboard

HTML Dashboard 保存在：
```
~/.openclaw/workspace/reports/bot-daily-{日期}.html
```

用浏览器打开即可查看交互式图表。

### 常用命令

| 命令 | 说明 |
|------|------|
| `/health` | 查看当前健康度 |
| `/dashboard` | 获取 Dashboard 链接 |
| `/diagnose 文档处理` | 诊断特定场景问题 |

---

## 🔧 进阶配置

### 自定义健康度权重

编辑 `config.json`：

```json
{
  "healthWeights": {
    "quality": 0.40,
    "efficiency": 0.30,
    "resource": 0.30
  }
}
```

### 自定义信号阈值

```json
{
  "signalThresholds": {
    "highScoreLowUse": {
      "minHealthScore": 85,
      "maxWeeklyCount": 5
    },
    "lowScoreHighRisk": {
      "minCorrectionRate": 0.10,
      "minFailureCount": 5
    }
  }
}
```

### 自定义业务价值权重

```json
{
  "businessValue": {
    "数据分析": 10,
    "文档处理": 8,
    "健康诊断": 5,
    "闲聊": 1
  }
}
```

---

## ❓ 常见问题

### Q: 数据没有自动采集？

A: 检查以下几点：
1. Bot 是否正常运行
2. 多维表格权限是否正确配置
3. 查看日志：`~/.openclaw/logs/`

### Q: 日报没有推送？

A: 检查以下几点：
1. crontab 是否配置正确
2. 飞书消息权限是否正常
3. 手动执行脚本看是否有报错

### Q: 如何删除所有数据？

A: 直接删除飞书多维表格中的数据表即可，Skill 不会存储任何本地数据。

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **文档**: https://github.com/Chenlei105/bot-quality-monitor

---

## 📜 版本信息

- **当前版本**: v3.0.0
- **发布日期**: 2026-03-24
- **作者**: 陈磊 / 小炸弹 💣

---

**让你的 Bot 更智能、更健康！** 🚀
