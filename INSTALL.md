# Bot Quality Monitor 安装指南

**版本**: 2.1.0  
**更新时间**: 2026-03-20

---

## 📥 下载与安装

### 方法 1：从飞书云盘下载（推荐）

**Step 1：下载文件**
- 文件名：`bot-quality-monitor-2.1.0.tar.gz`（12.5KB）
- 下载链接：（请联系大少爷获取飞书云盘分享链接）

**Step 2：解压安装**
```bash
# 解压到 OpenClaw skills 目录
tar -xzf bot-quality-monitor-2.1.0.tar.gz -C ~/.openclaw/skills/

# 验证安装
ls ~/.openclaw/skills/bot-quality-monitor/
```

**Step 3：初始化配置**
```bash
/init bot-quality-monitor
```

系统会提示输入：
1. **飞书多维表格 App Token**：你的数据中台 Token
2. **时区**：GMT+8（中国标准时间）
3. **是否存储消息内容**：建议选 No（隐私保护）

---

### 方法 2：手动创建（适合定制）

**Step 1：创建目录**
```bash
mkdir -p ~/.openclaw/skills/bot-quality-monitor/scripts
```

**Step 2：下载文件**
从以下位置下载所需文件：
- `SKILL.md`
- `package.json`
- `scripts/create-tables.py`
- `scripts/generate-dashboard.py`
- `scripts/generate-signal-alerts.py`
- `scripts/daily-report.sh`

**Step 3：设置权限**
```bash
chmod +x ~/.openclaw/skills/bot-quality-monitor/scripts/*.sh
```

**Step 4：初始化**
```bash
/init bot-quality-monitor
```

---

## ⚙️ 配置

### 1. 设置环境变量

```bash
# 编辑 ~/.bashrc 或 ~/.zshrc
export BITABLE_APP_TOKEN="你的飞书多维表格AppToken"

# 重新加载
source ~/.bashrc
```

### 2. 创建数据表

**选项 A：使用现有数据中台**
- App Token: `Xw4Tb5C8KagMiQswkdacNfVPn8e`
- 访问：https://xcnlx9hjxf3f.feishu.cn/base/Xw4Tb5C8KagMiQswkdacNfVPn8e

**选项 B：创建新表**
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

# 添加以下行：
# 每日 22:00 生成日报
0 22 * * * ~/.openclaw/skills/bot-quality-monitor/scripts/daily-report.sh

# 每周日 20:00 生成周报（待实现）
# 0 20 * * 0 ~/.openclaw/skills/bot-quality-monitor/scripts/weekly-insights.sh
```

---

## ✅ 验证安装

### 1. 检查文件结构

```bash
ls -la ~/.openclaw/skills/bot-quality-monitor/

# 应包含：
# SKILL.md
# package.json
# scripts/
```

### 2. 测试生成 Dashboard

```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/generate-dashboard.py

# 检查输出文件
ls ~/.openclaw/workspace/reports/bot-daily-*.html
```

### 3. 测试生成信号

```bash
python3 ~/.openclaw/skills/bot-quality-monitor/scripts/generate-signal-alerts.py

# 应输出：
# ✅ 检测到 X 个高分低用 Bot
# ✅ 检测到 Y 个低分高风险 Bot
# ✅ 检测到 Z 个高风险任务场景
```

---

## 🐛 常见问题

### Q1：提示 "ModuleNotFoundError: No module named 'feishu_bitable'"
**解决方案**：
```bash
# 安装飞书 SDK（如果需要）
pip3 install feishu-sdk
```

### Q2：定时任务不执行
**解决方案**：
```bash
# 检查 crontab 配置
crontab -l

# 检查日志
tail -f ~/.openclaw/workspace/logs/bot-daily-report.log
```

### Q3：数据表无法写入
**解决方案**：
1. 检查 App Token 是否正确：`echo $BITABLE_APP_TOKEN`
2. 确认表 ID 是否匹配（config.yaml）
3. 检查飞书权限设置

---

## 📚 更多文档

- **SKILL.md**：完整功能说明
- **PUBLISH-GUIDE.md**：发布指南
- **PRD v1.5**：https://xcnlx9hjxf3f.feishu.cn/wiki/I5fVwdcRCioExIkDIXtcrqdtnUg

---

## 🆘 获取帮助

遇到问题请：
1. 查看 SKILL.md 常见问题章节
2. 检查日志：`~/.openclaw/workspace/logs/`
3. 联系大少爷（陈磊）

---

*安装指南 v2.1.0 · 2026-03-20*
