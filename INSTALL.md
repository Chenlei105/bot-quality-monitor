# 📦 安装指南

Bot Quality Monitor 提供**两种安装方式**，您可以根据自己的习惯选择：

---

## 🤖 方式一：纯 Bot 对话安装（推荐，零命令行）

**适合人群**：所有用户，尤其是不熟悉命令行的用户

### Step 1: 安装 Skill（从 GitHub）

**发送给 Bot**（**必须指定从 GitHub 安装**）：
```
帮我从 GitHub 安装 https://github.com/Chenlei105/bot-quality-monitor
```

或者简洁版（如果 Bot 支持自动识别）：
```
安装 Chenlei105/bot-quality-monitor
```

⚠️ **重要**：
- 必须明确指定 **GitHub** 或 **完整 GitHub 链接**
- 不要说"帮我安装 bot-quality-monitor"（会去 SkillHub/ClawHub）
- 正确示例：`从 GitHub 安装 bot-quality-monitor`

Bot 会自动：
1. 从 GitHub 克隆仓库
2. 安装到 `~/.openclaw/workspace/skills/bot-quality-monitor/`
3. 回复安装成功

### Step 2: 创建监控表格

**发送给 Bot**：
```
帮我创建 Bot 质量监控数据表
```

Bot 会自动：
1. 在**你的飞书空间**创建多维表格
2. 批量创建 12 张数据表
3. 添加 100+ 个字段
4. 写入 70 条测试数据（7 天数据）
5. 保存配置到 `~/.openclaw/workspace/skills/bot-quality-monitor/config.json`

**预计耗时**: 2-3 分钟

### Step 3: 验证安装

**发送给 Bot**：
```
/health
```

如果看到类似回复，说明安装成功：
```
📊 综合健康度: 82 分 (较昨日 +3)
├─ 质量维度: 85 分 (+2)
├─ 效率维度: 80 分 (+5)
└─ 资源维度: 78 分 (+1)

━━━━━━━━━━ 关键指标 ━━━━━━━━━━
📈 会话数: 156 (+12%)
✅ 完成率: 89% (+5%)
🔄 纠错率: 4% (-2%)
```

### Step 4: 查看你的表格

**发送给 Bot**：
```
给我看一下监控表格的链接
```

Bot 会回复飞书表格链接，点击即可查看。

---

## 💻 方式二：命令行安装（开发者推荐）

**适合人群**：熟悉命令行、需要自定义配置的用户

### Step 1: 克隆仓库

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/Chenlei105/bot-quality-monitor.git
```

### Step 2: 自动安装

**方式 2A: 通过 Bot 安装（推荐）**

发送给 Bot：
```
帮我创建 Bot 质量监控数据表
```

**方式 2B: 手动运行脚本**

```bash
# 获取你的 open_id（从飞书复制）
YOUR_OPEN_ID="ou_xxxxxxxxxxxxxx"

# 运行安装脚本
python3 ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/auto-setup-v5.py $YOUR_OPEN_ID
```

脚本会输出 JSON 工作流，需要你的 Bot 执行。

### Step 3: 验证安装

```bash
# 检查配置文件
cat ~/.openclaw/workspace/skills/bot-quality-monitor/config.json

# 测试健康度查询
# 发送给 Bot: /health
```

---

## ⚙️ 配置说明

### 配置文件位置
```
~/.openclaw/workspace/skills/bot-quality-monitor/config.json
```

### 配置示例
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "YnD8bXLLqaURZGsGPJFceGaxnVf",
  "receiverOpenId": "ou_baa3525cf6cb5c0fc1ce4e26753d812d",
  "tables": {
    "L2_会话汇总表": "tblxxxxxx",
    "L3_每日指标汇总": "tblxxxxxx",
    ...
  }
}
```

### 可自定义项

#### 修改推送时间

**发送给 Bot**：
```
/settime 21:00
```

或手动编辑 config.json：
```json
{
  "reportTime": "21:00"
}
```

#### 修改时区

**发送给 Bot**：
```
/settz GMT+8
```

或手动编辑 config.json：
```json
{
  "timezone": "GMT+8"
}
```

---

## 🔍 验证安装成功

### 检查清单

- [ ] **Skill 已安装**: `ls ~/.openclaw/workspace/skills/bot-quality-monitor/`
- [ ] **配置文件存在**: `~/.openclaw/workspace/skills/bot-quality-monitor/config.json`
- [ ] **飞书表格已创建**: 打开配置文件中的 `bitableAppToken` 对应的表格链接
- [ ] **表格包含 12 张表**: 在飞书表格中看到 12 张数据表
- [ ] **L2 表有数据**: 查看 L2_会话汇总表，应该有 70 条测试数据
- [ ] **Bot 响应 /health**: 发送 `/health` 能看到健康度数据

### 常见问题

#### Q1: Bot 说"未安装该 Skill"
**解决**：
```
帮我从 GitHub 安装 https://github.com/Chenlei105/bot-quality-monitor
```

**为什么必须指定 GitHub？**
- SkillHub/ClawHub 可能没有最新版本（v5.0.0）
- GitHub 是官方源，保证最新、最稳定
- 避免版本不匹配导致的功能缺失

#### Q1.5: 我说"安装 bot-quality-monitor"，Bot 去了 SkillHub
**解决**：明确指定来源
```
从 GitHub 安装 bot-quality-monitor
```
或
```
安装 https://github.com/Chenlei105/bot-quality-monitor
```

#### Q2: 创建表格时报错"权限不足"
**解决**：
1. 确认你的飞书账号有创建多维表格的权限
2. 尝试手动在飞书创建一个测试表格，如果能创建，说明有权限

#### Q3: /health 返回"暂无数据"
**正常情况**：刚安装时确实没有真实数据，需要：
- 等待 24 小时数据积累
- 或查看测试数据：发送 `/createdemo`

#### Q4: 想重新安装
**解决**：
```bash
# 删除旧的 Skill
rm -rf ~/.openclaw/workspace/skills/bot-quality-monitor/

# 重新安装（方式一的 Step 1）
# 发送给 Bot: 帮我安装 bot-quality-monitor
```

---

## 📊 安装后的第一步

### 1. 查看你的监控表格

**发送给 Bot**：
```
给我看一下监控表格的链接
```

点击链接，你会看到：
- 12 张数据表
- L2_会话汇总表有 70 条测试数据
- 100+ 个字段已就绪

### 2. 查看健康度

**发送给 Bot**：
```
/health
```

查看基于测试数据的健康度报告。

### 3. 生成 Dashboard

**发送给 Bot**：
```
/dashboard
```

Bot 会生成交互式 Dashboard HTML，可以用浏览器打开查看。

### 4. 设置推送时间

**发送给 Bot**：
```
/settime 21:00
```

修改日报推送时间（默认 22:00）。

### 5. 开始真实使用

从现在开始，正常与 Bot 对话，数据会自动积累：
- 每分钟自动采集会话数据
- 每日 22:00 自动推送健康度日报
- 每周日 20:00 推送平台周报（给大少爷）

---

## 🎯 下一步

### 对于普通用户
1. ✅ 安装完成
2. ⏳ 等待 24 小时数据积累
3. 📊 第二天 22:00 收到第一份完整日报

### 对于开发者
1. ✅ 安装完成
2. 🔧 自定义配置（时间/时区/字段）
3. 📈 接入自己的数据源（修改 collect-sessions.py）

---

## 📚 相关文档

- [README.md](README.md) - 项目介绍
- [SKILL.md](SKILL.md) - Skill 使用说明
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志
- [HEARTBEAT.md](HEARTBEAT.md) - 定时任务配置

---

**需要帮助？**
- GitHub Issues: https://github.com/Chenlei105/bot-quality-monitor/issues
- 发送给 Bot: `/help`
