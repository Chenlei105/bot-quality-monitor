#!/usr/bin/env python3
"""
会话指标采集器 - 四维健康度指标

采集维度:
1. 质量: 解决率 + 满意度
2. 效率: 任务解决时长
3. 资源: Token 消耗
4. 异常: 非预期中断 + P99 响应时长

输入: Session 历史记录
输出: 结构化指标数据
"""

import json
import sys
from datetime import datetime

def analyze_session(session_history):
    """
    分析单个会话,提取四维指标
    
    Args:
        session_history: sessions_history 返回的会话历史
    
    Returns:
        dict: 四维指标数据
    """
    messages = session_history.get("messages", [])
    if not messages:
        return None
    
    # 基础信息
    session_key = session_history.get("sessionKey", "")
    user_id = extract_user_id(session_key)
    scene_type = detect_scene_type(messages)
    
    # ========== 1. 质量维度 ==========
    quality_metrics = {
        "resolution_status": detect_resolution_status(messages),
        "satisfaction_score": calculate_satisfaction(messages),
        "correction_count": count_corrections(messages),
        "retry_count": count_retries(messages),
        "positive_signals": detect_positive_signals(messages),
        "negative_signals": detect_negative_signals(messages)
    }
    
    # ========== 2. 效率维度 ==========
    efficiency_metrics = {
        "total_duration_ms": calculate_total_duration(messages),
        "effective_duration_ms": calculate_effective_duration(messages),
        "round_count": count_rounds(messages),
        "avg_response_time_ms": calculate_avg_response_time(messages),
        "p99_response_time_ms": calculate_p99_response_time(messages)
    }
    
    # ========== 3. 资源维度 ==========
    resource_metrics = {
        "total_input_tokens": sum_tokens(messages, "input"),
        "total_output_tokens": sum_tokens(messages, "output"),
        "total_tokens": sum_tokens(messages, "total"),
        "tool_calls_count": count_tool_calls(messages),
        "avg_tokens_per_round": calculate_avg_tokens_per_round(messages)
    }
    
    # ========== 4. 异常维度 ==========
    exception_metrics = {
        "unexpected_interruption": detect_unexpected_interruption(messages),
        "error_count": count_errors(messages),
        "timeout_count": count_timeouts(messages),
        "abnormal_exit": detect_abnormal_exit(messages)
    }
    
    # 汇总
    return {
        "session_key": session_key,
        "user_id": user_id,
        "scene_type": scene_type,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "quality": quality_metrics,
        "efficiency": efficiency_metrics,
        "resource": resource_metrics,
        "exception": exception_metrics,
        "metadata": {
            "message_count": len(messages),
            "start_time": messages[0].get("timestamp") if messages else None,
            "end_time": messages[-1].get("timestamp") if messages else None
        }
    }

# ========== 质量维度分析函数 ==========

def detect_resolution_status(messages):
    """判断任务是否解决"""
    # 正向信号: 自然结束、深入探索
    # 负向信号: 重复追问、辱骂、跳入竞品
    user_messages = [m for m in messages if m.get("role") == "user"]
    assistant_messages = [m for m in messages if m.get("role") == "assistant"]
    
    if not user_messages or not assistant_messages:
        return "unknown"
    
    # 检查最后几条消息
    last_user = user_messages[-1].get("content", [])
    last_user_text = extract_text(last_user).lower()
    
    # 负向信号
    negative_keywords = ["不对", "错了", "不行", "重新", "垃圾", "差劲", "没用"]
    if any(kw in last_user_text for kw in negative_keywords):
        return "failed"
    
    # 正向信号: 感谢、确认
    positive_keywords = ["谢谢", "好的", "明白", "可以", "👍", "👌"]
    if any(kw in last_user_text for kw in positive_keywords):
        return "resolved"
    
    # 默认: 根据轮次判断
    if len(user_messages) <= 3:
        return "resolved"  # 短对话默认解决
    else:
        return "partial"  # 长对话可能未完全解决

def calculate_satisfaction(messages):
    """计算满意度评分 (0-100)"""
    score = 70  # 基准分
    
    # 追问/重试次数 (负向)
    retry_count = count_retries(messages)
    score -= retry_count * 5
    
    # 纠错次数 (负向)
    correction_count = count_corrections(messages)
    score -= correction_count * 10
    
    # 正向信号 (点赞、感谢等)
    positive_count = len(detect_positive_signals(messages))
    score += positive_count * 10
    
    # 负向信号 (点踩、辱骂等)
    negative_count = len(detect_negative_signals(messages))
    score -= negative_count * 15
    
    return max(0, min(100, score))

def count_corrections(messages):
    """统计纠错次数"""
    correction_keywords = ["错了", "不对", "重新", "修改", "更正"]
    count = 0
    for msg in messages:
        if msg.get("role") == "user":
            text = extract_text(msg.get("content", [])).lower()
            if any(kw in text for kw in correction_keywords):
                count += 1
    return count

def count_retries(messages):
    """统计重试次数 (语义重复检测)"""
    # 简化版: 检测连续相似的用户消息
    user_messages = [m for m in messages if m.get("role") == "user"]
    retry_count = 0
    for i in range(1, len(user_messages)):
        prev_text = extract_text(user_messages[i-1].get("content", []))
        curr_text = extract_text(user_messages[i].get("content", []))
        # 简单的相似度判断
        if len(prev_text) > 10 and len(curr_text) > 10:
            if text_similarity(prev_text, curr_text) > 0.7:
                retry_count += 1
    return retry_count

def detect_positive_signals(messages):
    """检测正向信号"""
    signals = []
    positive_keywords = ["谢谢", "感谢", "赞", "好的", "明白", "👍", "👌", "🎉"]
    for msg in messages:
        if msg.get("role") == "user":
            text = extract_text(msg.get("content", []))
            for kw in positive_keywords:
                if kw in text:
                    signals.append({"type": "positive_keyword", "keyword": kw})
    return signals

def detect_negative_signals(messages):
    """检测负向信号"""
    signals = []
    negative_keywords = ["垃圾", "差劲", "没用", "不行", "烂", "👎"]
    for msg in messages:
        if msg.get("role") == "user":
            text = extract_text(msg.get("content", []))
            for kw in negative_keywords:
                if kw in text:
                    signals.append({"type": "negative_keyword", "keyword": kw})
    return signals

# ========== 效率维度分析函数 ==========

def calculate_total_duration(messages):
    """计算总时长 (ms)"""
    if len(messages) < 2:
        return 0
    start_time = parse_timestamp(messages[0].get("timestamp"))
    end_time = parse_timestamp(messages[-1].get("timestamp"))
    return int((end_time - start_time) * 1000)

def calculate_effective_duration(messages):
    """计算有效时长 (扣除用户思考时间)"""
    # 如果两条消息间隔 > 5 分钟,认为是用户思考,不计入有效时长
    threshold_ms = 5 * 60 * 1000
    total_ms = 0
    for i in range(1, len(messages)):
        prev_time = parse_timestamp(messages[i-1].get("timestamp"))
        curr_time = parse_timestamp(messages[i].get("timestamp"))
        gap_ms = int((curr_time - prev_time) * 1000)
        if gap_ms <= threshold_ms:
            total_ms += gap_ms
    return total_ms

def count_rounds(messages):
    """统计对话轮次"""
    return len([m for m in messages if m.get("role") == "user"])

def calculate_avg_response_time(messages):
    """计算平均响应时间"""
    response_times = []
    for i in range(1, len(messages)):
        if messages[i-1].get("role") == "user" and messages[i].get("role") == "assistant":
            prev_time = parse_timestamp(messages[i-1].get("timestamp"))
            curr_time = parse_timestamp(messages[i].get("timestamp"))
            response_times.append((curr_time - prev_time) * 1000)
    return int(sum(response_times) / len(response_times)) if response_times else 0

def calculate_p99_response_time(messages):
    """计算 P99 响应时间"""
    response_times = []
    for i in range(1, len(messages)):
        if messages[i-1].get("role") == "user" and messages[i].get("role") == "assistant":
            prev_time = parse_timestamp(messages[i-1].get("timestamp"))
            curr_time = parse_timestamp(messages[i].get("timestamp"))
            response_times.append((curr_time - prev_time) * 1000)
    if not response_times:
        return 0
    response_times.sort()
    p99_index = int(len(response_times) * 0.99)
    return int(response_times[p99_index]) if p99_index < len(response_times) else 0

# ========== 资源维度分析函数 ==========

def sum_tokens(messages, token_type):
    """统计 Token 消耗"""
    total = 0
    for msg in messages:
        usage = msg.get("usage", {})
        if token_type == "input":
            total += usage.get("input", 0)
        elif token_type == "output":
            total += usage.get("output", 0)
        elif token_type == "total":
            total += usage.get("totalTokens", usage.get("input", 0) + usage.get("output", 0))
    return total

def count_tool_calls(messages):
    """统计工具调用次数"""
    count = 0
    for msg in messages:
        content = msg.get("content", [])
        for item in content:
            if item.get("type") == "toolCall":
                count += 1
    return count

def calculate_avg_tokens_per_round(messages):
    """计算每轮平均 Token"""
    total_tokens = sum_tokens(messages, "total")
    rounds = count_rounds(messages)
    return int(total_tokens / rounds) if rounds > 0 else 0

# ========== 异常维度分析函数 ==========

def detect_unexpected_interruption(messages):
    """检测非预期中断"""
    # 如果最后一条是用户消息且没有助手回复,可能是中断
    if messages and messages[-1].get("role") == "user":
        return True
    return False

def count_errors(messages):
    """统计错误次数"""
    count = 0
    for msg in messages:
        content = extract_text(msg.get("content", []))
        if "错误" in content or "失败" in content or "error" in content.lower():
            count += 1
    return count

def count_timeouts(messages):
    """统计超时次数"""
    # 检测响应时间超过 30 秒的情况
    timeout_threshold_ms = 30 * 1000
    count = 0
    for i in range(1, len(messages)):
        if messages[i-1].get("role") == "user" and messages[i].get("role") == "assistant":
            prev_time = parse_timestamp(messages[i-1].get("timestamp"))
            curr_time = parse_timestamp(messages[i].get("timestamp"))
            if (curr_time - prev_time) * 1000 > timeout_threshold_ms:
                count += 1
    return count

def detect_abnormal_exit(messages):
    """检测异常退出"""
    # 检测最后一条助手消息包含"抱歉"/"无法"等
    assistant_messages = [m for m in messages if m.get("role") == "assistant"]
    if assistant_messages:
        last_text = extract_text(assistant_messages[-1].get("content", []))
        if "抱歉" in last_text or "无法" in last_text or "不能" in last_text:
            return True
    return False

# ========== 辅助函数 ==========

def extract_user_id(session_key):
    """从 session_key 提取用户 ID"""
    # session_key 格式: agent:main:feishu:direct:ou_xxx
    parts = session_key.split(":")
    return parts[-1] if len(parts) > 4 else "unknown"

def detect_scene_type(messages):
    """检测场景类型"""
    all_text = " ".join([extract_text(m.get("content", [])) for m in messages])
    
    scene_keywords = {
        "数据分析": ["数据", "统计", "分析", "图表", "dashboard"],
        "文档处理": ["文档", "docx", "pdf", "编辑", "写", "生成文档"],
        "健康诊断": ["健康", "诊断", "检查", "问题"],
        "搜索查询": ["搜索", "查询", "找", "search"],
        "代码调试": ["代码", "bug", "调试", "运行", "脚本"],
        "闲聊": ["你好", "怎么样", "谢谢", "聊天"]
    }
    
    for scene, keywords in scene_keywords.items():
        if any(kw in all_text for kw in keywords):
            return scene
    
    return "其他"

def extract_text(content_list):
    """从 content 数组提取文本"""
    text_parts = []
    for item in content_list:
        if item.get("type") == "text":
            text_parts.append(item.get("text", ""))
    return " ".join(text_parts)

def parse_timestamp(ts_str):
    """解析时间戳"""
    try:
        # 尝试解析 ISO 格式
        from dateutil import parser
        return parser.parse(ts_str).timestamp()
    except:
        # Fallback: 当前时间
        return datetime.now().timestamp()

def text_similarity(text1, text2):
    """简单的文本相似度计算"""
    # 简化版: 基于词重叠率
    words1 = set(text1.split())
    words2 = set(text2.split())
    if not words1 or not words2:
        return 0
    overlap = len(words1 & words2)
    return overlap / min(len(words1), len(words2))

# ========== 主函数 ==========

if __name__ == "__main__":
    # 从标准输入读取 session 历史
    if len(sys.argv) > 1:
        session_json = sys.argv[1]
        session_history = json.loads(session_json)
    else:
        session_history = json.load(sys.stdin)
    
    metrics = analyze_session(session_history)
    
    if metrics:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "No messages found"}, ensure_ascii=False))
