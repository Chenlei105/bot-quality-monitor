# 快速开始指南

5 分钟上手 Bot Quality Monitor

---

## 1. 安装（30 秒）

```bash
openclaw skill install bot-quality-monitor
```

等待安装完成，看到 ✅ 表示成功。

---

## 2. 创建监控表格（60 秒）

对你的 Bot 说：

> 帮我创建 Bot 质量监控数据表

Bot 会自动：
- 在你的飞书空间创建多维表格
- 创建 12 张数据表
- 添加核心字段
- 写入 3 条测试数据
- 保存配置

完成后 Bot 会发送表格链接给你。

---

## 3. 查看数据（10 秒）

点击 Bot 发送的链接，打开你的监控表格。

你会看到：
- **L2_会话汇总表**：每个对话的统计数据
- **L3_每日指标汇总**：每天的健康度评分
- **L3_三类信号表**：智能预警信号

---

## 4. 等待日报（第二天）

明天 22:00，Bot 会自动推送首份健康度日报。

---

## 常用命令

```bash
# 修改推送时间
/settime 21:00

# 查看帮助
/help

# 查看健康度
/health

# 生成 Dashboard
/dashboard
```

---

## 下一步

- 📖 阅读 [完整文档](../README.md)
- 🛠️ 查看 [故障排查](./TROUBLESHOOTING.md)
- 🔒 了解 [隐私保护](./DATA-ISOLATION.md)

---

## 需要帮助？

- GitHub Issues: https://github.com/Chenlei105/bot-quality-monitor/issues
- 文档首页: [README.md](../README.md)
