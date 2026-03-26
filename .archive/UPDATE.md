# 🔄 Bot Quality Monitor 更新指南

---

## 快速更新

如果你已经安装过 Bot Quality Monitor，按以下步骤更新到最新版本：

```bash
# 1. 进入 Skill 目录
cd ~/.openclaw/workspace/skills/bot-quality-monitor

# 2. 拉取最新代码
git pull origin main

# 3. 执行更新脚本
./hooks/install.sh
```

---

## 更新内容 (v4.0.0)

### v4.0.0 (2026-03-26)
- ✅ GitHub 安装支持全自动子 Skill 安装
- ✅ GitHub 安装支持全自动子 Skill 卸载
- ✅ 安装输出增加功能介绍（新用户知道能干什么）
- ✅ 创建后增加完整欢迎指南（授权说明、数据采集、接下来做什么）

---

## 如果遇到问题

### 1. git pull 失败（本地有修改）

```bash
# 放弃本地修改，重新拉取
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git checkout .
git pull origin main
./hooks/install.sh
```

### 2. 子 Skill 找不到

重新运行安装脚本会自动复制子 Skill：

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./hooks/install.sh
```

### 3. 完全重装

如果想重新安装，先卸载再重新安装：

```bash
# 卸载
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./hooks/uninstall.sh

# 删除目录
cd ~/.openclaw/workspace/skills
rm -rf bot-quality-monitor bot-analytics-collector bot-daily-report bot-platform-insights

# 重新安装
git clone https://github.com/Chenlei105/bot-quality-monitor.git
cd bot-quality-monitor
./hooks/install.sh
```

---

## 版本发布历史

查看 [CHANGELOG.md](./CHANGELOG.md) 了解完整版本历史。