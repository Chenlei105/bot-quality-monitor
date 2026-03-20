# Bot Quality Monitor

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/chenlei/bot-quality-monitor/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.8+-orange.svg)](https://openclaw.ai)

OpenClaw Bot 质量监控 Skill 体系 - 自动化监控 Bot 使用质量，提供数据驱动的优化建议。

---

## 📊 核心功能

- **三维度健康度评分**：质量（40%）+ 效率（30%）+ 资源（30%）
- **三类智能信号提示**：高分低用 Bot / 低分高风险 Bot / 高风险任务预警
- **每日质量日报**：飞书私信推送，麦肯锡风格报告
- **HTML Dashboard**：Plotly 交互式可视化
- **Skill ROI 评分**：成本视角看性价比
- **平台洞察周报**：失败模式识别 + Skill 编排推荐

---

## 🚀 快速开始

### 方法 1：通过 skillhub 安装（推荐）

```bash
skillhub install bot-quality-monitor
```

### 方法 2：手动安装

```bash
# 下载最新 Release
wget https://github.com/chenlei/bot-quality-monitor/releases/download/v2.1.0/bot-quality-monitor-2.1.0.tar.gz

# 解压到 OpenClaw skills 目录
tar -xzf bot-quality-monitor-2.1.0.tar.gz -C ~/.openclaw/skills/

# 初始化配置
/init bot-quality-monitor
```

### 方法 3：从源码安装

```bash
git clone https://github.com/chenlei/bot-quality-monitor.git ~/.openclaw/skills/bot-quality-monitor
cd ~/.openclaw/skills/bot-quality-monitor
/init bot-quality-monitor
```

---

## 📋 前置条件

- **OpenClaw**: >= 2026.3.8
- **Python**: >= 3.8
- **飞书多维表格**: App Token（数据存储）

---

## ⚙️ 配置

### 1. 设置环境变量

```bash
export BITABLE_APP_TOKEN="你的飞书多维表格AppToken"
```

### 2. 创建数据表

```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/create-tables.py
```

这会创建 6 张表：
- L1_消息明细表
- L2_会话汇总表
- L3_每日指标汇总
- L3_Signal_Alerts
- L3_Skill_ROI
- L3_Skill_Run

### 3. 配置定时任务

```bash
crontab -e

# 每日 22:00 生成日报
0 22 * * * ~/.openclaw/skills/bot-quality-monitor/scripts/daily-report.sh
```

---

## 📊 数据架构

### 三层数据模型

```
L1 消息明细 (实时写入)
    ↓
L2 会话汇总 (按会话聚合)
    ↓
L3 每日指标 (每日凌晨 3:00 生成)
    ↓
日报 / 周报 (定时推送)
```

### 6 张数据表

| 表名 | 说明 | 字段数 |
|------|------|--------|
| L1_消息明细表 | 每条消息一行 | 15 |
| L2_会话汇总表 | 每个会话一行 | 21 |
| L3_每日指标汇总 | 每日汇总 | 19 |
| L3_Signal_Alerts | 三类信号记录 | 12 |
| L3_Skill_ROI | Skill 性价比评分 | 10 |
| L3_Skill_Run | Skill 执行拆分 | 7 |

---

## 📈 使用示例

### 1. 查看今日报告

```
你：生成今日 Bot 使用报告
```

Bot 会自动：
1. 读取 L2 会话汇总数据
2. 计算三维度健康度
3. 检测三类信号
4. 生成飞书卡片推送

### 2. 生成 HTML Dashboard

```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/generate-dashboard.py

# 打开生成的文件
open ~/.openclaw/workspace/reports/bot-daily-2026-03-20.html
```

### 3. 手动触发信号检测

```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/generate-signal-alerts.py
```

---

## 🎨 Dashboard 预览

HTML Dashboard 包含：
- 📊 综合健康度仪表盘（实时动画）
- 📈 7天趋势折线图（纠错率 + 首解率）
- 🔗 数据中台快速链接

![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+Preview)

---

## 📚 文档

- **安装指南**: [INSTALL.md](INSTALL.md)
- **发布指南**: [PUBLISH-GUIDE.md](PUBLISH-GUIDE.md)
- **Skill 文档**: [SKILL.md](SKILL.md)
- **PRD v1.5**: https://xcnlx9hjxf3f.feishu.cn/wiki/I5fVwdcRCioExIkDIXtcrqdtnUg

---

## 🐛 常见问题

### Q1：为什么 L3_每日指标汇总是空的？
A：需要等到每日凌晨 3:00 自动生成，或手动触发聚合任务。

### Q2：日报没有自动推送？
A：检查 crontab 配置：`crontab -l`

### Q3：HTML Dashboard 无法打开？
A：右键 → 打开方式 → 选择浏览器，或拖拽文件到浏览器窗口。

### Q4：数据不准确怎么办？
A：
1. 检查配置文件：`~/.openclaw/skills/bot-analytics-shared/config.yaml`
2. 确认 App Token 正确：`echo $BITABLE_APP_TOKEN`
3. 查看日志：`tail -f ~/.openclaw/workspace/logs/bot-daily-report.log`

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/your-feature`
3. 提交修改：`git commit -am 'Add your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

---

## 📝 版本历史

### v2.1.0（2026-03-20）

**新增功能**：
- ✨ 三类智能信号提示（高分低用/低分高风险/高风险任务）
- ✨ HTML Dashboard（Plotly 交互式可视化）
- ✨ Skill ROI 评分（成本视角看性价比）
- ✨ 多 Skill 协作分析
- ✨ 会话切割优化（时间窗口+任务边界）

**数据架构升级**：
- ✨ L2 新增 3 个字段（Skill数量/协作成本系数/关键路径）
- ✨ L3 新增 3 张表（Signal_Alerts/Skill_ROI/Skill_Run）

**开发效率**：
- 🚀 6.5 小时完成（预估 6 天，加速 7.4x）

### v2.0.0（2026-03-18）
- ✨ 生产化改造（App Token 配置化、隐私保护、写入队列）
- ✨ 实时触发 + 归档机制

### v1.0.0（2026-03-18）
- 🎉 初版发布

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👤 作者

**小炸弹** 💣  
OpenClaw Agent

---

## 🙏 致谢

- 感谢 **大少爷（陈磊）** 的全程支持和高效协作 💪
- 感谢 **OpenClaw 团队** 提供的强大工具链 🛠️
- 感谢所有测试用户的反馈 🎯

---

## 📮 联系方式

- **Issues**: https://github.com/chenlei/bot-quality-monitor/issues
- **飞书**: 联系大少爷（陈磊）

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
