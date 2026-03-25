# Bot Quality Monitor 安装指南

**5 分钟快速上手，让你的 Bot 更智能！**

---

## 📋 前提条件

- ✅ 已安装 OpenClaw（[安装指南](https://docs.openclaw.ai)）
- ✅ 已配置飞书机器人（或其他支持的平台）
- ✅ 飞书账号（企业版或个人版均可）
- ✅ 飞书机器人已授予多维表格权限

---

## 🚀 快速安装

### 方式一：一键安装（推荐，SkillHub）

```bash
openclaw skill install bot-quality-monitor
```

安装完成后，**所有子 Skill 会自动安装**：
- `bot-analytics-collector` - 数据采集
- `bot-daily-report` - 日报生成
- `bot-platform-insights` - 平台洞察

### 方式二：从 GitHub 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Chenlei105/bot-quality-monitor.git
cd bot-quality-monitor
./hooks/install.sh
```

---

## ✨ 全自动配置（只需一句话）

安装完成后，**对你的 Bot 说一句话**：

> **帮我创建 Bot 质量监控数据表**

Bot 会全自动完成以下操作：
1. 创建飞书多维表格应用
2. 自动创建 **12 张数据表**（含归档和统计）
3. 自动生成完整的 `config.json` 配置
4. 设置好定时任务（通过 OpenClaw Heartbeat）

**全程 10 秒，不需要你做任何其他操作！** 🎉

---

## ✅ 验证安装

安装完成后，你可以：

### 1. 检查 Skill 是否安装成功

```bash
openclaw skill list | grep bot
```

应该看到：
```
bot-quality-monitor      v4.0.0  智能 Bot 健康监控系统
bot-analytics-collector  v4.0.0  Bot 对话数据采集器
bot-daily-report         v4.0.0  Bot 健康度日报生成器
bot-platform-insights    v4.0.0  Bot 平台级洞察引擎
```

### 2. 等待数据采集

安装完成后，Heartbeat 会自动开始采集对话数据，**无需重启**。

与 Bot 正常对话即可，数据会自动写入你的多维表格。

### 3. 接收第一份日报

安装后第二天 **22:00**，你会自动收到飞书私信推送的健康度日报，包含：
- 📊 综合健康度评分（0-100）
- 📈 7 天趋势图
- 🔔 三类智能信号
- 💡 改进建议

---

## 📊 日常使用

### 常用命令

| 命令 | 说明 |
|------|------|
| `/health` | 查看当前健康度 |
| `/dashboard` | 获取 Dashboard 链接 |
| `/diagnose <场景>` | 诊断特定场景问题 |

### 查看 Dashboard

HTML Dashboard 保存在：
```
~/.openclaw/workspace/reports/p0-dashboard-YYYYMMDD.html
```

用浏览器打开即可查看交互式图表。

---

## 🔧 进阶配置（可选）

你可以编辑 `config.json` 自定义配置：

### 自定义健康度权重

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
    "搜索查询": 4,
    "代码调试": 6,
    "闲聊": 1,
    "其他": 3
  }
}
```

### 修改报告时间或时区

```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8"
}
```

---

## 🔐 权限检查清单

安装前，请确保你的飞书机器人已开通以下权限：

| 权限 | 说明 |
|------|------|
| 云文档 - 查看和编辑 | 读写多维表格 |
| 消息 - 发送消息 | 推送日报 |
| 日历 - 查看用户信息 | （不需要，可选） |

如果授权失败，请重新授权：
```
/openclaw feishu reauthorize
```

---

## ❓ 常见问题

### Q1: 安装后数据没有自动采集？

**A**: 检查以下几点：
1. Bot 是否正常运行（Heartbeat 每分钟触发）
2. 多维表格权限是否正确（机器人是否能编辑）
3. 查看日志：`~/.openclaw/workspace/logs/bot-analytics-error.log`
4. 检查 `config.json` 是否配置正确（App Token 和 Table ID）

### Q2: 没有收到日报？

**A**: 检查以下几点：
1. `receiverOpenId` 在 `config.json` 中是否正确
2. 飞书机器人是否有发送私信权限
3. 手动执行测试：
```bash
python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-signal-alerts.py
python3 ~/.openclaw/workspace/skills/bot-daily-report/scripts/generate-html-dashboard.py
```

### Q3: Dashboard 显示"暂无数据"？

**A**: 数据采集需要时间积累，等待 24 小时后会有首日数据。

### Q4: 如何关闭匿名使用统计？

**A**: 设置环境变量：
```bash
export SKILL_TRACKING=off
```

#### Q5: 如何卸载？

```bash
# 删除 Skill 目录
cd ~/.openclaw/workspace/skills
rm -rf bot-quality-monitor
rm -rf bot-analytics-collector
rm -rf bot-daily-report
rm -rf bot-platform-insights

# 删除本地日志
rm -f ~/.openclaw/workspace/logs/bot-analytics-error.log
rm -f ~/.openclaw/workspace/logs/collected-sessions.json
```

> 💡 飞书多维表格不会自动删除，如果你不需要了，可以手动删除。

### Q6: 如何删除所有数据？

**A**: 直接删除飞书多维表格中的数据表即可，Skill 不会存储任何原始数据在本地。

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **GitHub Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions
- **完整文档**: https://github.com/Chenlei105/bot-quality-monitor

---

## 📜 版本信息

- **当前版本**: v4.0.0
- **发布日期**: 2026-03-25
- **作者**: 陈磊 / 小炸弹 💣

---

**让你的 Bot 更智能、更健康！** 🚀
