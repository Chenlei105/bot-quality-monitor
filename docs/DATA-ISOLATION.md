# 数据隔离与隐私保护说明

## 架构设计

Bot Quality Monitor 采用**双轨数据流**架构，天然实现数据隔离：

### 数据流 A：用户本地数据（完全隔离）

```
用户 A（企业 A）
  ↓ 安装 Skill 到自己的 Bot（如"小旋风"）
  用户 A 说："创建表格"
  ↓ 小旋风调用飞书 API
  飞书多维表格 X（在企业 A 的飞书空间）
  ↓ 小旋风采集数据
  用户 A 与小旋风的对话记录
  ↓ 小旋风写入
  表格 X（只有用户 A 和企业 A 成员可见）

用户 B（企业 B）
  ↓ 安装 Skill 到自己的 Bot（如"小助手"）
  用户 B 说："创建表格"
  ↓ 小助手调用飞书 API
  飞书多维表格 Y（在企业 B 的飞书空间）
  ↓ 小助手采集数据
  用户 B 与小助手的对话记录
  ↓ 小助手写入
  表格 Y（只有用户 B 和企业 B 成员可见）
```

**隔离机制**：
- ✅ 每个用户的 Bot 创建**独立的多维表格**
- ✅ 表格在**用户自己的飞书企业空间**
- ✅ 飞书权限系统保证**企业 A 无法访问企业 B 的表格**
- ✅ 数据包含**真实对话内容**（四维指标）

**隐私保护**：
- 用户 A 的 Bot 只能访问企业 A 的表格
- 用户 B 的 Bot 只能访问企业 B 的表格
- 跨企业完全隔离（飞书企业隔离机制）
- 只有创建者本人和同企业成员可以查看数据

---

### 数据流 B：全局匿名统计（中央汇总）

```
用户 A 的 Bot（企业 A）
  ↓ 每小时自动上报
  user_id: anon_abc123（匿名）
  event: install / run / uninstall
  ↓ HTTP POST 到 Webhook
  飞书群消息

用户 B 的 Bot（企业 B）
  ↓ 每小时自动上报
  user_id: anon_def456（匿名）
  event: install / run / uninstall
  ↓ HTTP POST 到 Webhook
  飞书群消息

小炸弹（项目维护者的 Bot）
  ↓ 每 10 分钟检查
  读取 Webhook 消息
  ↓ 解析 JSON
  提取所有事件
  ↓ 批量写入
  中央表格（Xw4Tb5C8KagMiQswkdacNfVPn8e）
  ↓ 用途
  统计分析：安装量、活跃度、成功率
```

**匿名机制**：
- ✅ **匿名 ID**（sha256 hash，不可逆）
- ✅ **不采集隐私信息**：
  - ❌ 不采集真实用户名
  - ❌ 不采集飞书 ID
  - ❌ 不采集对话内容
  - ❌ 不采集 IP 地址
- ✅ **只采集统计信息**：
  - ✅ 事件类型（install / run / uninstall）
  - ✅ 时间戳
  - ✅ 系统信息（os / platform / python 版本）

**用户可关闭**：
```bash
export SKILL_TRACKING=off
```

---

## 权限模型

### 飞书多维表格权限特性

| 特性 | 说明 |
|------|------|
| 权限粒度 | **表级别**（不支持行级权限） |
| 创建者权限 | 表格创建者自动成为 Owner |
| 共享机制 | 可通过"添加成员"共享给其他人 |
| 跨企业访问 | 不支持（企业隔离） |

### 数据流 A 权限

```
用户创建表格 → 用户成为 Owner → 数据写入用户表格
```

**访问控制**：
- 创建者：完全控制（读/写/删除）
- 其他用户：**默认无权限**（除非创建者主动共享）

### 数据流 B 权限

```
所有用户 → Webhook 上报 → 小炸弹写入 → 中央表格
```

**访问控制**：
- 大少爷：完全控制（Owner）
- 其他用户：**无权限访问中央表格**

---

## 常见问题

### Q1: 用户 A 能看到用户 B 的数据吗？

**A: 完全不能。**

- 数据流 A：每个用户的数据在**独立表格**中，飞书权限系统保证隔离
- 数据流 B：所有用户数据都是**匿名的**，且只有大少爷有权限访问

### Q2: 中央表格会泄露用户隐私吗？

**A: 不会。**

中央表格只有：
- 匿名 ID（anon_xxxxxxxx）
- 事件类型（install / run / uninstall）
- 时间戳
- 系统信息（非敏感）

**不包含**：
- 真实用户名
- 飞书 ID
- 对话内容
- 任何可识别身份的信息

### Q3: 为什么需要中央表格？

**A: 用于统计分析和产品改进。**

典型用途：
- 有多少人安装了 Skill？
- 哪些场景使用最多？
- 成功率如何？
- 哪些地方需要优化？

这些统计数据**不涉及用户隐私**，是匿名的聚合数据。

### Q4: 我不想上报匿名数据，可以关闭吗？

**A: 可以。**

```bash
export SKILL_TRACKING=off
```

设置后，你的机器人将不会上报任何数据到中央表格。

---

## 技术实现

### 匿名 ID 生成算法

```python
import hashlib

user = os.environ.get("USER", "unknown")
home = os.environ.get("HOME", "unknown")
hostname = os.popen("hostname").read().strip()

unique_string = f"{user}:{home}:{hostname}"
hash_id = hashlib.sha256(unique_string.encode()).hexdigest()[:16]

anonymous_id = f"anon_{hash_id}"
```

**特性**：
- ✅ 基于机器特征生成
- ✅ 同一台机器始终生成同一 ID
- ✅ 不同机器生成不同 ID
- ✅ **不可逆**（无法从 anon_xxx 推导出真实信息）

### 数据上报内容

```json
{
  "event_type": "install",
  "skill_name": "bot-quality-monitor",
  "skill_version": "3.0.0",
  "user_id": "anon_944721ff47947e57",
  "timestamp": 1774509021976,
  "source": "github",
  "extra": "{\"os\": \"posix\", \"platform\": \"linux\", \"python\": \"3.12\"}"
}
```

**不包含的信息**：
- ❌ 用户名
- ❌ 飞书 ID
- ❌ 对话内容
- ❌ 文件路径
- ❌ IP 地址
- ❌ 任何敏感信息

---

## 合规声明

本项目遵循以下隐私原则：

1. **最小化采集**：只采集必要的统计信息
2. **匿名化处理**：所有用户数据匿名化
3. **用户可控**：用户可随时关闭数据上报
4. **透明公开**：数据采集机制完全开源
5. **安全存储**：数据存储在飞书企业版（符合企业安全标准）

如有隐私顾虑，请联系项目维护者。

---

## 审计日志

所有数据上报操作都有本地日志：

```bash
# 本地上报记录
~/.openclaw/workspace/logs/skill-usage.jsonl

# 已同步记录（带时间戳）
~/.openclaw/workspace/logs/skill-usage.jsonl.uploaded.*

# 中央表格处理记录（小炸弹）
~/.openclaw/workspace/logs/processed-webhook-messages.json
```

用户可随时审查本地日志，确认上报的内容。
