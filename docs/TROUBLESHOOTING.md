# 故障排查指南

## 常见问题与解决方案

### 1. 创建表格失败

**症状**：
- 用户说"创建表格"后，Bot 没有响应
- 或者报错："创建失败"

**可能原因**：
1. 飞书应用权限不足
2. 网络连接问题
3. 用户 Bot 未正确配置飞书凭证

**解决方案**：

**步骤 1**：检查飞书应用权限
```bash
# 检查 openclaw.json 中的飞书配置
cat ~/.openclaw/openclaw.json | grep -A 10 "feishu"
```

确保有以下权限：
- `bitable:app:create` - 创建多维表格
- `bitable:app:write` - 写入数据
- `im:message:send` - 发送消息

**步骤 2**：检查网络连接
```bash
# 测试飞书 API 连通性
curl -v https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
```

**步骤 3**：查看错误日志
```bash
tail -f ~/.openclaw/workspace/logs/bot-analytics-error.log
```

**步骤 4**：手动重试
```
对 Bot 说："帮我创建 Bot 质量监控数据表"
```

---

### 2. 数据采集不工作

**症状**：
- 表格创建成功
- 但没有新数据写入

**可能原因**：
1. config.json 未正确保存
2. Heartbeat 未运行
3. 表格权限问题

**解决方案**：

**步骤 1**：检查配置文件
```bash
cat ~/.openclaw/workspace/skills/bot-quality-monitor/config.json
```

应该包含：
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "YOUR_APP_TOKEN",  // 不为空
  "receiverOpenId": "YOUR_OPEN_ID",     // 不为空
  "tables": {
    "L2_会话汇总表": "tblXXX"          // 不为空
  }
}
```

**步骤 2**：检查 Heartbeat 是否运行
```bash
# 查看最近的采集日志
cat ~/.openclaw/workspace/logs/collected-sessions.json | jq .
```

应该有最近的采集记录。

**步骤 3**：手动触发采集
```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
python3 bot-analytics-collector/auto-collect.py
```

---

### 3. 日报未推送

**症状**：
- 到了推送时间（默认 22:00）
- 但没有收到日报

**可能原因**：
1. 表格中没有数据
2. 推送时间配置错误
3. Bot 未运行

**解决方案**：

**步骤 1**：检查表格数据
访问你的飞书多维表格，确认 L2_会话汇总表 有数据。

**步骤 2**：检查推送时间配置
```bash
cat ~/.openclaw/workspace/skills/bot-quality-monitor/config.json | grep reportTime
```

**步骤 3**：手动生成日报
```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor/bot-daily-report
python3 scripts/generate-signal-alerts.py
```

---

### 4. 权限错误

**症状**：
- 报错："Permission denied"
- 或者："Access token invalid"

**可能原因**：
1. 飞书 token 过期
2. 应用权限不足
3. 表格被删除或移动

**解决方案**：

**步骤 1**：重新授权
```
对 Bot 说："/oauth revoke"
然后重新创建表格
```

**步骤 2**：检查表格是否存在
访问 config.json 中的 bitableAppToken 对应的表格链接：
```
https://www.feishu.cn/base/{bitableAppToken}
```

如果 404，说明表格已删除。

**步骤 3**：重新创建表格
```bash
# 清空配置
rm ~/.openclaw/workspace/skills/bot-quality-monitor/config.json

# 重新创建
对 Bot 说："帮我创建 Bot 质量监控数据表"
```

---

### 5. 跨企业数据未上报

**症状**：
- 中央统计表格没有其他用户的数据
- 只有自己的数据

**可能原因**：
1. 其他用户的 Bot 未更新 Skill
2. Webhook 上报失败
3. 网络连接问题

**解决方案**：

**步骤 1**：确认其他用户已安装
联系其他用户，确认他们已执行：
```bash
openclaw skill install bot-quality-monitor
```

**步骤 2**：检查 Webhook 上报日志
```bash
# 其他用户的机器上执行
cat ~/.openclaw/workspace/logs/skill-usage.jsonl
```

应该有 install 事件记录。

**步骤 3**：手动触发同步
```bash
# 其他用户的机器上执行
cd ~/.openclaw/workspace/skills/bot-quality-monitor
python3 scripts/track-usage.py sync
```

检查飞书群消息是否收到数据上报卡片。

**步骤 4**：检查小炸弹的自动入库
中央表格维护者（大少爷）检查：
```bash
cat ~/.openclaw/workspace/logs/processed-webhook-messages.json | jq .
```

应该有已处理的 message_id。

---

### 6. 性能问题

**症状**：
- Bot 响应变慢
- Heartbeat 执行时间过长
- 飞书 API 限流

**可能原因**：
1. 会话数量过多
2. 批量写入数据过大
3. 网络延迟高

**解决方案**：

**步骤 1**：检查会话数量
```bash
cat ~/.openclaw/workspace/logs/collected-sessions.json | jq '. | length'
```

如果超过 1000 个会话，考虑清理旧数据。

**步骤 2**：调整采集频率
修改 HEARTBEAT.md：
```markdown
**性能优化**：
- 单次 Heartbeat 最多采集 10 个会话（原来 20 个）
- 批量写入阈值：攒够 20 条（原来 10 条）
```

**步骤 3**：启用归档机制
```bash
# 归档 90 天前的数据
cd ~/.openclaw/workspace/skills/bot-quality-monitor
python3 scripts/archive-old-data.py
```

---

## 日志位置

| 日志文件 | 用途 |
|----------|------|
| `~/.openclaw/workspace/logs/collected-sessions.json` | 已采集会话记录 |
| `~/.openclaw/workspace/logs/bot-analytics-error.log` | 采集错误日志 |
| `~/.openclaw/workspace/logs/skill-usage.jsonl` | Skill 使用埋点 |
| `~/.openclaw/workspace/logs/processed-webhook-messages.json` | 已处理 Webhook 消息 |
| `~/.openclaw/workspace/logs/webhook-processing-error.log` | Webhook 处理错误 |

---

## 诊断命令

### 完整健康检查
```bash
cd ~/.openclaw/workspace/skills/bot-quality-monitor
python3 scripts/health-check.py
```

输出示例：
```
✅ 配置文件存在
✅ 飞书表格可访问
✅ Heartbeat 正常运行
⚠️  最近 1 小时未采集新数据
❌ Webhook 上报失败（网络错误）

建议：
1. 检查网络连接
2. 重试 Webhook 同步
```

### 查看最近采集
```bash
cat ~/.openclaw/workspace/logs/collected-sessions.json | jq '.[-5:]'
```

### 查看错误日志
```bash
tail -100 ~/.openclaw/workspace/logs/bot-analytics-error.log
```

---

## 紧急恢复

如果所有方法都失败，执行完整重置：

```bash
# 1. 备份旧数据（可选）
cp ~/.openclaw/workspace/skills/bot-quality-monitor/config.json ~/config.json.backup

# 2. 删除表格（如果需要）
bash ~/.openclaw/workspace/skills/bot-quality-monitor/hooks/delete-bitable.sh

# 3. 卸载 Skill
openclaw skill uninstall bot-quality-monitor

# 4. 重新安装
openclaw skill install bot-quality-monitor

# 5. 重新创建表格
对 Bot 说："帮我创建 Bot 质量监控数据表"
```

---

## 联系支持

如果以上方法都无法解决问题，请：

1. **收集诊断信息**：
   ```bash
   bash ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/collect-debug-info.sh > debug.txt
   ```

2. **提交 Issue**：
   访问 https://github.com/Chenlei105/bot-quality-monitor/issues
   
3. **包含以下信息**：
   - 操作系统版本
   - OpenClaw 版本
   - Skill 版本
   - 错误日志
   - 复现步骤

---

## 预防性维护

### 每周检查清单

- [ ] 检查表格数据是否正常增长
- [ ] 查看错误日志是否有异常
- [ ] 验证日报是否按时推送
- [ ] 检查中央表格是否收到数据

### 每月维护

- [ ] 归档 90 天前的数据
- [ ] 清理错误日志
- [ ] 更新 Skill 到最新版本
- [ ] 备份配置文件

```bash
# 月度维护脚本
bash ~/.openclaw/workspace/skills/bot-quality-monitor/scripts/monthly-maintenance.sh
```
