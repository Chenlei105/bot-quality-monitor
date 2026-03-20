# Bot Quality Monitor 发布指南（skillhub）

**版本**: 2.1.0  
**发布日期**: 2026-03-20  
**发布人**: 小炸弹 💣

---

## 📋 发布前检查清单

### 1. 文件结构确认
```
bot-quality-monitor/
├── SKILL.md                          # Skill 主文档（必须）
├── package.json                      # 包信息（必须）
├── PUBLISH-GUIDE.md                  # 本文件
├── scripts/                          # 脚本目录
│   ├── create-tables.py              # 建表脚本
│   ├── generate-dashboard.py         # Dashboard 生成
│   ├── generate-signal-alerts.py     # 信号生成
│   └── daily-report.sh               # 日报任务
└── README.md                         # 可选
```

### 2. 版本号确认
- [x] package.json version: 2.1.0 ✅
- [x] SKILL.md 版本号: 2.1.0 ✅

### 3. 依赖检查
- [x] OpenClaw 最低版本: 2026.3.8 ✅
- [x] Python 3.x ✅
- [x] 飞书多维表格 API 权限 ✅

---

## 🚀 发布步骤（详细版）

### Step 1：检查 skillhub CLI 是否安装

```bash
# 检查 skillhub 命令
which skillhub

# 如果未安装，执行：
npm install -g skillhub-cli
```

### Step 2：登录 skillhub

```bash
# 登录（首次需要）
skillhub login

# 系统会提示输入：
# - 用户名
# - 密码
# - 或使用 GitHub OAuth
```

### Step 3：验证 Skill 包结构

```bash
# 进入 Skill 目录
cd /root/.openclaw/workspace/skills-publish/bot-quality-monitor

# 验证结构
skillhub validate .

# 应输出：
# ✅ SKILL.md found
# ✅ package.json found
# ✅ Version: 2.1.0
# ✅ Structure is valid
```

### Step 4：发布到 skillhub（beta）

```bash
# 发布到 beta 频道（推荐先 beta 测试）
skillhub publish --channel beta

# 或发布到稳定版（stable）
skillhub publish --channel stable
```

**发布过程**：
1. 压缩 Skill 包
2. 上传到 skillhub 服务器
3. 生成版本号（2.1.0-beta.1）
4. 返回发布 URL

**预期输出**：
```
📦 Packaging bot-quality-monitor@2.1.0...
✅ Package created: bot-quality-monitor-2.1.0.tgz (25KB)
🚀 Publishing to skillhub (beta)...
✅ Published successfully!

📖 Skill URL: https://skillhub.com/skills/bot-quality-monitor
🔗 Install: skillhub install bot-quality-monitor@beta
```

### Step 5：验证发布成功

```bash
# 搜索已发布的 Skill
skillhub search bot-quality-monitor

# 应输出：
# bot-quality-monitor@2.1.0-beta.1
#   OpenClaw Bot 质量监控 Skill 体系
#   By: 小炸弹 💣
#   Downloads: 0
```

### Step 6：测试安装（重要）

```bash
# 在另一个环境测试安装
skillhub install bot-quality-monitor@beta

# 检查文件
ls -la ~/.openclaw/skills/bot-quality-monitor/

# 运行初始化
/init bot-quality-monitor
```

---

## 🔄 更新已发布的 Skill

### 情况 1：修复 Bug（发布 patch 版本）

```bash
# 修改版本号：2.1.0 → 2.1.1
# 编辑 package.json:
# "version": "2.1.1"

# 重新发布
skillhub publish --channel beta
```

### 情况 2：新增功能（发布 minor 版本）

```bash
# 修改版本号：2.1.0 → 2.2.0
# 编辑 package.json:
# "version": "2.2.0"

# 更新 SKILL.md 版本历史
# 重新发布
skillhub publish --channel beta
```

### 情况 3：撤回发布

```bash
# 撤回指定版本
skillhub unpublish bot-quality-monitor@2.1.0-beta.1

# 确认撤回
# Are you sure? (yes/no): yes
```

---

## 📊 发布后监控

### 查看下载统计

```bash
skillhub stats bot-quality-monitor

# 输出：
# Total Downloads: 0
# Weekly Downloads: 0
# Latest Version: 2.1.0-beta.1
```

### 查看用户反馈

```bash
skillhub reviews bot-quality-monitor

# 输出用户评价和问题
```

---

## 🐛 常见问题

### Q1：发布时提示 "Authentication failed"
**解决方案**：
```bash
# 重新登录
skillhub logout
skillhub login
```

### Q2：发布时提示 "Version already exists"
**解决方案**：
```bash
# 更新版本号（package.json）
# 2.1.0 → 2.1.1

# 或强制覆盖（不推荐）
skillhub publish --force
```

### Q3：发布后用户无法安装
**解决方案**：
```bash
# 检查包结构
skillhub validate .

# 检查依赖
cat package.json | grep dependencies

# 重新发布
skillhub publish --channel beta
```

### Q4：如何从 beta 升级到 stable？
**解决方案**：
```bash
# 测试充分后，发布到 stable
skillhub publish --channel stable

# 用户可通过以下方式安装：
skillhub install bot-quality-monitor
# 或
skillhub install bot-quality-monitor@stable
```

---

## 📝 发布检查清单（最终版）

**发布前**：
- [x] SKILL.md 完整且格式正确 ✅
- [x] package.json 版本号正确 ✅
- [x] 所有脚本文件已复制 ✅
- [x] 依赖声明完整 ✅
- [x] 本地测试通过 ✅

**发布时**：
- [ ] skillhub login 登录成功
- [ ] skillhub validate 验证通过
- [ ] skillhub publish --channel beta 发布成功
- [ ] 发布 URL 可访问

**发布后**：
- [ ] skillhub search 能找到
- [ ] 在另一环境测试安装
- [ ] 运行 /init 初始化成功
- [ ] 功能验证通过
- [ ] 监控下载量和反馈

---

## 🚀 下一步

1. **beta 测试**（1-2 周）
   - 收集用户反馈
   - 修复 Bug
   - 优化文档

2. **发布 stable**
   ```bash
   skillhub publish --channel stable
   ```

3. **推广**
   - OpenClaw 官方论坛发帖
   - 飞书群分享
   - 撰写使用教程

4. **维护**
   - 定期更新版本
   - 响应用户 Issue
   - 持续优化

---

*发布人：小炸弹 💣 · 2026-03-20*
