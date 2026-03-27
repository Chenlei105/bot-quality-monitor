#!/usr/bin/env python3
"""
Webhook 消息自动入库脚本

功能:
- 每 10 分钟搜索飞书消息
- 筛选 "Bot Quality Monitor 使用数据上报" 卡片消息
- 提取 JSON 数据并写入中央表格
- 记录已处理的消息,避免重复

用法:
    在 HEARTBEAT.md 中配置自动运行
    或手动测试: python3 process-webhook-messages.py
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

# 配置
CENTRAL_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
CENTRAL_TABLE_ID = "tbllGdVAIIzITahT"  # L0_Skill_Usage

PROCESSED_LOG_PATH = Path.home() / ".openclaw/workspace/logs/processed-webhook-messages.json"
ERROR_LOG_PATH = Path.home() / ".openclaw/workspace/logs/webhook-processing-error.log"

# 确保日志目录存在
PROCESSED_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
ERROR_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    
    if level == "ERROR":
        with open(ERROR_LOG_PATH, "a") as f:
            f.write(log_message + "\n")

def load_processed_messages():
    """加载已处理消息记录"""
    try:
        if not PROCESSED_LOG_PATH.exists():
            return {}
        
        with open(PROCESSED_LOG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"加载已处理记录失败: {e}", "WARN")
        return {}

def save_processed_message(message_id, event_count, records_written):
    """保存已处理消息"""
    try:
        processed = load_processed_messages()
        processed[message_id] = {
            "processed_at": int(datetime.now().timestamp() * 1000),
            "event_count": event_count,
            "records_written": records_written
        }
        
        with open(PROCESSED_LOG_PATH, "w") as f:
            json.dump(processed, f, indent=2)
        
        log(f"已保存处理记录: {message_id}")
    except Exception as e:
        log(f"保存处理记录失败: {e}", "ERROR")

def extract_json_from_card(card_content):
    """
    从飞书卡片中提取 JSON 数据
    
    卡片格式:
    {
      "elements": [
        {
          "tag": "div",
          "text": {
            "content": "```json\\n[...]\\n```"
          }
        }
      ]
    }
    """
    try:
        # 方法 1: 从 card 结构中提取
        if isinstance(card_content, dict):
            elements = card_content.get("elements", [])
            for element in elements:
                if element.get("tag") == "div":
                    text_content = element.get("text", {}).get("content", "")
                    
                    # 提取 ```json ... ``` 中的内容
                    match = re.search(r'```json\s*\n(.*?)\n```', text_content, re.DOTALL)
                    if match:
                        json_str = match.group(1).strip()
                        return json.loads(json_str)
        
        # 方法 2: 直接解析文本
        if isinstance(card_content, str):
            match = re.search(r'```json\s*\n(.*?)\n```', card_content, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                return json.loads(json_str)
        
        return None
    except Exception as e:
        log(f"提取 JSON 失败: {e}", "ERROR")
        return None

def main():
    """主流程"""
    log("=" * 60)
    log("Webhook 消息自动入库任务开始")
    log("=" * 60)
    
    # 1. 加载已处理消息
    processed = load_processed_messages()
    log(f"已处理消息数: {len(processed)}")
    
    # 2. 计算搜索时间范围 (最近 15 分钟)
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=15)
    
    # 输出 OpenClaw 指令,由 Heartbeat 执行
    workflow = {
        "action": "process_webhook_messages",
        "steps": [
            {
                "step": 1,
                "description": "搜索最近 15 分钟的 Webhook 消息",
                "tool": "feishu_im_user_search_messages",
                "params": {
                    "query": "Bot Quality Monitor 使用数据上报",
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "sender_type": "bot",
                    "page_size": 50
                },
                "save_output": "messages"
            },
            {
                "step": 2,
                "description": "过滤未处理的消息",
                "processed_messages": list(processed.keys()),
                "python_logic": "filter_unprocessed_messages"
            },
            {
                "step": 3,
                "description": "提取每条消息的 JSON 数据",
                "python_logic": "extract_json_from_card",
                "foreach": "unprocessed_messages"
            },
            {
                "step": 4,
                "description": "批量写入中央表格",
                "tool": "feishu_bitable_app_table_record",
                "params": {
                    "action": "batch_create",
                    "app_token": CENTRAL_APP_TOKEN,
                    "table_id": CENTRAL_TABLE_ID,
                    "records": "${extracted_events}"
                }
            },
            {
                "step": 5,
                "description": "保存已处理消息",
                "python_logic": "save_processed_message",
                "foreach": "processed_messages"
            }
        ],
        "silent": True  # 静默执行,无需回复
    }
    
    print(json.dumps(workflow, indent=2, ensure_ascii=False))
    
    log("=" * 60)
    log("Webhook 消息自动入库任务结束")
    log("=" * 60)

if __name__ == "__main__":
    main()
