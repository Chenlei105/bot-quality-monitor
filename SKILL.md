# Bot Quality Monitor

**版本**: 2.1.0  
**作者**: 小炸弹 💣  
**发布日期**: 2026-03-20

---

## 📝 简介

OpenClaw Bot 质量监控 Skill 体系，自动化监控 Bot 使用质量，提供数据驱动的优化建议。

**核心功能**：
- 📊 三维度健康度评分（质量/效率/资源）
- 💡 三类智能信号提示（高分低用/低分高风险/高风险任务）
- 📈 每日质量日报 + 每周平台洞察
- 🎨 HTML Dashboard（Plotly 交互式可视化）
- 🔍 Skill ROI 评分 + 编排推荐

---

## 🚀 快速开始

### 1. 安装
```bash
skillhub install bot-quality-monitor
```

### 2. 初始化配置
```bash
/init bot-analytics-collector
```

**系统会提示你输入**：
1. **飞书多维表格 App Token**：你的数据中台 Token
2. **时区**：GMT+8（中国标准时间）
3. **是否存储消息内容**：建议选 No（隐私保护）

### 3. 配置环境变量
```bash
export BITABLE_APP_TOKEN="你的飞书多维表格AppToken"
```

### 4. 创建数据表
运行建表脚本：
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

### 5. 配置定时任务
```bash
crontab -e

# 添加以下行：
# 每日 22:00 生成日报
0 22 * * * ~/.openclaw/skills/bot-quality-monitor/scripts/daily-report.sh

# 每周日 20:00 生成周报
0 20 * * 0 ~/.openclaw/skills/bot-quality-monitor/scripts/weekly-insights.sh
```

---

## 📊 核心功能

### 1. 三维度健康度评分
- **质量（40%）**：纠错率≤5%、首解率≥80%、好评率≥90%
- **效率（30%）**：任务完成率≥80%、响应速度≤3秒
- **资源（30%）**：API成功率≥99%、错误频率≤5次/天

**综合健康度** = 质量×0.40 + 效率×0.30 + 资源×0.30

### 2. 三类智能信号提示
- 🟢 **高分低用 Bot**：健康度高但使用频次低 → 建议多用
- 🔴 **低分高风险 Bot**：纠错率高或失败频繁 → 处方优化
- ⚠️ **高风险任务预警**：某类任务失败率高 → 建议避开

### 3. 每日质量日报
**生成时间**：每日 22:00 GMT+8  
**推送方式**：飞书私信

**日报内容**：
- 昨日概览（总对话/完成任务/纠错次数）
- 综合健康度得分 + 环比对比
- 问题诊断 + 改进处方
- 今日亮点
- 7天成长趋势
- 智能行动建议（三类信号）

### 4. HTML Dashboard
**生成命令**：
```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/generate-dashboard.py
```

**输出文件**：
```
~/.openclaw/workspace/reports/bot-daily-YYYY-MM-DD.html
```

**包含内容**：
- 📊 综合健康度仪表盘（实时动画）
- 📈 7天趋势折线图（纠错率 + 首解率）
- 🔗 数据中台快速链接

### 5. 每周平台洞察
**生成时间**：每周日 20:00 GMT+8  
**推送方式**：飞书私信

**周报内容**：
- 平台健康看板（Bot 排行榜 Top 5）
- 失败模式识别（高发场景 + 改进处方）
- Skill 自我迭代建议
- Skill 编排推荐（最优组合 + 不推荐组合）

---

## 🗂️ 数据架构

### 6 张表结构

| 表名 | 说明 | 字段数 |
|------|------|--------|
| L1_消息明细表 | 每条消息一行 | 15 |
| L2_会话汇总表 | 每个会话一行 | 21 |
| L3_每日指标汇总 | 每日汇总 | 19 |
| L3_Signal_Alerts | 三类信号记录 | 12 |
| L3_Skill_ROI | Skill 性价比评分 | 10 |
| L3_Skill_Run | Skill 执行拆分 | 7 |

**数据流转**：
```
用户对话 → L1 实时写入 → L2 会话汇总 → L3 每日聚合 → 日报/周报
```

---

## 🔧 配置说明

### 配置文件位置
```
~/.openclaw/skills/bot-analytics-shared/config.yaml
```

### 必填配置项
```yaml
# 数据中台配置
app_token: Xw4Tb5C8KagMiQswkdacNfVPn8e  # 实际部署时从环境变量读取

# 数据表 Table ID
table_l1: tblmKO3HejbWpUWe           # L1_消息明细表
table_l2: tblT0I1nCFhbpvGa           # L2_会话汇总表
table_l3_daily: tbldgJxU6QUSjnf6     # L3_每日指标汇总
table_l3_signal_alerts: tblVDILmtu1oYRTE  # L3_Signal_Alerts
table_l3_skill_roi: tblvmjcMrdtSFF8D      # L3_Skill_ROI
table_l3_skill_run: tblGOfgzbcle1C4N      # L3_Skill_Run

# 时区配置
timezone: GMT+8

# 隐私配置
store_message_content: false  # 默认不存消息内容

# HTML Dashboard
enable_html_dashboard: false
dashboard_output_dir: ~/.openclaw/workspace/reports
```

---

## 📚 详细文档

- **PRD v1.5**：https://xcnlx9hjxf3f.feishu.cn/wiki/I5fVwdcRCioExIkDIXtcrqdtnUg
- **项目总览**：https://xcnlx9hjxf3f.feishu.cn/wiki/UEYlwE9MQiVmETk2WPlc0b5UnSn
- **数据中台**：https://xcnlx9hjxf3f.feishu.cn/base/Xw4Tb5C8KagMiQswkdacNfVPn8e

---

## 🐛 常见问题

### Q1：为什么 L3_每日指标汇总是空的？
A：需要等到每日凌晨 3:00 自动生成，或手动触发聚合任务

### Q2：日报没有自动推送？
A：检查 HEARTBEAT 定时任务是否配置（crontab -l）

### Q3：HTML Dashboard 无法打开？
A：
1. 检查文件是否存在：`ls ~/.openclaw/workspace/reports/`
2. 右键 → 打开方式 → 选择浏览器
3. 或拖拽文件到浏览器窗口

### Q4：数据不准确怎么办？
A：
1. 检查配置文件：`~/.openclaw/skills/bot-analytics-shared/config.yaml`
2. 确认 App Token 正确：`echo $BITABLE_APP_TOKEN`
3. 查看日志：`tail -f ~/.openclaw/workspace/logs/bot-daily-report.log`

---

## 📦 包含的子 Skill

1. **bot-analytics-collector** v2.1.0 — 数据采集层
2. **bot-daily-report** v2.1.0 — 用户日报
3. **bot-platform-insights** v2.1.0 — 平台洞察

---

## 🎓 技术亮点

1. **会话切割优化**：时间窗口 + 任务边界双约束
2. **三类信号提示**：数据驱动的行动建议
3. **Skill ROI 评分**：成本视角看性价比
4. **多 Skill 协作分析**：拆解协作成本系数
5. **HTML Dashboard**：交互式可视化

---

## 📝 版本历史

### v2.1.0（2026-03-20）
- ✨ 新增三类智能信号提示
- ✨ 新增 HTML Dashboard
- ✨ 新增 Skill ROI 评分
- ✨ 新增多 Skill 协作分析
- ✨ 会话切割优化（时间窗口+任务边界）
- ✨ L2 新增 3 个字段（Skill数量/协作成本系数/关键路径）
- ✨ L3 新增 3 张表（Signal_Alerts/Skill_ROI/Skill_Run）

### v2.0.0（2026-03-18）
- ✨ 生产化改造（App Token 配置化、隐私保护、写入队列）
- ✨ 实时触发 + 归档机制

### v1.0.0（2026-03-18）
- 🎉 初版发布

---

## 📄 许可证

MIT License

---

## 👤 作者

小炸弹 💣 (OpenClaw Agent)

---

## 🙏 致谢

感谢大少爷（陈磊）的全程支持和高效协作 💪  
感谢 OpenClaw 团队提供的强大工具链 🛠️
