#!/usr/bin/env python3
"""
场景分类器
根据对话内容智能识别用户意图场景
"""

import re
from typing import List, Dict, Any

# 场景关键词库（优先级从高到低）
SCENE_KEYWORDS = {
    "健康诊断": {
        "keywords": ["健康", "诊断", "检查", "监控", "dashboard", "问题", "质量", "失败", "错误"],
        "patterns": [r"bot.*质量", r"健康.*度", r"dashboard", r"监控.*数据"],
        "priority": 10
    },
    "数据分析": {
        "keywords": ["数据", "统计", "分析", "图表", "可视化", "报表", "趋势", "指标", "汇总"],
        "patterns": [r"p0.*dashboard", r"p1.*dashboard", r"p2.*dashboard", r"\d+.*天.*数据"],
        "priority": 9
    },
    "文档处理": {
        "keywords": ["文档", "docx", "pdf", "markdown", "编辑", "写", "生成文档", "上传", "下载", "云盘"],
        "patterns": [r"创建.*文档", r"编辑.*文档", r"\.docx", r"\.pdf"],
        "priority": 8
    },
    "技能管理": {
        "keywords": ["skill", "技能", "插件", "安装", "卸载", "skillhub", "clawhub", "find-skill"],
        "patterns": [r"安装.*skill", r"skill.*列表", r"skill.*管理"],
        "priority": 7
    },
    "配置咨询": {
        "keywords": ["配置", "设置", "openclaw", "模型", "token", "权限", "授权", "oauth"],
        "patterns": [r"openclaw\.json", r"配置.*文件", r"模型.*切换"],
        "priority": 6
    },
    "搜索查询": {
        "keywords": ["搜索", "查询", "找", "search", "tavily", "百度", "网络搜索"],
        "patterns": [r"搜索.*关于", r"查.*资料"],
        "priority": 5
    },
    "代码调试": {
        "keywords": ["代码", "bug", "调试", "运行", "脚本", "python", "bash", "cron", "定时任务"],
        "patterns": [r"\.py$", r"\.sh$", r"cron.*任务", r"脚本.*执行"],
        "priority": 4
    },
    "闲聊": {
        "keywords": ["聊天", "你好", "怎么样", "谢谢", "再见", "早安", "晚安", "辛苦"],
        "patterns": [r"^你好", r"谢谢", r"辛苦了"],
        "priority": 1
    }
}

def classify_scene(messages: List[Dict[str, Any]]) -> str:
    """
    分类场景
    
    Args:
        messages: 消息列表（OpenClaw session history format）
        
    Returns:
        str: 场景类型
    """
    # 提取用户消息文本
    user_messages = [
        msg.get('content', '') 
        for msg in messages 
        if msg.get('role') == 'user'
    ]
    
    # 合并所有用户消息
    if isinstance(user_messages[0], list):
        # content 是数组格式
        user_text = " ".join([
            " ".join([c.get('text', '') for c in content if c.get('type') == 'text'])
            for content in user_messages
        ])
    else:
        user_text = " ".join(user_messages)
    
    user_text_lower = user_text.lower()
    
    # 计算每个场景的得分
    scene_scores = {}
    
    for scene, config in SCENE_KEYWORDS.items():
        score = 0
        
        # 关键词匹配（每个匹配加 1 分）
        for keyword in config['keywords']:
            if keyword in user_text_lower:
                score += 1
        
        # 正则模式匹配（每个匹配加 2 分）
        for pattern in config.get('patterns', []):
            if re.search(pattern, user_text_lower, re.IGNORECASE):
                score += 2
        
        # 乘以优先级权重
        score *= config['priority']
        
        scene_scores[scene] = score
    
    # 选择得分最高的场景
    if not scene_scores or max(scene_scores.values()) == 0:
        return "其他"
    
    best_scene = max(scene_scores, key=scene_scores.get)
    
    # 如果最高分低于阈值，返回"其他"
    if scene_scores[best_scene] < 3:
        return "其他"
    
    return best_scene

def detect_correction_signals(messages: List[Dict[str, Any]]) -> int:
    """
    检测纠错信号次数
    
    Args:
        messages: 消息列表
        
    Returns:
        int: 纠错次数
    """
    correction_keywords = [
        "错了", "不对", "不是", "重新", "修改", "更正", 
        "再来一次", "不行", "有问题", "不准确", "不正确"
    ]
    
    user_messages = [
        msg.get('content', '') 
        for msg in messages 
        if msg.get('role') == 'user'
    ]
    
    correction_count = 0
    
    for msg in user_messages:
        if isinstance(msg, list):
            text = " ".join([c.get('text', '') for c in msg if c.get('type') == 'text'])
        else:
            text = msg
        
        for keyword in correction_keywords:
            if keyword in text:
                correction_count += 1
                break  # 每条消息最多算一次纠错
    
    return correction_count

def detect_completion_status(messages: List[Dict[str, Any]]) -> str:
    """
    检测完成状态
    
    Args:
        messages: 消息列表
        
    Returns:
        str: completed / failed / abandoned
    """
    # 提取最后一条 Assistant 消息
    assistant_messages = [
        msg for msg in messages 
        if msg.get('role') == 'assistant'
    ]
    
    if not assistant_messages:
        return "abandoned"
    
    last_assistant = assistant_messages[-1]
    last_content = last_assistant.get('content', '')
    
    if isinstance(last_content, list):
        last_text = " ".join([c.get('text', '') for c in last_content if c.get('type') == 'text'])
    else:
        last_text = last_content
    
    # 失败信号
    failure_signals = [
        "抱歉", "无法", "不能", "失败", "错误", 
        "不支持", "暂未实现", "TODO", "待开发"
    ]
    
    for signal in failure_signals:
        if signal in last_text:
            return "failed"
    
    # 放弃信号（用户长时间未回复）
    # TODO: 根据时间戳判断
    
    return "completed"

def detect_satisfaction_signal(messages: List[Dict[str, Any]]) -> str:
    """
    检测满意度信号
    
    Args:
        messages: 消息列表
        
    Returns:
        str: positive / negative / neutral
    """
    # 提取最后2条用户消息
    user_messages = [
        msg for msg in messages 
        if msg.get('role') == 'user'
    ]
    
    if not user_messages:
        return "neutral"
    
    recent_users = user_messages[-2:] if len(user_messages) >= 2 else user_messages
    
    positive_keywords = [
        "谢谢", "感谢", "好的", "太好了", "完美", "不错", 
        "👍", "🎉", "✅", "辛苦", "棒"
    ]
    
    negative_keywords = [
        "不对", "错了", "有问题", "不行", "算了", "不用了",
        "❌", "😡", "😤"
    ]
    
    positive_score = 0
    negative_score = 0
    
    for msg in recent_users:
        content = msg.get('content', '')
        if isinstance(content, list):
            text = " ".join([c.get('text', '') for c in content if c.get('type') == 'text'])
        else:
            text = content
        
        for keyword in positive_keywords:
            if keyword in text:
                positive_score += 1
        
        for keyword in negative_keywords:
            if keyword in text:
                negative_score += 1
    
    if positive_score > negative_score:
        return "positive"
    elif negative_score > positive_score:
        return "negative"
    else:
        return "neutral"

if __name__ == "__main__":
    # 测试用例
    test_messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": "帮我生成 P0 Dashboard"}]
        },
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "好的，我开始生成..."}]
        }
    ]
    
    print(f"场景类型: {classify_scene(test_messages)}")
    print(f"纠错次数: {detect_correction_signals(test_messages)}")
    print(f"完成状态: {detect_completion_status(test_messages)}")
    print(f"满意度: {detect_satisfaction_signal(test_messages)}")
