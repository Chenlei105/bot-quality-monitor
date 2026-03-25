# Bot Quality Monitor - 更新指南

**最新版本**: v3.0.1  
**发布日期**: 2026-03-25  
**仓库地址**: https://github.com/Chenlei105/bot-quality-monitor

---

## 🎉 v3.0.1 更新内容

### ✅ 新功能

1. **真正的数据上报功能**
   - 修复：之前只记录本地日志，现在能真正上报到飞书多维表格
   - 新增：自动同步流程（每天凌晨 2 点）
   - 新增：安装/卸载钩子，自动埋点

2. **隐私保护增强**
   - 新增：`DATA_TRACKING.md` 隐私说明文档
   - 支持：一键关闭数据上报（`export SKILL_TRACKING=off`）
   - 保证：数据完全匿名，不可反推真实身份

3. **自动化改进**
   - 集成：OpenClaw Agent heartbeat 自动同步
   - 优化：静默埋点，不影响 Skill 正常使用
   - 新增：本地日志归档机制

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
