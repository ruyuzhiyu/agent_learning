"""
Week 1 项目：智能个人助手
主程序入口
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from tools.calendar import CalendarTool
from tools.weather import WeatherTool
from tools.calculator import CalculatorTool
from tools.memo import MemoTool

# 加载环境变量
load_dotenv()


def create_assistant():
    """
    创建智能助手Agent
    """
    # 初始化LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # 创建工具列表
    tools = [
        CalendarTool(),
        WeatherTool(),
        CalculatorTool(),
        MemoTool()
    ]
    
    # 获取ReAct提示词模板
    prompt = hub.pull("hwchase17/react")
    
    # 创建Agent
    agent = create_react_agent(llm, tools, prompt)
    
    # 创建Agent执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    return agent_executor


def main():
    """
    主程序
    """
    print("="*60)
    print("智能个人助手")
    print("="*60)
    print("\n我可以帮你：")
    print("- 管理日程（添加、查询日程）")
    print("- 查询天气")
    print("- 执行计算")
    print("- 记录备忘录")
    print("\n输入 'quit' 或 'exit' 退出\n")
    
    # 创建助手
    assistant = create_assistant()
    
    # 交互循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n你: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n再见！")
                break
            
            # 跳过空输入
            if not user_input:
                continue
            
            # 调用Agent
            response = assistant.invoke({"input": user_input})
            
            # 显示回复
            print(f"\n助手: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n抱歉，出现错误: {str(e)}")
            print("请重试或输入 'quit' 退出。")


if __name__ == "__main__":
    main()
