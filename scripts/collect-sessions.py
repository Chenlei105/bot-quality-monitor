#!/usr/bin/env python3
"""
Bot 会话数据自动采集脚本 - Session Hook 版本

功能:
- 每次 Heartbeat 自动触发
- 调用 sessions_list 获取最近活跃的会话
- 过滤出未采集的新会话
- 提取关键指标并写入飞书多维表格

用法:
    在 HEARTBEAT.md 中配置自动运行
    或手动测试: python3 collect-sessions.py
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 配置文件路径
CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/bot-quality-monitor/config.json"
COLLECTED_SESSIONS_PATH = Path.home() / ".openclaw/workspace/logs/collected-sessions.json"
ERROR_LOG_PATH = Path.home() / ".openclaw/workspace/logs/bot-analytics-error.log"

# 确保日志目录存在
COLLECTED_SESSIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
ERROR_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    
    # 错误日志写入文件
    if level == "ERROR":
        with open(ERROR_LOG_PATH, "a") as f:
            f.write(log_message + "\n")

def load_config():
    """加载配置文件（从用户自己的 config.json）"""
    try:
        if not CONFIG_PATH.exists():
            log("配置文件不存在,跳过采集（用户还未安装）", "WARN")
            return None
        
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        
        # 验证必要字段
        if not config.get('bitableAppToken'):
            log("配置文件缺少 bitableAppToken", "ERROR")
            return None
        
        if not config.get('tables', {}).get('L2_会话汇总表'):
            log("配置文件缺少 L2_会话汇总表 ID", "ERROR")
            return None
        
        log(f"✓ 配置加载成功: app_token={config['bitableAppToken'][:10]}...")
        return config
    except Exception as e:
        log(f"加载配置文件失败: {e}", "ERROR")
        return None

def get_user_table_ids(config):
    """从配置文件获取用户自己的表格 ID"""
    try:
        app_token = config['bitableAppToken']
        table_id = config['tables']['L2_会话汇总表']
        
        return {
            'app_token': app_token,
            'table_id': table_id
        }
    except Exception as e:
        log(f"获取表格 ID 失败: {e}", "ERROR")
        return None

# ====== 旧代码（硬编码中央表格 ID）已删除 ======
# CENTRAL_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"  # 删除
# CENTRAL_TABLE_ID = "tblT0I1nCFhbpvGa"  # 删除
        
        # 验证必要字段
        if "bitableAppToken" not in config or "tables" not in config:
            log("配置文件缺少必要字段,跳过采集", "WARN")
            return None
        
        return config
    except Exception as e:
        log(f"加载配置失败: {e}", "ERROR")
        return None

def load_collected_sessions():
    """加载已采集会话记录"""
    try:
        if not COLLECTED_SESSIONS_PATH.exists():
            return set()
        
        with open(COLLECTED_SESSIONS_PATH, "r") as f:
            data = json.load(f)
            return set(data.get("collected", []))
    except Exception as e:
        log(f"加载已采集记录失败: {e}", "WARN")
        return set()

def save_collected_sessions(sessions):
    """保存已采集会话记录"""
    try:
        with open(COLLECTED_SESSIONS_PATH, "w") as f:
            json.dump({
                "collected": list(sessions),
                "last_update": int(datetime.now().timestamp() * 1000)
            }, f, indent=2)
    except Exception as e:
        log(f"保存已采集记录失败: {e}", "ERROR")

def identify_scene_type(messages):
    """识别场景类型"""
    user_text = " ".join([
        m.get('content', '') 
        for m in messages 
        if m.get('role') == 'user'
    ]).lower()
    
    scene_keywords = {
        "数据分析": ["数据", "统计", "分析", "图表", "dashboard"],
        "文档处理": ["文档", "docx", "pdf", "编辑", "写", "生成文档"],
        "健康诊断": ["健康", "诊断", "检查", "问题"],
        "搜索查询": ["搜索", "查询", "找", "search"],
        "代码调试": ["代码", "bug", "调试", "运行", "脚本"],
        "闲聊": ["聊天", "你好", "怎么样", "谢谢"]
    }
    
    for scene, keywords in scene_keywords.items():
        if any(keyword in user_text for keyword in keywords):
            return scene
    
    return "其他"

def extract_session_metrics(session_key, history):
    """从会话历史中提取指标"""
    try:
        messages = history.get('messages', [])
        
        if not messages:
            return None
        
        # 提取各类消息
        user_messages = [m for m in messages if m.get('role') == 'user']
        assistant_messages = [m for m in messages if m.get('role') == 'assistant']
        tool_calls = [m for m in messages if m.get('role') == 'tool']
        
        # 识别纠错信号
        correction_count = sum(1 for m in user_messages if any(
            keyword in m.get('content', '').lower() 
            for keyword in ['错了', '不对', '重新', '修改', '更正']
        ))
        
        # 识别场景类型
        scene_type = identify_scene_type(messages)
        
        # 判断完成状态
        last_assistant = assistant_messages[-1] if assistant_messages else {}
        completion_status = "completed"
        if any(word in last_assistant.get('content', '') for word in ["抱歉", "无法"]):
            completion_status = "failed"
        
        # 提取时间戳
        start_time = messages[0].get('timestamp') if messages else None
        end_time = messages[-1].get('timestamp') if messages else None
        
        # 提取模型信息
        model_name = history.get('model', 'unknown')
        
        # 提取用户信息
        user_owner_id = history.get('metadata', {}).get('sender_id', 'unknown')
        
        return {
            "session_id": session_key,
            "用户所有者ID": user_owner_id,
            "bot_id": "cli_a922b6c0b8b89bd1",
            "bot_name": "小炸弹",
            "scene_type": scene_type,
            "turn_count": len(user_messages),
            "correction_count": correction_count,
            "api_calls": len(tool_calls),
            "completion_status": completion_status,
            "model_used": model_name,
            "session_start": start_time,  # 修复字段名
            "session_end": end_time,      # 修复字段名
            "total_tokens": sum(m.get('usage', {}).get('total_tokens', 0) for m in assistant_messages),
            "first_resolve": correction_count == 0,
            "satisfaction_signal": "positive" if completion_status == "completed" else "negative"
        }
    except Exception as e:
        log(f"提取会话指标失败 ({session_key}): {e}", "ERROR")
        return None

def main():
    """主流程"""
    log("=" * 60)
    log("Bot 会话数据自动采集任务开始")
    log("=" * 60)
    
    # 1. 加载配置（从用户自己的 config.json）
    config = load_config()
    if not config:
        log("配置未就绪,跳过本次采集")
        return
    
    table_info = get_user_table_ids(config)
    if not table_info:
        log("表格 ID 获取失败,跳过采集", "ERROR")
        return
    
    app_token = table_info['app_token']
    table_id = table_info['table_id']
    
    log(f"✓ 使用用户表格: {app_token[:10]}.../{table_id}")
    
    # 2. 加载已采集会话
    collected = load_collected_sessions()
    log(f"已采集会话数: {len(collected)}")
    
    # 3. 获取最近活跃的会话
    # 这里输出 OpenClaw 指令,由 Heartbeat 执行
    print(json.dumps({
        "action": "collect_sessions",
        "steps": [
            {
                "step": 1,
                "tool": "sessions_list",
                "params": {
                    "activeMinutes": 60,
                    "limit": 50
                },
                "save_output": "sessions"
            },
            {
                "step": 2,
                "description": "过滤未采集的会话",
                "collected_sessions": list(collected),
                "python_logic": "filter_new_sessions"
            },
            {
                "step": 3,
                "tool": "sessions_history",
                "params": {
                    "sessionKey": "${new_session_key}",
                    "limit": 100,
                    "includeTools": True
                },
                "save_output": "history",
                "foreach": "new_sessions"
            },
            {
                "step": 4,
                "description": "提取会话指标",
                "python_logic": "extract_session_metrics"
            },
            {
                "step": 5,
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": app_token,
                    "table_id": table_id,
                    "records": "${extracted_records}"
                }
            },
            {
                "step": 6,
                "description": "保存已采集会话",
                "python_logic": "save_collected_sessions"
            }
        ]
    }, indent=2, ensure_ascii=False))
    
    log("=" * 60)
    log("Bot 会话数据自动采集任务结束")
    log("=" * 60)

if __name__ == "__main__":
    main()
