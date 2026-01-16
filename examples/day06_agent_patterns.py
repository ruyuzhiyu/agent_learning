"""
Day 6: Agent架构设计示例代码
学习目标：理解不同的Agent模式和实现方式
"""

import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain import hub
from langchain.agents import AgentType, initialize_agent


# 初始化LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


# ========== 准备工具 ==========

def calculator(expression: str) -> str:
    """计算器工具"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def search(query: str) -> str:
    """搜索工具（模拟）"""
    mock_data = {
        "Python": "Python是一种高级编程语言",
        "北京人口": "北京常住人口约2100万",
        "AI Agent": "AI Agent是能够自主完成任务的智能系统"
    }
    for key in mock_data:
        if key.lower() in query.lower():
            return mock_data[key]
    return f"未找到关于'{query}'的信息"


# 创建工具列表
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="用于数学计算。输入数学表达式，返回计算结果。"
    ),
    Tool(
        name="Search",
        func=search,
        description="搜索信息。输入关键词，返回相关信息。"
    )
]


# ========== ReAct Agent示例 ==========

def react_agent_example():
    """
    ReAct Agent示例
    ReAct = Reasoning + Acting
    Agent会先思考（Reason），然后行动（Act）
    """
    print("ReAct Agent示例：")
    print("ReAct模式：Thought -> Action -> Observation -> ... -> Answer\n")
    
    # 创建ReAct Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,  # 显示思考过程
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    # 测试问题
    question = "北京有多少人口？如果每人每天需要2升水，一天总共需要多少升水？"
    print(f"问题: {question}\n")
    
    try:
        result = agent.run(question)
        print(f"\n最终答案: {result}")
    except Exception as e:
        print(f"执行出错: {e}")


# ========== Zero-shot Agent示例 ==========

def zero_shot_agent_example():
    """
    Zero-shot Agent示例
    不需要示例，直接根据工具描述决定使用哪个工具
    """
    print("\nZero-shot Agent示例：")
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    questions = [
        "什么是Python？",
        "计算 123 * 456",
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        try:
            answer = agent.run(q)
            print(f"答案: {answer}")
        except Exception as e:
            print(f"错误: {e}")
        print("-" * 60)


# ========== 自定义Agent示例 ==========

class SimpleAgent:
    """
    简单的自定义Agent实现
    展示Agent的基本思考循环
    """
    
    def __init__(self, llm, tools, max_iterations=5):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    def run(self, question: str) -> str:
        """
        执行Agent的思考-行动循环
        """
        print(f"开始处理问题: {question}\n")
        
        context = f"问题: {question}\n\n"
        context += "可用工具:\n"
        for name, tool in self.tools.items():
            context += f"- {name}: {tool.description}\n"
        
        for i in range(self.max_iterations):
            print(f"\n=== 迭代 {i+1} ===")
            
            # 1. 思考下一步
            prompt = f"""{context}

请分析当前情况，决定下一步行动：
1. 如果需要使用工具，回复: USE_TOOL: [工具名] [参数]
2. 如果已经可以回答，回复: ANSWER: [答案]

你的决定:"""
            
            from langchain.schema import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            decision = response.content.strip()
            
            print(f"Agent决定: {decision}")
            
            # 2. 执行决定
            if decision.startswith("USE_TOOL:"):
                # 解析工具调用
                parts = decision.replace("USE_TOOL:", "").strip().split(" ", 1)
                tool_name = parts[0]
                tool_input = parts[1] if len(parts) > 1 else ""
                
                # 调用工具
                if tool_name in self.tools:
                    observation = self.tools[tool_name].run(tool_input)
                    print(f"工具返回: {observation}")
                    context += f"\n观察: {observation}\n"
                else:
                    print(f"工具 {tool_name} 不存在")
                    
            elif decision.startswith("ANSWER:"):
                # 返回最终答案
                answer = decision.replace("ANSWER:", "").strip()
                return answer
            
            else:
                print("无法理解Agent的决定，尝试继续...")
        
        return "达到最大迭代次数，无法完成任务"


def custom_agent_example():
    """
    测试自定义Agent
    """
    print("\n自定义Agent示例：")
    
    agent = SimpleAgent(llm=llm, tools=tools)
    
    question = "计算 50 乘以 40"
    answer = agent.run(question)
    
    print(f"\n最终答案: {answer}")


# ========== Plan-and-Execute Agent示例 ==========

def plan_and_execute_concept():
    """
    Plan-and-Execute模式概念演示
    先规划整体步骤，再逐步执行
    """
    print("\nPlan-and-Execute模式概念：")
    
    problem = "查询北京人口，然后计算如果每人每天用水2升，一天需要多少升"
    
    # 模拟规划阶段
    print(f"问题: {problem}\n")
    print("规划阶段:")
    plan = [
        "步骤1: 使用Search工具查询北京人口",
        "步骤2: 提取人口数字",
        "步骤3: 使用Calculator计算总用水量（人口 * 2）",
        "步骤4: 返回答案"
    ]
    
    for step in plan:
        print(f"  {step}")
    
    # 模拟执行阶段
    print("\n执行阶段:")
    print("  执行步骤1: 查询北京人口")
    population_info = search("北京人口")
    print(f"  结果: {population_info}")
    
    print("  执行步骤2: 提取数字 2100万")
    population = 21000000
    
    print(f"  执行步骤3: 计算 {population} * 2")
    total_water = calculator(f"{population} * 2")
    print(f"  结果: {total_water}升")
    
    print(f"\n  最终答案: 北京一天需要约{total_water}升水")


# ========== Agent性能分析 ==========

def analyze_agent_performance():
    """
    分析Agent的决策过程和性能
    """
    print("\nAgent性能分析：")
    
    class AnalyzedAgent:
        """带性能分析的Agent"""
        
        def __init__(self, agent):
            self.agent = agent
            self.stats = {
                "tool_calls": 0,
                "iterations": 0,
                "errors": 0
            }
        
        def run(self, question):
            """运行并收集统计"""
            import time
            start_time = time.time()
            
            try:
                # 这里简化统计
                result = self.agent.run(question)
                self.stats["iterations"] = 1
                return result
            except Exception as e:
                self.stats["errors"] += 1
                raise e
            finally:
                elapsed = time.time() - start_time
                print(f"\n性能统计:")
                print(f"  执行时间: {elapsed:.2f}秒")
                print(f"  迭代次数: {self.stats['iterations']}")
                print(f"  错误次数: {self.stats['errors']}")
    
    # 创建并测试
    base_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False
    )
    
    analyzed = AnalyzedAgent(base_agent)
    result = analyzed.run("计算 10 + 20")
    print(f"结果: {result}")


if __name__ == "__main__":
    print("Day 6: Agent架构设计示例\n")
    print("="*60)
    
    # 示例1: ReAct Agent
    try:
        react_agent_example()
    except Exception as e:
        print(f"ReAct示例出错: {e}")
    
    print("\n" + "="*60)
    
    # 示例2: Plan-and-Execute概念
    plan_and_execute_concept()
    
    print("\n" + "="*60)
    
    # 示例3: 自定义Agent
    try:
        custom_agent_example()
    except Exception as e:
        print(f"自定义Agent示例出错: {e}")
    
    # 练习任务
    print("\n" + "="*60)
    print("练习任务：")
    print("="*60)
    print("1. 对比ReAct和Plan-and-Execute的优缺点")
    print("2. 实现一个支持多步推理的Agent")
    print("3. 优化Agent的决策流程，减少不必要的工具调用")
    print("4. 添加Agent的错误恢复机制")
    print("5. 分析并优化Agent的性能")
