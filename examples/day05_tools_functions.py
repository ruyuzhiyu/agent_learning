"""
Day 5: Tools和Function Calling示例代码
学习目标：掌握工具的创建和使用，理解Function Calling机制
"""

import os
import json
from datetime import datetime
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain import hub
from pydantic import BaseModel, Field


# 初始化LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


# ========== 基础工具示例 ==========

# 支持的安全操作符
import ast
import operator

_calc_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval_expr(node):
    """安全地评估数学表达式"""
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        op = _calc_operators.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的操作符")
        return op(_safe_eval_expr(node.left), _safe_eval_expr(node.right))
    elif isinstance(node, ast.UnaryOp):
        op = _calc_operators.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的操作符")
        return op(_safe_eval_expr(node.operand))
    else:
        raise ValueError(f"不支持的节点类型")


def calculator(expression: str) -> str:
    """
    计算器工具：计算数学表达式（使用安全的AST解析）
    """
    try:
        tree = ast.parse(expression, mode='eval')
        result = _safe_eval_expr(tree.body)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_current_time(timezone: Optional[str] = None) -> str:
    """
    获取当前时间工具
    """
    now = datetime.now()
    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def search_mock(query: str) -> str:
    """
    模拟搜索工具
    实际使用中可以接入真实的搜索API
    """
    # 这里只是模拟返回
    mock_results = {
        "天气": "今天北京天气晴朗，温度15-25度",
        "AI": "AI是人工智能的缩写，指机器展现的智能",
        "Python": "Python是一种流行的编程语言"
    }
    
    for key in mock_results:
        if key in query:
            return mock_results[key]
    
    return f"搜索'{query}'的结果: 未找到相关信息"


# ========== 自定义工具类 ==========

class WeatherTool(BaseTool):
    """
    天气查询工具
    继承BaseTool创建自定义工具
    """
    name = "weather_query"
    description = "查询指定城市的天气情况。输入城市名称，返回天气信息。"
    
    def _run(self, city: str) -> str:
        """同步执行"""
        # 模拟天气数据
        weather_data = {
            "北京": "晴天，15-25度，空气质量良好",
            "上海": "多云，18-26度，有轻微雾霾",
            "深圳": "阴天，22-28度，湿度较高"
        }
        
        return weather_data.get(city, f"{city}的天气信息暂时无法获取")
    
    async def _arun(self, city: str) -> str:
        """异步执行"""
        return self._run(city)


class CodeExecutor(BaseTool):
    """
    代码执行工具（仅用于教学演示，实际使用需要沙箱环境）
    """
    name = "code_executor"
    description = "执行简单的Python数学表达式并返回结果。仅支持基本的数学运算。"
    
    def _run(self, code: str) -> str:
        """执行代码"""
        try:
            # 安全起见，实际使用应该有沙箱环境
            # 这里只允许简单的数学表达式
            if any(keyword in code for keyword in ['import', 'exec', 'eval', 'open', '__']):
                return "代码包含不允许的操作"
            
            # 使用AST安全解析（仅支持数学表达式）
            tree = ast.parse(code, mode='eval')
            result = _safe_eval_expr(tree.body)
            return f"执行结果: {result}"
        except Exception as e:
            return f"执行错误: {str(e)}"
    
    async def _arun(self, code: str) -> str:
        return self._run(code)


# ========== Function Calling示例 ==========

def function_calling_example():
    """
    使用OpenAI的Function Calling功能
    """
    print("Function Calling示例：")
    
    # 定义函数
    functions = [
        {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：2+2, 10*5"
                    }
                },
                "required": ["expression"]
            }
        }
    ]
    
    # 创建消息
    messages = [
        {"role": "user", "content": "北京今天天气怎么样？"}
    ]
    
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 调用API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    
    message = response.choices[0].message
    
    if message.function_call:
        print(f"\nLLM选择调用函数: {message.function_call.name}")
        print(f"参数: {message.function_call.arguments}")
        
        # 执行函数
        if message.function_call.name == "get_weather":
            args = json.loads(message.function_call.arguments)
            result = f"北京天气：晴天，25度"
            print(f"函数返回: {result}")


# ========== 使用LangChain Tools ==========

def langchain_tools_example():
    """
    使用LangChain工具
    """
    print("\nLangChain Tools示例：")
    
    # 创建工具列表
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="用于执行数学计算。输入一个数学表达式，返回计算结果。"
        ),
        Tool(
            name="CurrentTime",
            func=get_current_time,
            description="获取当前时间。不需要输入参数。"
        ),
        Tool(
            name="Search",
            func=search_mock,
            description="搜索信息。输入搜索关键词，返回相关信息。"
        ),
        WeatherTool()  # 自定义工具
    ]
    
    # 打印工具信息
    print("\n可用工具:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    # 手动使用工具
    print("\n手动调用工具示例:")
    print(tools[0].run("10 * 5 + 3"))
    print(tools[1].run(""))
    print(tools[3].run("北京"))


# ========== 工具链组合 ==========

def tool_chain_example():
    """
    组合多个工具完成复杂任务
    """
    print("\n工具链示例：")
    
    # 场景：查询天气后，根据温度计算体感温度
    
    # 1. 查询天气
    weather_result = "北京：晴天，25度"
    print(f"步骤1 - 查询天气: {weather_result}")
    
    # 2. 提取温度（这里简化处理）
    temperature = 25
    print(f"步骤2 - 提取温度: {temperature}度")
    
    # 3. 计算体感温度（简化公式）
    humidity = 60  # 假设湿度60%
    feels_like = temperature + (humidity - 50) * 0.1
    print(f"步骤3 - 计算体感温度: {feels_like}度")
    
    # 4. 生成建议
    if feels_like > 28:
        suggestion = "天气较热，建议穿短袖，多喝水"
    elif feels_like > 20:
        suggestion = "天气舒适，适合外出活动"
    else:
        suggestion = "天气较凉，建议加件外套"
    
    print(f"步骤4 - 穿衣建议: {suggestion}")


# ========== 带参数验证的工具 ==========

class EmailInput(BaseModel):
    """邮件工具的输入参数"""
    to: str = Field(description="收件人邮箱地址")
    subject: str = Field(description="邮件主题")
    body: str = Field(description="邮件正文")


class EmailTool(BaseTool):
    """
    发送邮件工具（模拟）
    """
    name = "send_email"
    description = "发送邮件。需要提供收件人、主题和正文。"
    args_schema = EmailInput
    
    def _run(self, to: str, subject: str, body: str) -> str:
        """发送邮件"""
        # 实际实现中应该调用邮件服务
        return f"邮件已发送至 {to}\n主题: {subject}\n内容: {body[:50]}..."
    
    async def _arun(self, to: str, subject: str, body: str) -> str:
        return self._run(to, subject, body)


if __name__ == "__main__":
    print("Day 5: Tools和Function Calling示例\n")
    print("="*60)
    
    # 示例1: Function Calling
    try:
        function_calling_example()
    except Exception as e:
        print(f"Function Calling示例需要OpenAI API: {e}")
    
    print("\n" + "="*60)
    
    # 示例2: LangChain Tools
    langchain_tools_example()
    
    print("\n" + "="*60)
    
    # 示例3: 工具链
    tool_chain_example()
    
    print("\n" + "="*60)
    
    # 示例4: 带参数验证的工具
    email_tool = EmailTool()
    print("\n带参数验证的工具示例:")
    print(email_tool.run({
        "to": "example@example.com",
        "subject": "测试邮件",
        "body": "这是一封测试邮件"
    }))
    
    # 练习任务
    print("\n" + "="*60)
    print("练习任务：")
    print("="*60)
    print("1. 创建一个文件操作工具（读取、写入）")
    print("2. 实现一个数据库查询工具（模拟）")
    print("3. 组合多个工具完成：查询天气→生成报告→发送邮件")
    print("4. 添加工具调用的错误处理和重试机制")
