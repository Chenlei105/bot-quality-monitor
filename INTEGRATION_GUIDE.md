# Bot Quality Monitor - 真实数据集成指南

## 当前状态

✅ **已完成**:
1. P0/P1/P2 三层 Dashboard 生成脚本
2. 定时任务配置（Cron）
3. 数据归档脚本
4. 飞书多维表格结构（12 张表已创建）

⚠️ **待集成**:
1. Dashboard 脚本中的模拟数据替换为真实数据
2. 数据采集功能（用户对话自动上报）
3. 授权引导流程（OAuth）

---

## 集成步骤

### 第一步：替换 P0 Dashboard 真实数据

**文件**: `p0-dashboard/generate-p0-dashboard.py`

**需要修改的函数**: `fetch_user_data(user_owner_id)`

**原代码**（第 21-90 行）:
```python
def fetch_user_data(user_owner_id):
    """
    获取用户最近 7 天的数据
    """
    # TODO: 这里需要调用 feishu_bitable_app_table_record 工具
    # 暂时返回模拟数据用于测试
    
    # 模拟数据
    return {
        "latest_score": {...},
        "yesterday_score": {...},
        ...
    }
```

**替换为真实数据**:
```python
def fetch_user_data(user_owner_id):
    """
    获取用户最近 7 天的数据
    """
    from openclaw_tools import feishu_bitable_app_table_record
    
    # 计算日期范围
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 读取 L3_每日指标汇总（最近 7 天）
    l3_data = feishu_bitable_app_table_record(
        action="list",
        app_token="Xw4Tb5C8KagMiQswkdacNfVPn8e",
        table_id="tbldgJxU6QUSjnf6",
        filter={
            "conjunction": "and",
            "conditions": [
                {"field_name": "user_owner_id", "operator": "is", "value": [user_owner_id]},
                {"field_name": "date", "operator": "isGreaterEqual", "value": [seven_days_ago]},
                {"field_name": "date", "operator": "isLessEqual", "value": [today]}
            ]
        },
        sort=[{"field_name": "date", "desc": False}]
    )
    
    # 2. 读取三类智能信号
    signals_data = feishu_bitable_app_table_record(
        action="list",
        app_token="Xw4Tb5C8KagMiQswkdacNfVPn8e",
        table_id="tblVDILmtu1oYRTE",
        filter={
            "conjunction": "and",
            "conditions": [
                {"field_name": "user_owner_id", "operator": "is", "value": [user_owner_id]},
                {"field_name": "date", "operator": "is", "value": [today]}
            ]
        }
    )
    
    # 3. 读取失败案例
    failures_data = feishu_bitable_app_table_record(
        action="list",
        app_token="Xw4Tb5C8KagMiQswkdacNfVPn8e",
        table_id="tblT0I1nCFhbpvGa",
        filter={
            "conjunction": "and",
            "conditions": [
                {"field_name": "user_owner_id", "operator": "is", "value": [user_owner_id]},
                {"field_name": "completion_status", "operator": "is", "value": ["failed"]},
                {"field_name": "date", "operator": "isGreaterEqual", "value": [seven_days_ago]}
            ]
        },
        sort=[{"field_name": "failure_count", "desc": True}],
        page_size=10
    )
    
    # 4. 数据转换
    records = l3_data.get('records', [])
    if not records:
        raise ValueError(f"用户 {user_owner_id} 最近 7 天无数据")
    
    latest_record = records[-1]['fields']
    yesterday_record = records[-2]['fields'] if len(records) >= 2 else latest_record
    
    # 构造返回数据
    return {
        "latest_score": {
            "health_score": latest_record['health_score'],
            "quality_score": latest_record['quality_score'],
            "efficiency_score": latest_record['efficiency_score'],
            "resource_score": latest_record['resource_score'],
            "health_rating": latest_record['health_rating']
        },
        "yesterday_score": {
            "health_score": yesterday_record['health_score']
        },
        "trend_data": {
            "dates": [r['fields']['date'] for r in records],
            "correction_rates": [r['fields']['correction_rate'] * 100 for r in records],
            "first_resolve_rates": [r['fields']['first_resolve_rate'] * 100 for r in records],
            "completion_rates": [r['fields']['completion_rate'] * 100 for r in records]
        },
        "scene_heatmap": extract_scene_heatmap(records),
        "signals": parse_signals(signals_data),
        "failures": parse_failures(failures_data)
    }
```

---

### 第二步：替换 P1 Dashboard 真实数据

**文件**: `p1-dashboard/generate-p1-dashboard.py`

**需要修改的函数**: `fetch_global_data()`

类似 P0，从 L3_每日指标汇总、L3_Skill_ROI 等表读取最近 30 天的全局数据。

---

### 第三步：替换 P2 Dashboard 真实数据

**文件**: `p2-dashboard/generate-p2-dashboard.py`

**需要修改的函数**: `fetch_archive_data(report_type)`

根据 `report_type`（monthly/quarterly/yearly）从对应的汇总表读取数据。

---

### 第四步：替换数据归档脚本真实调用

**文件**: `archive-scripts/archive-old-data.py`

**需要修改的函数**:
- `archive_l2_sessions()`
- `archive_l1_messages()`
- `generate_monthly_summary()`
- `generate_quarterly_summary()`
- `generate_yearly_summary()`

取消注释 TODO 部分，启用真实的 `feishu_bitable_app_table_record` 调用。

---

## 在 OpenClaw 环境中调用

由于 Dashboard 生成脚本需要调用 OpenClaw 工具（`feishu_bitable_app_table_record`），有两种集成方式：

### 方案 A：直接在 Skill 中调用（推荐）

将生成脚本封装为 Skill，在 Skill 上下文中可以直接调用 OpenClaw 工具。

**步骤**:
1. 修改 `generate-p0-dashboard.py`，添加：
```python
from openclaw_tools import feishu_bitable_app_table_record
```

2. 在 OpenClaw 中触发执行：
```bash
openclaw skill run bot-quality-monitor --task="生成 P0 Dashboard"
```

### 方案 B：通过 API 调用（备选）

如果无法在 Skill 中调用，可以通过 OpenClaw API 间接调用飞书接口。

---

## 测试验证

### 1. 验证数据读取
```python
# 测试读取 L3 表数据
python3 -c "
from openclaw_tools import feishu_bitable_app_table_record

result = feishu_bitable_app_table_record(
    action='list',
    app_token='Xw4Tb5C8KagMiQswkdacNfVPn8e',
    table_id='tbldgJxU6QUSjnf6',
    page_size=10
)

print(f'记录数: {len(result[\"records\"])}')
"
```

### 2. 验证 Dashboard 生成
```bash
# 集成真实数据后重新生成
python3 p0-dashboard/generate-p0-dashboard.py
```

### 3. 验证定时任务
```bash
# 手动触发 cron 任务（不等到定时时间）
/usr/bin/python3 /root/.openclaw/workspace/skills/bot-quality-monitor/p0-dashboard/generate-p0-dashboard.py
```

---

## 常见问题

### Q1: 模拟数据与真实数据字段不匹配怎么办？

**A**: 检查飞书多维表格的字段类型，确保与代码中的字段名一致。使用 `feishu_bitable_app_table_field` 工具查看字段列表。

### Q2: 用户没有数据怎么办？

**A**: 脚本应该捕获异常并返回友好提示，建议添加：
```python
if not records:
    return generate_empty_dashboard("暂无数据，请先使用 Bot 一段时间")
```

### Q3: Dashboard 图表不显示怎么办？

**A**: 检查：
1. Plotly CDN 是否可访问（`https://cdn.plot.ly/plotly-2.18.0.min.js`）
2. 浏览器控制台是否有 JavaScript 错误
3. 数据格式是否正确（数组长度一致）

---

## 下一步计划

1. **优先级 P0**: 集成 P0 Dashboard 真实数据（用户最关心）
2. **优先级 P1**: 集成 P1 Dashboard 真实数据（管理员需要）
3. **优先级 P2**: 集成 P2 Dashboard 真实数据（长期归档）
4. **优先级 P3**: 启用数据归档任务（防止数据膨胀）

---

## 联系支持

如果在集成过程中遇到问题，请查看日志文件：
- P0: `~/.openclaw/workspace/logs/p0-dashboard.log`
- P1: `~/.openclaw/workspace/logs/p1-dashboard.log`
- P2: `~/.openclaw/workspace/logs/p2-{monthly|quarterly|yearly}.log`
- 归档: `~/.openclaw/workspace/logs/data-archive.log`
