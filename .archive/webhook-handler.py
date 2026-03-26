#!/usr/bin/env python3
"""
飞书 Webhook 消息处理器

功能:
- 监听飞书 Webhook 消息（Bot 数据收集）
- 解析 JSON 数据
- 写入飞书多维表格

运行:
    在 HEARTBEAT.md 中配置自动运行
    或手动测试: python3 webhook-handler.py <message_id>
"""

import os
import sys
import json
from datetime import datetime

# 飞书多维表格配置
BITABLE_APP_TOKEN = "Xw4Tb5C8KagMiQswkdacNfVPn8e"
TABLE_ID = "tbllGdVAIIzITahT"

def parse_webhook_message(message_content):
    """
    解析 Webhook 消息内容
    
    消息格式：飞书卡片，包含 JSON 数据
    """
    try:
        # 提取卡片中的 JSON 数据
        # 假设卡片第二个元素包含 JSON
        if "elements" in message_content:
            for element in message_content.get("elements", []):
                if element.get("tag") == "div":
                    text_content = element.get("text", {}).get("content", "")
                    # 提取 ``` 中的 JSON
                    if "```json" in text_content:
                        json_start = text_content.find("```json") + 7
                        json_end = text_content.find("```", json_start)
                        json_str = text_content[json_start:json_end].strip()
                        return json.loads(json_str)
        
        return None
    except Exception as e:
        print(f"[webhook] 解析失败: {e}")
        return None

def write_to_bitable(events):
    """
    将事件写入飞书多维表格
    
    Args:
        events: 事件列表
    """
    if not events:
        print("[webhook] 没有数据需要写入")
        return
    
    print(f"[webhook] 准备写入 {len(events)} 条记录到 {BITABLE_APP_TOKEN}/{TABLE_ID}")
    
    # 构造 feishu_bitable_app_table_record 调用
    # 这里返回一个指令，由 OpenClaw Agent 执行
    batch_data = {
        "app_token": BITABLE_APP_TOKEN,
        "table_id": TABLE_ID,
        "records": [{"fields": event} for event in events]
    }
    
    # 保存到临时文件，供 Heartbeat 读取
    temp_file = os.path.expanduser("~/.openclaw/workspace/logs/webhook-batch.json")
    with open(temp_file, "w") as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
    
    print(f"[webhook] 已保存到临时文件: {temp_file}")
    print(f"[webhook] 请在 Heartbeat 中调用 feishu_bitable_app_table_record 批量写入")
    
    return temp_file

def handle_webhook_message(message_id):
    """
    处理 Webhook 消息
    
    Args:
        message_id: 飞书消息 ID
    """
    print(f"[webhook] 处理消息: {message_id}")
    
    # 这里应该调用飞书 API 获取消息内容
    # 简化版：假设消息内容已经在环境变量中
    # 实际使用时需要调用 feishu_im_user_get_messages 或类似工具
    
    # 示例：从标准输入读取消息内容
    if len(sys.argv) > 2:
        message_json = sys.argv[2]
        message_data = json.loads(message_json)
        
        events = parse_webhook_message(message_data)
        if events:
            write_to_bitable(events)
        else:
            print("[webhook] 未找到有效数据")
    else:
        print("[webhook] 用法: webhook-handler.py <message_id> '<message_json>'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: webhook-handler.py <message_id> ['<message_json>']")
        sys.exit(1)
    
    message_id = sys.argv[1]
    handle_webhook_message(message_id)
