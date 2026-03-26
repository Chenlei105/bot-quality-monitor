# 授权模型与配置管理

## 授权模型

Bot Quality Monitor 使用**分层授权模型**：

### 层级 1：OpenClaw 内部权限（自动）

```
OpenClaw Agent
  ↓ 内置权限
  - sessions_list（读取会话列表）
  - sessions_history（读取会话历史）
  - 读取本地文件系统
```

**无需额外授权**，OpenClaw Agent 自动拥有这些权限。

---

### 层级 2：飞书机器人权限（管理员授权一次）

```
飞书开放平台
  ↓ 应用权限配置
  - bitable:app:read（读取多维表格）
  - bitable:app:write（写入多维表格）
  - im:message:send（发送消息）
  - im:message:read（读取消息）
```

**授权方式**：
- 管理员在飞书开放平台配置应用权限
- 配置一次后，所有用户自动生效
- **用户无需单独授权**

**当前状态**：
- ✅ 已配置（大少爷的飞书应用）
- ✅ 所有功能正常工作

---

### 层级 3：用户 OAuth 授权（可选，取决于功能）

#### 场景 A：数据流 A（用户本地数据）

**授权需求**：
```
创建表格 → 需要以**用户身份**创建
  ↓ 需要 OAuth
  用户授权：bitable:app:create
  
写入数据 → 需要写入**用户的表格**
  ↓ 需要 OAuth
  用户授权：bitable:app:write
  
推送日报 → 需要发送消息给**用户**
  ↓ 需要 OAuth
  用户授权：im:message:send_as_user
```

**授权流程**：
1. 用户说："帮我创建 Bot 质量监控数据表"
2. Bot 检测到需要用户授权
3. Bot 推送授权链接（飞书卡片）
4. 用户点击授权
5. 授权成功后，Bot 自动创建表格
6. 后续数据采集和日报推送自动进行

**当前状态**：
- ⏳ 授权流程代码框架已有
- ⏳ 需要配置飞书应用的 OAuth 回调地址
- ⏳ 需要集成 OpenClaw 的 feishu_oauth 工具

#### 场景 B：数据流 B（全局统计）

**授权需求**：**无需用户授权**

```
数据上报 → HTTP POST 到公开 Webhook
  ↓ 无需授权
  
小炸弹写入中央表格 → 以**机器人身份**写入
  ↓ 无需用户授权
  机器人权限已足够
```

**当前状态**：
- ✅ 完全自动化
- ✅ 无需任何授权

---

## 配置管理

### 配置文件层级

```
层级 1：Skill 级别（全局配置）
  ~/.openclaw/workspace/skills/bot-quality-monitor/config.json
  
层级 2：Workspace 级别（任务配置）
  ~/.openclaw/workspace/HEARTBEAT.md
  
层级 3：运行时缓存（临时数据）
  ~/.openclaw/workspace/logs/skill-usage.jsonl
  ~/.openclaw/workspace/logs/processed-webhook-messages.json
```

### config.json 规范

**用途**：存储用户个性化配置

**结构**：
```json
{
  "reportTime": "22:00",
  "timezone": "GMT+8",
  "bitableAppToken": "用户创建表格后自动填写",
  "receiverOpenId": "用户的 open_id，自动获取",
  "tables": {
    "L0_Skill_Usage": "tbllGdVAIIzITahT",
    "L1_消息明细表": "tblmKO3HejbWpUWe",
    "L2_会话汇总表": "tblT0I1nCFhbpvGa"
  }
}
```

**填充时机**：
- reportTime/timezone：用户手动设置（/settime 命令）
- bitableAppToken：创建表格后自动回写
- receiverOpenId：从消息上下文自动获取
- tables：创建表格后自动回写

**当前状态**：
- ✅ 文件结构已定义
- ⏳ 自动回写逻辑待实现（需要 Bot 执行）

### HEARTBEAT.md 规范

**用途**：定义定时任务和自动化流程

**原则**：
- ✅ 任务配置写在 HEARTBEAT.md
- ✅ 硬编码的常量可以直接写（如中央表格 app_token）
- ✅ 用户个性化配置从 config.json 读取

**示例**：
```markdown
## Bot 数据自动采集

**配置读取**：
- 读取 config.json 获取 bitableAppToken 和 tables
- 如果未配置，跳过采集（用户还未创建表格）

**执行逻辑**：
1. 检查 config.json 是否存在
2. 读取 bitableAppToken
3. 如果为空，输出提示："请先创建表格（对 Bot 说：帮我创建表格）"
4. 如果不为空，继续采集...
```

**当前状态**：
- ✅ HEARTBEAT.md 已完善
- ⏳ config.json 读取逻辑待实现

---

## 配置管理流程

### 用户首次安装

```
1. 安装 Skill
   ↓ hooks/install.sh
   创建空的 config.json
   ↓ 配置 HEARTBEAT.md
   追加定时任务

2. 用户说："帮我创建表格"
   ↓ Bot 检测需要授权
   推送授权链接
   ↓ 用户授权
   创建飞书多维表格
   ↓ 自动回写 config.json
   {
     "bitableAppToken": "新生成的 token",
     "tables": {...}
   }

3. 用户说："设置推送时间为 22:00"
   ↓ command-handler.py set_time 22:00
   写入 config.json
   ↓ 确认
   "已设置推送时间为 22:00（GMT+8）"

4. 自动采集开始
   ↓ HEARTBEAT 读取 config.json
   获取 bitableAppToken 和 tables
   ↓ 采集数据
   写入用户的表格
```

### 配置更新

```
用户说："修改推送时间为 20:00"
  ↓ command-handler.py set_time 20:00
  更新 config.json
  ↓ 确认
  "已修改推送时间为 20:00（GMT+8）"
```

### 配置重置

```
用户说："重新创建表格"
  ↓ 删除旧表格
  调用 hooks/delete-bitable.sh
  ↓ 清空 config.json
  rm config.json && 创建空模板
  ↓ 重新创建
  重复首次安装流程
```

---

## 配置与授权的关系

### 数据流 A（用户本地）

```
授权：用户 OAuth
  ↓ 授权成功
配置：自动填充 config.json
  ↓ bitableAppToken + tables
后续操作：读取 config.json
  ↓ 自动采集、自动推送
```

### 数据流 B（全局统计）

```
授权：无需用户授权
  ↓
配置：硬编码在 HEARTBEAT.md
  ↓ 中央表格 app_token
后续操作：直接使用硬编码配置
  ↓ 自动上报、自动入库
```

---

## 常见问题

### Q1: 为什么有些配置在 config.json，有些在 HEARTBEAT.md？

**A: 按用途分层。**

- **config.json**：用户个性化配置（每个用户不同）
  - reportTime（推送时间）
  - bitableAppToken（用户的表格）
  
- **HEARTBEAT.md**：全局任务配置（所有用户相同）
  - 中央表格 app_token（固定值）
  - 定时任务触发时间（固定规则）

### Q2: 用户授权后，Bot 如何自动填充 config.json？

**A: Bot 执行回写逻辑。**

```python
# 创建表格成功后
app_token = create_result["app_token"]

# 读取 config.json
with open("config.json", "r") as f:
    config = json.load(f)

# 更新配置
config["bitableAppToken"] = app_token
config["tables"] = {...}

# 写回 config.json
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
```

**当前状态**：逻辑已设计，待 Bot 集成执行。

### Q3: 如果用户删除了表格，会发生什么？

**A: 优雅降级。**

```
HEARTBEAT 采集任务
  ↓ 读取 config.json
  bitableAppToken = "xxx"
  ↓ 调用飞书 API
  写入数据
  ↓ ❌ 返回 404（表格不存在）
  记录错误日志
  ↓ 静默跳过
  等待用户重新创建表格
```

**未来优化**：
- 检测到表格删除
- 主动通知用户："您的监控表格已删除，是否重新创建？"

---

## 授权最佳实践

### 对用户透明

1. **授权前告知**
   ```
   Bot："创建监控表格需要授权以下权限：
   - 创建多维表格
   - 写入表格数据
   - 发送消息通知
   
   点击下方链接授权 👇"
   ```

2. **授权后确认**
   ```
   Bot："✓ 授权成功！
   正在创建监控表格...
   ✓ 表格创建完成
   ✓ 已生成 7 天测试数据
   ✓ Demo 日报已推送
   
   您可以随时查看表格：
   https://www.feishu.cn/base/xxx"
   ```

3. **失败时提示**
   ```
   Bot："⚠ 授权失败
   可能原因：
   - 授权链接已过期
   - 网络连接问题
   
   请重试：[重新授权]"
   ```

### 最小化权限

- 只申请必要的权限
- 不申请"读取所有消息"等过度权限
- 授权范围限定在 Bot 相关功能

### 可撤销

- 用户可随时在飞书设置中撤销授权
- 撤销后，Bot 停止数据采集
- 不影响已采集的数据（数据归用户所有）

---

## 开发者指南

### 如何添加新配置项

1. **更新 config.json 模板**
   ```json
   {
     "reportTime": "22:00",
     "newConfig": "默认值"  // 新增
   }
   ```

2. **更新 command-handler.py**
   ```python
   def set_new_config(value):
       config = load_config()
       config["newConfig"] = value
       save_config(config)
   ```

3. **更新 SKILL.md 触发规则**
   ```markdown
   /setnewconfig <value> - 设置 newConfig
   ```

4. **更新文档**
   - README.md：用户操作说明
   - USERS_GUIDE.md：详细指南

### 如何添加新的授权权限

1. **在飞书开放平台添加权限**
   - 应用管理 → 权限管理
   - 添加需要的权限
   - 提交审核

2. **更新授权流程代码**
   ```python
   REQUIRED_SCOPES = [
       "bitable:app:create",
       "bitable:app:write",
       "new:scope"  # 新增
   ]
   ```

3. **更新文档**
   - AUTHORIZATION.md：说明新权限的用途
   - FAQ.md：解释为什么需要这个权限
