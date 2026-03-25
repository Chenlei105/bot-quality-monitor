# Bot Quality Monitor - 更新指南

**最新版本**: v4.0.0  
**发布日期**: 2026-03-25  
**仓库地址**: https://github.com/Chenlei105/bot-quality-monitor

---

## 🎉 v4.0.0 更新内容

### ✅ 重大更新 - 全自动傻瓜式安装

1. **全自动创建多维表格**
   - 新增：`scripts/auto-create-bitable.py` 一键创建
   - 用户只需要说一句话：**帮我创建 Bot 质量监控数据表**
   - Bot 自动创建 12 张表 + 自动生成 `config.json` + 配置完成

2. **安装脚本增强**
   - 自动检查并安装 Python 依赖（plotly + jinja2）
   - 自动创建 `reports` 目录
   - 自动生成 `config.json` 模板带完整默认配置

3. **废弃手动 crontab**
   - 完全基于 OpenClaw 原生 Heartbeat 驱动
   - 用户无需编辑 crontab，开箱即用
   - 每分钟检查，时间到点自动执行

4. **完整数据表结构**
   - 一次性创建 12 张表（包含归档表和聚合表）
   - 所有字段类型自动配置正确

5. **文档全面重构**
   - INSTALL.md 完全重写，傻瓜式流程
   - 所有版本号统一更新到 4.0.0
   - 添加完整的故障排查和卸载说明

### 从 v3.x 更新到 v4.0.0

不需要重新配置，现有配置兼容。如果想体验全自动安装，可以：
```bash
# 备份原有配置
cp ~/.openclaw/workspace/skills/bot-quality-monitor/config.json ~/bm-config-backup.json

# 拉取更新
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main

# 重新运行安装脚本（会保留你的现有配置）
./hooks/install.sh
```

---

## 📥 如何更新

### 方法 1：Git Pull（推荐）

如果您是通过 `git clone` 安装的：

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main
```

### 方法 2：重新安装

如果您不确定安装方式，可以直接重新克隆：

```bash
# 备份旧版本（可选）
cd ~/.openclaw/workspace/skills
mv bot-quality-monitor bot-quality-monitor.backup

# 克隆最新版本
git clone https://github.com/Chenlei105/bot-quality-monitor.git

# 安装完成后测试
cd bot-quality-monitor
./hooks/install.sh
```

### 方法 3：手动替换

下载最新的 3 个文件：

1. **scripts/track-usage.py**  
   https://github.com/Chenlei105/bot-quality-monitor/blob/main/scripts/track-usage.py

2. **hooks/install.sh**  
   https://github.com/Chenlei105/bot-quality-monitor/blob/main/hooks/install.sh

3. **hooks/uninstall.sh**  
   https://github.com/Chenlei105/bot-quality-monitor/blob/main/hooks/uninstall.sh

替换到 `~/.openclaw/workspace/skills/bot-quality-monitor/` 对应位置。

---

## 🔄 更新后验证

### 1. 检查版本

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git log --oneline -1
```

应该显示：
```
d50e252 feat: 补全数据上报功能
```

### 2. 测试埋点

```bash
python3 scripts/track-usage.py run '{"scene": "test_update"}'
```

应该显示：
```
[track] run | bot-quality-monitor v3.0.0 | 2026-03-25T...
[track] 已记录到 /root/.openclaw/workspace/logs/skill-usage.jsonl
```

### 3. 测试同步

```bash
python3 scripts/track-usage.py sync
```

应该显示：
```
[sync] 准备同步 1 条记录到飞书多维表格
[sync] 目标表: Xw4Tb5C8KagMiQswkdacNfVPn8e/tbllGdVAIIzITahT
[sync] 待上报数据已保存: ~/.openclaw/workspace/logs/skill-usage-sync.json
[sync] OpenClaw Agent 会在下次 heartbeat 时自动上报
```

---

## ❓ 常见问题

### Q1: 更新后数据会丢失吗？

**A**: 不会。所有数据存储在飞书多维表格中，更新 Skill 不影响数据。

---

### Q2: 我需要重新授权吗？

**A**: 不需要。授权信息存储在 OpenClaw 配置中，更新 Skill 不影响授权。

---

### Q3: 更新失败怎么办？

**A**: 如果 `git pull` 失败，直接重新克隆：

```bash
cd ~/.openclaw/workspace/skills
rm -rf bot-quality-monitor
git clone https://github.com/Chenlei105/bot-quality-monitor.git
```

---

### Q4: 我不想上报数据，怎么关闭？

**A**: 设置环境变量：

```bash
export SKILL_TRACKING=off
```

详见 [DATA_TRACKING.md](./DATA_TRACKING.md)

---

## 📞 支持

- **Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions

---

**感谢使用 Bot Quality Monitor！** 🎉
