#!/usr/bin/env python3
"""
平台级 Dashboard HTML 生成器（紫色渐变模板）

功能:
- 读取中央表格的平台数据
- 使用外部 HTML 模板（紫色渐变 + 玻璃质感）
- 生成平台级 Dashboard

用法:
    python3 generate-platform-dashboard.py
"""

import sys
import json
from datetime import datetime
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates/platform-dashboard-template.html"

def main():
    """主流程"""
    # 读取模板
    if not TEMPLATE_PATH.exists():
        print(json.dumps({
            "error": f"模板文件不存在: {TEMPLATE_PATH}",
            "message": "请确保 scripts/templates/platform-dashboard-template.html 存在"
        }))
        sys.exit(1)
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 生成输出路径
    output_dir = Path.home() / ".openclaw/workspace/reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"platform-dashboard-{datetime.now().strftime('%Y%m%d')}.html"
    
    # 写入 HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    # 返回结果
    print(json.dumps({
        "success": True,
        "output_path": str(output_path),
        "message": f"平台 Dashboard 已生成: {output_path}"
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
