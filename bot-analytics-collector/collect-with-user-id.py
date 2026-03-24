#!/usr/bin/env python3
"""
Bot 数据采集脚本 v3.0
支持多租户 - 自动记录 user_owner_id
"""

import sys
import json
from datetime import datetime

def collect_session_data(session_data, user_owner_id):
    """
    采集会话数据并写入 L2 表
    
    Args:
        session_data: 会话数据字典
        user_owner_id: 用户所有者 ID (open_id)
    """
    
    # 确保 session_data 包含 user_owner_id
    session_data['用户所有者ID'] = user_owner_id
    
    print(f"✅ 采集会话数据 (用户: {user_owner_id})")
    print(f"   Bot: {session_data.get('bot_name')}")
    print(f"   场景: {session_data.get('scene_type')}")
    print(f"   状态: {session_data.get('completion_status')}")
    
    # TODO: 调用 feishu_bitable_app_table_record 写入 L2 表
    # 确保包含 user_owner_id 字段
    
    return True

def get_current_user_id():
    """
    获取当前用户的 open_id
    
    从环境变量或配置文件中读取
    """
    # 方法 1: 从消息上下文获取
    # sender_id = os.getenv('OPENCLAW_SENDER_ID')
    
    # 方法 2: 从配置文件读取
    try:
        with open('~/.openclaw/workspace/skills/bot-quality-monitor/config.json') as f:
            config = json.load(f)
            return config.get('user_owner_id')
    except:
        pass
    
    # 方法 3: 默认值 (开发环境)
    return "ou_baa3525cf6cb5c0fc1ce4e26753d812d"

if __name__ == "__main__":
    # 示例用法
    user_id = get_current_user_id()
    
    sample_session = {
        "bot_id": "cli_a922b6c0b8b89bd1",
        "bot_name": "小炸弹",
        "scene_type": "文档处理",
        "completion_status": "completed",
        "turn_count": 3,
        "correction_count": 0
    }
    
    collect_session_data(sample_session, user_id)
