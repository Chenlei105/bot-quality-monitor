#!/usr/bin/env python3
"""
Bot Quality Monitor - 命令处理器
处理用户的各种命令请求
用法（由Bot调用）:
python3 scripts/command-handler.py <command> [args]
例如:
python3 scripts/command-handler.py create_bitable <user_open_id>
python3 scripts/command-handler.py health
python3 scripts/command-handler.py dashboard
python3 scripts/command-handler.py diagnose 文档处理
python3 scripts/command-handler.py set_time 20:00
python3 scripts/command-handler.py set_timezone GMT+8
python3 scripts/command-handler.py demo
python3 scripts/command-handler.py help
"""

import sys
import json
import os
from datetime import datetime

# 技能目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "reportTime": "22:00",
        "timezone": "GMT+8"
    }

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def cmd_create_bitable(user_open_id):
    """创建多维表格"""
    print("🚀 正在创建 Bot Quality Monitor 多维表格...")
    print("📊 将创建 12 张数据表...")
    
    # 调用 auto-create-bitable.py 获取表结构
    import subprocess
    result = subprocess.run(
        [sys.executable, os.path.join(SKILL_DIR, "scripts/auto-create-bitable.py"), user_open_id],
        capture_output=True, text=True
    )
    
    # 解析返回的 JSON
    try:
        tables_def = json.loads(result.stdout)
        print("✅ 表结构已生成")
        print(f"📋 将创建 {len(tables_def.get('tables', []))} 张数据表")
        
        # 返回创建指令，让 Bot 调用飞书 API 创建
        return json.dumps({
            "action": "create_bitable",
            "name": "Bot Quality Monitor",
            "tables": tables_def.get('tables', []),
            "user_open_id": user_open_id
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ 生成表结构失败: {e}")
        return json.dumps({"error": str(e)})

def cmd_demo():
    """生成 Demo 数据"""
    print("📈 正在生成测试数据...")
    
    # 调用 generate-demo-data.py
    import subprocess
    result = subprocess.run(
        [sys.executable, os.path.join(SKILL_DIR, "scripts/generate-demo-data.py")],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print("✅ 测试数据已生成")
        # 返回生成 Demo 日报的指令
        return json.dumps({
            "action": "generate_demo_report",
            "message": "测试数据已生成，正在生成 Demo 日报..."
        }, ensure_ascii=False)
    else:
        print(f"❌ 生成测试数据失败: {result.stderr}")
        return json.dumps({"error": result.stderr})

def cmd_health():
    """查看健康度"""
    config = load_config()
    
    # 返回读取健康度数据的指令
    return json.dumps({
        "action": "read_health_data",
        "config": config
    }, ensure_ascii=False)

def cmd_dashboard():
    """获取 Dashboard"""
    # 返回生成 Dashboard 的指令
    return json.dumps({
        "action": "generate_dashboard"
    }, ensure_ascii=False)

def cmd_diagnose(scene):
    """诊断场景"""
    # 返回诊断指令
    return json.dumps({
        "action": "diagnose_scene",
        "scene": scene
    }, ensure_ascii=False)

def cmd_set_time(time_str):
    """设置推送时间"""
    config = load_config()
    
    # 验证时间格式
    try:
        hour, minute = time_str.split(':')
        hour = int(hour)
        minute = int(minute)
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            config['reportTime'] = time_str
            save_config(config)
            return json.dumps({
                "action": "set_time",
                "success": True,
                "message": f"✅ 推送时间已设置为: {time_str}",
                "time": time_str
            }, ensure_ascii=False)
    except:
        pass
    
    return json.dumps({
        "action": "set_time",
        "success": False,
        "message": "❌ 时间格式错误，请使用 HH:MM 格式，例如：/settime 20:00"
    }, ensure_ascii=False)

def cmd_set_timezone(tz):
    """设置时区"""
    config = load_config()
    
    # 简单的时区验证
    valid_tz = ["GMT+8", "GMT", "UTC", "PST", "EST", "JST", "CST"]
    if tz.upper() in [v.upper() for v in valid_tz]:
        config['timezone'] = tz
        save_config(config)
        return json.dumps({
            "action": "set_timezone",
            "success": True,
            "message": f"✅ 时区已设置为: {tz}",
            "timezone": tz
        }, ensure_ascii=False)
    
    return json.dumps({
        "action": "set_timezone",
        "success": False,
        "message": f"❌ 不支持的时区，支持: {', '.join(valid_tz)}"
    }, ensure_ascii=False)

def cmd_help():
    """帮助信息"""
    help_text = """
📖 Bot Quality Monitor 帮助

━━━━━━━━━━ 命令列表 ━━━━━━━━━━

/health [scene]
   查看整体或特定场景的健康度
   示例: /health 或 /health 文档处理

/dashboard
   获取 HTML Dashboard 链接
   用浏览器打开可查看交互式图表

/diagnose <场景>
   诊断特定场景的问题
   示例: /diagnose 文档处理

/settime <时间>
   设置日报推送时间
   示例: /settime 20:00 或 /settime 9:00

/settz <时区>
   设置时区
   示例: /settz GMT+8 或 /settz UTC

/createdemo
   重新生成测试数据并推送 Demo 日报
   示例: /createdemo

/help
   显示帮助信息

━━━━━━━━━━ 了解更多 ━━━━━━━━━━

GitHub: https://github.com/Chenlei105/bot-quality-monitor
"""
    return json.dumps({
        "action": "help",
        "message": help_text.strip()
    }, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: command-handler.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create_bitable" and len(sys.argv) >= 3:
        result = cmd_create_bitable(sys.argv[2])
    elif command == "demo":
        result = cmd_demo()
    elif command == "health":
        result = cmd_health()
    elif command == "dashboard":
        result = cmd_dashboard()
    elif command == "diagnose" and len(sys.argv) >= 3:
        result = cmd_diagnose(sys.argv[2])
    elif command == "set_time" and len(sys.argv) >= 3:
        result = cmd_set_time(sys.argv[2])
    elif command == "set_timezone" and len(sys.argv) >= 3:
        result = cmd_set_timezone(sys.argv[2])
    elif command == "help":
        result = cmd_help()
    else:
        result = json.dumps({
            "error": f"Unknown command: {command}"
        })
    
    print(result)

if __name__ == "__main__":
    main()