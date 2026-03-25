#!/usr/bin/env python3
"""
Bot 数据自动采集脚本（Session Hook 版本）
在 OpenClaw 环境中运行，每次对话结束后自动触发

用法：
1. 由 OpenClaw Skill 系统自动调用
2. 或手动触发：python3 auto-collect.py <session_key>
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# OpenClaw 工具导入（仅在 OpenClaw 环境中有效）
try:
    from openclaw_tools import feishu_bitable_app_table_record, sessions_history
except ImportError:
    print("⚠️ 警告：未在 OpenClaw 环境中运行，使用模拟模式")
    feishu_bitable_app_table_record = None
    sessions_history = None

# 配置
APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
L1_TABLE_ID = "tblmKO3HejbWpUWe"  # L1_消息明细
L2_TABLE_ID = "tblT0I1nCFhbpvGa"  # L2_会话汇总

def log(message):
    """输出日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def extract_session_data(session_key):
    """
    从 OpenClaw Session 提取会话数据
    
    Args:
        session_key: Session 标识符
        
    Returns:
        dict: 会话数据
    """
    if not sessions_history:
        log("⚠️ 模拟模式：跳过会话数据提取")
        return None
    
    try:
        # 获取最近的对话历史
        history = sessions_history(
            sessionKey=session_key,
            limit=50,
            includeTools=True
        )
        
        if not history or 'messages' not in history:
            log(f"⚠️ Session {session_key} 无有效历史记录")
            return None
        
        messages = history['messages']
        
        # 提取关键信息
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
        if "抱歉" in last_assistant.get('content', '') or "无法" in last_assistant.get('content', ''):
            completion_status = "failed"
        
        # 提取模型信息
        model_name = history.get('model', 'unknown')
        
        # 提取用户信息
        user_owner_id = history.get('metadata', {}).get('sender_id', 'unknown')
        
        return {
            "session_key": session_key,
            "user_owner_id": user_owner_id,
            "bot_id": "cli_a922b6c0b8b89bd1",  # 从 openclaw.json 读取
            "bot_name": "小炸弹 💣",
            "scene_type": scene_type,
            "turn_count": len(user_messages),
            "correction_count": correction_count,
            "tool_call_count": len(tool_calls),
            "completion_status": completion_status,
            "model_name": model_name,
            "start_time": messages[0].get('timestamp') if messages else None,
            "end_time": messages[-1].get('timestamp') if messages else None
        }
        
    except Exception as e:
        log(f"❌ 提取会话数据失败: {str(e)}")
        import traceback
        log(traceback.format_exc())
        return None

def identify_scene_type(messages):
    """
    识别场景类型
    
    Args:
        messages: 消息列表
        
    Returns:
        str: 场景类型
    """
    # 合并所有用户消息
    user_text = " ".join([
        m.get('content', '') 
        for m in messages 
        if m.get('role') == 'user'
    ]).lower()
    
    # 场景关键词匹配
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

def upload_to_feishu(session_data):
    """
    上传会话数据到飞书多维表格
    
    Args:
        session_data: 会话数据字典
        
    Returns:
        bool: 是否成功
    """
    if not feishu_bitable_app_table_record:
        log("⚠️ 模拟模式：跳过飞书上传")
        return False
    
    try:
        # 写入 L2_会话汇总表
        result = feishu_bitable_app_table_record(
            action="create",
            app_token=APP_TOKEN,
            table_id=L2_TABLE_ID,
            fields={
                "会话ID": session_data["session_key"],
                "用户所有者ID": session_data["user_owner_id"],
                "Bot ID": session_data["bot_id"],
                "Bot昵称": session_data["bot_name"],
                "场景类型": session_data["scene_type"],
                "轮次数": session_data["turn_count"],
                "纠错次数": session_data["correction_count"],
                "工具调用次数": session_data["tool_call_count"],
                "完成状态": session_data["completion_status"],
                "模型名称": session_data["model_name"],
                "开始时间": session_data["start_time"],
                "结束时间": session_data["end_time"],
                "创建时间": int(datetime.now().timestamp() * 1000)
            }
        )
        
        log(f"✅ 成功上传会话数据到飞书: {session_data['session_key']}")
        return True
        
    except Exception as e:
        log(f"❌ 上传飞书失败: {str(e)}")
        import traceback
        log(traceback.format_exc())
        return False

def process_session(session_key):
    """
    处理单个会话
    
    Args:
        session_key: Session 标识符
        
    Returns:
        bool: 是否成功
    """
    log(f"开始处理会话: {session_key}")
    
    # 1. 提取会话数据
    session_data = extract_session_data(session_key)
    if not session_data:
        log(f"⚠️ 无法提取会话数据，跳过")
        return False
    
    # 2. 上传到飞书
    success = upload_to_feishu(session_data)
    
    if success:
        log(f"✅ 会话处理完成: {session_key}")
    else:
        log(f"⚠️ 会话处理部分失败: {session_key}")
    
    return success

def main():
    """
    主流程
    """
    log("=" * 60)
    log("Bot 数据自动采集任务开始")
    log("=" * 60)
    
    # 从命令行参数获取 session_key
    if len(sys.argv) > 1:
        session_key = sys.argv[1]
        log(f"手动触发模式: session_key={session_key}")
        process_session(session_key)
    else:
        # 自动模式：扫描最近的 session
        log("自动模式：扫描最近的活跃会话")
        
        # TODO: 调用 sessions_list 获取最近的会话列表
        # 这里需要根据实际情况实现
        
        log("⚠️ 自动模式暂未实现，请使用手动触发模式")
        log("用法: python3 auto-collect.py <session_key>")
    
    log("=" * 60)
    log("Bot 数据自动采集任务结束")
    log("=" * 60)

if __name__ == "__main__":
    main()
