# Bot Quality Monitor v3.0.1 Release Notes

**发布日期**: 2026-03-25  
**仓库**: https://github.com/Chenlei105/bot-quality-monitor

---

## 🎯 本次更新重点

**数据上报功能正式可用！**

之前版本（v3.0.0）虽然添加了埋点代码，但只记录到本地日志，没有真正上报到服务器。

本次更新（v3.0.1）补全了完整的上报流程，数据会自动同步到飞书多维表格。

---

## ✨ 新功能

### 1. 真正的数据上报

- ✅ **自动同步**：每天凌晨 2 点自动将本地日志同步到飞书多维表格
- ✅ **集成 OpenClaw**：通过 OpenClaw Agent heartbeat 自动处理
- ✅ **静默埋点**：上报过程完全静默，不影响正常使用
- ✅ **失败保护**：上报失败不影响 Skill 功能，数据保留在本地

### 2. 安装/卸载钩子

- ✅ **自动埋点**：安装/卸载时自动记录事件
- ✅ **无需手动**：用户无需任何操作，自动完成
- ✅ **可追踪**：能准确统计安装量和卸载率

### 3. 隐私保护文档

- ✅ **透明说明**：新增 `DATA_TRACKING.md`，详细说明数据收集范围
- ✅ **一键关闭**：用户可随时通过 `export SKILL_TRACKING=off` 关闭
- ✅ **完全匿名**：用户 ID 是单向 hash，不可反推真实身份

---

## 🔧 技术改进

### 更新的文件

1. **scripts/track-usage.py**
   - 补全 `sync_to_bitable()` 函数
   - 改为生成待上报数据文件，由 OpenClaw Agent 自动上报
   - 优化错误处理，静默失败

2. **hooks/install.sh**（新增）
   - 安装时自动调用 `track-usage.py install`
   - 记录安装事件到本地日志

3. **hooks/uninstall.sh**（新增）
   - 卸载时自动调用 `track-usage.py uninstall`
   - 记录卸载事件到本地日志

4. **DATA_TRACKING.md**（新增）
   - 详细说明数据收集范围和隐私保护措施
   - 提供关闭数据上报的方法

5. **UPDATE_GUIDE.md**（新增）
   - 为已安装用户提供更新指南

---

## 📊 数据上报流程

```
用户安装 Skill
    ↓
hooks/install.sh 执行
    ↓
记录到本地日志（~/.openclaw/workspace/logs/skill-usage.jsonl）
    ↓
每天凌晨 2 点 cron 触发 sync
    ↓
生成待上报数据（skill-usage-sync.json）
    ↓
OpenClaw Agent heartbeat 检测到待同步数据
    ↓
调用飞书 API 批量上报
    ↓
上报成功，归档本地日志（.uploaded.*）
```

---

## 🔄 如何更新

### 方法 1：Git Pull

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
git pull origin main
```

### 方法 2：重新克隆

```bash
cd ~/.openclaw/workspace/skills
rm -rf bot-quality-monitor
git clone https://github.com/Chenlei105/bot-quality-monitor.git
```

详见 [UPDATE_GUIDE.md](./UPDATE_GUIDE.md)

---

## 🐛 Bug 修复

- 修复：v3.0.0 中 `sync_to_bitable()` 函数只打印提示，没有实际上报
- 修复：缺少安装/卸载钩子，无法自动埋点

---

## 📈 后续计划

- [ ] 发布到 clawhub（等待用户反馈后）
- [ ] 添加数据可视化 Dashboard（查看安装量趋势）
- [ ] 支持更多埋点事件（如错误上报）

---

## 📞 反馈与支持

- **Issues**: https://github.com/Chenlei105/bot-quality-monitor/issues
- **Discussions**: https://github.com/Chenlei105/bot-quality-monitor/discussions

---

**感谢所有早期用户的支持！** 🎉
