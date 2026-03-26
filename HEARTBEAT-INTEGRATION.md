# HEARTBEAT.md 集成指南

## 📋 问题说明

为了让所有安装了 `bot-quality-monitor` 的机器人能够自动上报使用数据到中央表格，需要在每个机器人的 `~/.openclaw/workspace/HEARTBEAT.md` 中添加同步任务。

**重要**：HEARTBEAT.md 是机器人的本地配置文件，不在 Git 仓库中，需要手动配置。

---

## ✅ 自动配置方法

运行以下命令，自动将同步任务添加到 HEARTBEAT.md：

```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
./scripts/setup-heartbeat.sh
```

---

## 📝 手动配置方法

如果自动脚本失败，请手动编辑 `~/.openclaw/workspace/HEARTBEAT.md`，在文件末尾添加以下内容：

```markdown
## Skill 使用数据同步（每小时）

**执行时间**：每小时一次（整点：XX:00）

**触发条件**：当前时间分钟数为 00

**执行脚本**：`python3 ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/track-usage.py sync`

**执行流程**：
1. **生成同步文件**：
   - 读取本地 `~/.openclaw/workspace/logs/skill-usage.jsonl`
   - 生成 `~/.openclaw/workspace/logs/skill-usage-sync.json`
   
2. **上报数据**：
   - 调用 `feishu_bitable_app_table_record` 批量写入
   - 目标表格：`Xw4Tb5C8KagMiQswkdacNfVPn8e / tbllGdVAIIzITahT`
   
3. **清理归档**：
   - 上报成功后归档本地日志为 `.uploaded.时间戳`
   - 删除 `skill-usage-sync.json`

4. **静默**：无需通知大少爷

**重要**：
- 此任务在**所有安装了 bot-quality-monitor 的机器人**上都会执行
- 每小时自动汇总数据到中央表格
- 中央表格可以看到所有机器人的匿名使用数据
```

---

## 🔍 验证配置

配置完成后，运行以下命令验证：

```bash
# 1. 检查 HEARTBEAT.md 是否包含同步任务
grep -A 5 "Skill 使用数据同步" ~/.openclaw/workspace/HEARTBEAT.md

# 2. 手动触发一次同步测试
cd ~/.openclaw/workspace/skills/bot-quality-monitor
python3 scripts/track-usage.py sync

# 3. 检查是否生成同步文件
ls -lh ~/.openclaw/workspace/logs/skill-usage-sync.json
```

如果看到 `skill-usage-sync.json` 文件生成，说明配置成功。

---

## ⏰ 同步时间说明

- **同步频率**：每小时一次（整点：00:00, 01:00, 02:00, ...）
- **数据延迟**：最多 1 小时
- **中央表格**：`Xw4Tb5C8KagMiQswkdacNfVPn8e / tbllGdVAIIzITahT`

---

## 🐛 故障排查

### 问题 1：数据没有上报

**检查清单**：
1. HEARTBEAT.md 是否包含同步任务？
2. `~/.openclaw/workspace/logs/skill-usage.jsonl` 是否存在？
3. 机器人的 Heartbeat 是否正常运行？
4. 飞书多维表格权限是否正确？

### 问题 2：sync 脚本报错

**可能原因**：
- Python 环境问题
- 文件权限问题
- 路径配置错误

**解决方法**：
```bash
# 检查 Python 版本
python3 --version

# 检查脚本权限
ls -lh ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/track-usage.py

# 手动运行查看错误
python3 ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/track-usage.py sync
```

---

## 📊 查看上报数据

访问中央表格查看所有机器人的数据：

https://www.feishu.cn/base/Xw4Tb5C8KagMiQswkdacNfVPn8e?table=tbllGdVAIIzITahT

---

## 🔐 隐私说明

- **匿名 ID**：基于机器特征的 sha256 hash，不可逆
- **不采集的信息**：真实用户名、飞书 ID、对话内容、IP 地址
- **用户可关闭**：`export SKILL_TRACKING=off`

---

## 📞 获取帮助

如果遇到问题，请查看日志：

```bash
tail -f ~/.openclaw/workspace/logs/bot-analytics-error.log
```

或者联系大少爷（陈磊）。
