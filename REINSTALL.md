# 🔄 彻底卸载并重新安装 Bot Quality Monitor

---

## 为什么要重装？

体验全新的安装流程：
- ✅ 安装输出增加功能介绍（新用户知道能干什么）
- ✅ 创建后增加完整欢迎指南（授权说明、数据采集、接下来做什么）
- ✅ 子 Skill 自动安装到正确位置

---

## 完整操作步骤

### 第一步：彻底卸载

```bash
# 1. 进入 Skill 目录
cd ~/.openclaw/workspace/skills/bot-quality-monitor

# 2. 执行卸载脚本（会自动删除子 Skill）
./hooks/uninstall.sh

# 3. 删除主目录
cd ~/.openclaw/workspace/skills
rm -rf bot-quality-monitor

# 4. 删除子 Skill 目录（确保干净）
rm -rf bot-analytics-collector
rm -rf bot-daily-report
rm -rf bot-platform-insights

# 5. 删除本地日志（可选）
rm -f ~/.openclaw/workspace/logs/bot-analytics-error.log
rm -f ~/.openclaw/workspace/logs/collected-sessions.json

# 6. 删除配置（可选，会重新生成）
rm -f ~/.openclaw/workspace/skills/bot-quality-monitor/config.json
```

> ⚠️ 注意：飞书多维表格 **不会自动删除**，如果你想删除数据，按下面的步骤手动删除。

---

## 如何手动删除飞书多维表格

### 方法一：从多维表格列表删除

1. 打开飞书，点击左侧 **"云空间"**
2. 点击 **"多维表格"**
3. 找到 **"Bot Quality Monitor"** 这个应用
4. 鼠标右键点击 → **删除**（或点击右上角更多按钮 → 删除）
5. 确认删除

### 方法二：从应用管理删除

1. 打开飞书，点击左侧 **"管理后台"**（需要管理员权限）
2. 点击 **"应用管理"**
3. 搜索 **"Bot Quality Monitor"**
4. 点击进入应用详情
5. 点击 **"删除应用"**
6. 确认删除

### 方法三：从 Bot 创建的多维表格删除

如果你的 Bot 创建了多维表格但你不知道在哪：

1. 让 Bot 查询：`/dashboard` 或查看配置中的 `bitableAppToken`
2. 或者直接去飞书云空间 → 多维表格，搜索包含 "Bot Quality Monitor" 或 "L1_" "L2_" "L3_" 的表格
3. 删除这些表格即可

### 方法四：用脚本删除（命令行操作）

如果你在服务器上直接操作，也可以用我们提供的脚本：

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./hooks/delete-bitable.sh
```

脚本会：
1. 让你选择删除方式（输入 App Token / 让 Bot 帮忙查 / 取消）
2. 确认后才执行删除
3. 提供飞书手动操作替代方案

> ⚠️ 脚本需要你的 Bot 有多维表格管理权限才能真正删除。

---

### 确认删除干净

删除后，**重新安装时会创建全新的多维表格**，数据不会混在一起。

---

### 第二步：重新安装

```bash
# 1. 进入 Skills 目录
cd ~/.openclaw/workspace/skills

# 2. 克隆最新代码
git clone https://github.com/Chenlei105/bot-quality-monitor.git

# 3. 进入目录
cd bot-quality-monitor

# 4. 执行安装脚本
./hooks/install.sh
```

安装脚本会自动：
- ✅ 安装 Python 依赖（plotly、jinja2）
- ✅ 创建目录（reports/）
- ✅ 生成配置文件模板
- ✅ **自动安装子 Skill** 到 skills/ 根目录 ← 新功能
- ✅ 显示功能介绍（新用户知道能干什么）← 新功能

---

### 第三步：创建数据表

安装完成后，**对你的 Bot 说一句话**：

```
帮我创建 Bot 质量监控数据表
```

Bot 会全自动：
1. 创建飞书多维表格应用（12 张表）
2. 自动生成配置
3. **输出完整的欢迎指南** ← 新功能（包含授权说明、数据采集、接下来做什么）

---

## 验证安装成功

```bash
# 检查 Skill 是否都安装了
openclaw skill list | grep bot
```

应该看到：
```
bot-quality-monitor      v4.0.0  智能 Bot 健康监控系统
bot-analytics-collector  v4.0.0  Bot 对话数据采集器
bot-daily-report         v4.0.0  Bot 健康度日报生成器
bot-platform-insights    v4.0.0  Bot 平台级洞察引擎
```

---

## 体验新流程

| 步骤 | 用户看到的 |
|------|-----------|
| 1. `./hooks/install.sh` | 安装输出显示功能介绍（安装这个 Skill 能干什么） |
| 2. 对 Bot 说"帮我创建..." | Bot 创建数据表 |
| 3. 创建完成后 | Bot 输出完整欢迎指南（授权说明、数据采集、接下来做什么） |
| 4. 输入 `/health` | 立即看到健康度（如果有数据） |
| 5. 等待 22:00 | 收到健康度日报 |

---

## 常见问题

### Q: 卸载后飞书多维表格还在吗？

**A**: 在的，卸载脚本不会删除飞书上的数据。如果想删掉，重新安装前手动去飞书删除那个多维表格应用。

### Q: 数据会丢失吗？

**A**: 如果不删多维表格，数据不会丢失。重新安装后配置指向同一个多维表格，数据会自动继续积累。

### Q: 需要重启 OpenClaw 吗？

**A**: 不需要，Heartbeat 会自动识别新安装的 Skill。