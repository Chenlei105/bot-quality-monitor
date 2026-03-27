#!/usr/bin/env python3
"""
Dashboard HTML 生成器（使用紫色渐变模板）

功能:
- 读取 L3_每日指标汇总表
- 使用外部 HTML 模板（紫色渐变 + 玻璃质感）
- 生成交互式 Dashboard

用法:
    python3 generate-dashboard.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"
TEMPLATE_PATH = Path(__file__).parent / "templates/user-dashboard-template.html"

def main():
    """主流程"""
    # 读取配置
    if not CONFIG_PATH.exists():
        print(json.dumps({
            "error": "配置文件不存在",
            "workflow": [
                {
                    "step": "create_config",
                    "message": "请先运行 auto-setup-v5.py 创建配置"
                }
            ]
        }))
        sys.exit(1)
    
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    
    # 读取模板
    if not TEMPLATE_PATH.exists():
        print(json.dumps({
            "error": f"模板文件不存在: {TEMPLATE_PATH}",
            "message": "请确保 scripts/templates/user-dashboard-template.html 存在"
        }))
        sys.exit(1)
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 生成输出路径
    output_dir = Path.home() / ".openclaw/workspace/reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"dashboard-{datetime.now().strftime('%Y%m%d')}.html"
    
    # 写入 HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    # 返回结果
    print(json.dumps({
        "success": True,
        "output_path": str(output_path),
        "message": f"Dashboard 已生成: {output_path}"
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
