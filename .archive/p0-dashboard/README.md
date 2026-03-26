# P0 Dashboard - 用户个人健康度看板

## 功能说明
- **数据范围**: 最近 7 天
- **生成时机**: 每日 22:00
- **推送对象**: 每个用户

## 核心模块（6个）
1. 综合健康度仪表盘（Gauge Chart）
2. 三维度雷达图（Radar Chart）
3. 7 天趋势折线图（Line Chart）
4. 场景健康度热力图（Heatmap）
5. 三类智能信号卡片（Cards）
6. 失败案例 Top 10 + 诊断建议（Table）

## 使用方法

### 1. 手动测试生成
```bash
python3 generate-p0-dashboard.py
```

### 2. 集成真实数据
当前脚本使用模拟数据，集成真实数据需要：

1. 在 OpenClaw 环境中调用 `feishu_bitable_app_table_record` 工具
2. 替换 `fetch_user_data()` 函数中的 TODO 部分
3. 从飞书多维表格读取：
   - L3_每日指标汇总表（最近 7 天）
   - L3_Signal_Alerts 表（三类信号）
   - L2_会话汇总表（失败案例）

### 3. 上传到飞书云盘
生成的 HTML 文件需要上传到飞书云盘并获取分享链接：

```python
# 在 OpenClaw 环境中调用
feishu_drive_file(
    action="upload",
    file_path=output_path,
    name=f"P0-个人健康度看板-{date}.html"
)
```

### 4. 推送日报
在日报飞书卡片中添加"查看详细报告"按钮，点击跳转到 HTML Dashboard。

## 定时任务
已配置 Cron：
```bash
# 每日 22:00 生成
0 22 * * * python3 /path/to/generate-p0-dashboard.py
```

## 输出位置
- **本地文件**: `~/.openclaw/workspace/reports/p0-dashboard-YYYYMMDD.html`
- **日志文件**: `~/.openclaw/workspace/logs/p0-dashboard.log`

## 技术栈
- Python 3.11+
- Plotly 5.x（交互式图表）
- Jinja2 3.x（HTML 模板）
- Bootstrap 5.1.3（CSS 框架）

## 下一步优化
1. [ ] 集成真实数据（替换模拟数据）
2. [ ] 添加用户筛选（支持多用户）
3. [ ] 移动端适配
4. [ ] 添加日报历史查看功能
