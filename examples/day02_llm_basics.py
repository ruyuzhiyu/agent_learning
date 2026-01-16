"""
Day 2: 大模型基础示例代码
学习目标：理解LLM的基本使用和Prompt Engineering
"""

import os
from openai import OpenAI
import ast
import operator

# 初始化客户端（需要设置环境变量 OPENAI_API_KEY）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 支持的安全操作符
_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """安全地评估数学表达式"""
    if isinstance(node, ast.Num):  # 数字
        return node.n
    elif isinstance(node, ast.BinOp):  # 二元运算符
        op = _operators.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的操作符: {type(node.op).__name__}")
        return op(_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # 一元运算符
        op = _operators.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的操作符: {type(node.op).__name__}")
        return op(_safe_eval(node.operand))
    else:
        raise ValueError(f"不支持的节点类型: {type(node).__name__}")


def calculator(expression: str) -> str:
    """
    计算器工具：计算数学表达式（使用安全的AST解析）
    """
    try:
        # 使用AST安全解析和执行
        tree = ast.parse(expression, mode='eval')
        result = _safe_eval(tree.body)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"
    """
    基础的LLM调用示例
    
    Args:
        prompt: 输入提示词
        temperature: 温度参数，控制输出的随机性（0-2）
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=500
    )
    
    return response.choices[0].message.content


def chat_with_system_prompt(system_prompt: str, user_message: str):
    """
    使用系统提示词的对话示例
    系统提示词用于定义AI的角色和行为
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.choices[0].message.content


def multi_turn_conversation():
    """
    多轮对话示例
    展示如何维护对话历史
    """
    messages = [
        {"role": "system", "content": "你是一个友好的AI助手。"}
    ]
    
    # 第一轮
    messages.append({"role": "user", "content": "我叫小明"})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})
    print(f"AI: {assistant_message}")
    
    # 第二轮 - AI应该记得用户的名字
    messages.append({"role": "user", "content": "我叫什么名字？"})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_message = response.choices[0].message.content
    print(f"AI: {assistant_message}")


def test_different_temperatures():
    """
    测试不同温度参数的效果
    temperature越低，输出越确定；越高，输出越随机
    """
    prompt = "写一句关于春天的诗"
    
    print("Temperature = 0.1 (更确定):")
    print(basic_completion(prompt, temperature=0.1))
    print("\n" + "="*50 + "\n")
    
    print("Temperature = 1.5 (更随机):")
    print(basic_completion(prompt, temperature=1.5))


def prompt_engineering_examples():
    """
    Prompt Engineering示例
    展示不同提示词技巧
    """
    
    # 1. Few-shot Learning
    few_shot_prompt = """
    将以下句子翻译成英文：
    
    例子1:
    中文：你好
    英文：Hello
    
    例子2:
    中文：谢谢
    英文：Thank you
    
    中文：再见
    英文：
    """
    print("Few-shot示例:")
    print(basic_completion(few_shot_prompt))
    print("\n" + "="*50 + "\n")
    
    # 2. 结构化输出
    structured_prompt = """
    分析以下文本的情感，并以JSON格式输出：
    {
        "sentiment": "positive/negative/neutral",
        "confidence": 0.0-1.0,
        "keywords": []
    }
    
    文本：今天天气真好，心情很愉快！
    """
    print("结构化输出示例:")
    print(basic_completion(structured_prompt, temperature=0))


if __name__ == "__main__":
    print("Day 2: 大模型基础示例\n")
    
    # 示例1: 基础调用
    print("="*50)
    print("示例1: 基础调用")
    print("="*50)
    result = basic_completion("什么是AI Agent？用一句话解释。")
    print(result)
    print()
    
    # 示例2: 使用系统提示词
    print("="*50)
    print("示例2: 系统提示词")
    print("="*50)
    result = chat_with_system_prompt(
        system_prompt="你是一个Python编程专家，用简洁的方式回答问题。",
        user_message="什么是装饰器？"
    )
    print(result)
    print()
    
    # 示例3: 多轮对话
    print("="*50)
    print("示例3: 多轮对话")
    print("="*50)
    multi_turn_conversation()
    print()
    
    # 练习任务
    print("\n" + "="*50)
    print("练习任务：")
    print("="*50)
    print("1. 尝试不同的temperature值，观察输出差异")
    print("2. 编写一个问答、总结和翻译的prompt")
    print("3. 实现一个简单的对话机器人")
    print("4. 测试token限制对输出的影响")
