"""
Day 3: LangChain入门示例代码
学习目标：掌握LangChain的基本组件和使用方法
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 初始化LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def basic_prompt_template():
    """
    基础的PromptTemplate使用
    """
    # 创建提示词模板
    template = "给我讲一个关于{topic}的{style}故事"
    prompt = PromptTemplate(
        input_variables=["topic", "style"],
        template=template
    )
    
    # 格式化提示词
    formatted_prompt = prompt.format(topic="AI", style="科幻")
    print("格式化的提示词:", formatted_prompt)
    
    # 使用LLM生成回复
    response = llm.invoke(formatted_prompt)
    print("LLM回复:", response.content)


def chat_prompt_template_example():
    """
    ChatPromptTemplate示例
    用于构建多角色对话
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，用{language}回答问题。"),
        ("user", "{question}")
    ])
    
    # 格式化消息
    messages = prompt.format_messages(
        role="Python专家",
        language="简洁的中文",
        question="什么是列表推导式？"
    )
    
    response = llm.invoke(messages)
    print("回复:", response.content)


def simple_chain_example():
    """
    简单链（LLMChain）示例
    将提示词模板和LLM组合
    """
    # 创建提示词模板
    prompt = PromptTemplate(
        input_variables=["product"],
        template="为{product}写一句广告语"
    )
    
    # 创建链
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 运行链
    result = chain.run(product="智能手表")
    print("广告语:", result)


def sequential_chain_example():
    """
    顺序链示例
    将多个链串联起来
    """
    from langchain.chains import SimpleSequentialChain
    
    # 第一个链：生成故事大纲
    first_prompt = PromptTemplate(
        input_variables=["topic"],
        template="为{topic}写一个简短的故事大纲（3-5句话）"
    )
    first_chain = LLMChain(llm=llm, prompt=first_prompt)
    
    # 第二个链：给故事起名字
    second_prompt = PromptTemplate(
        input_variables=["outline"],
        template="根据以下故事大纲，起一个吸引人的标题：\n{outline}"
    )
    second_chain = LLMChain(llm=llm, prompt=second_prompt)
    
    # 组合成顺序链
    overall_chain = SimpleSequentialChain(
        chains=[first_chain, second_chain],
        verbose=True  # 显示中间步骤
    )
    
    result = overall_chain.run("太空探险")
    print("最终标题:", result)


# 定义输出数据模型
class MovieReview(BaseModel):
    """电影评论的结构化数据"""
    title: str = Field(description="电影名称")
    rating: float = Field(description="评分（0-10）")
    summary: str = Field(description="评论摘要")
    sentiment: str = Field(description="情感：positive/negative/neutral")


def output_parser_example():
    """
    输出解析器示例
    将LLM输出解析为结构化数据
    """
    # 创建解析器
    parser = PydanticOutputParser(pydantic_object=MovieReview)
    
    # 创建包含格式指令的提示词
    prompt = PromptTemplate(
        template="分析以下电影评论并提取信息：\n{review}\n\n{format_instructions}",
        input_variables=["review"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # 创建链
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 运行并解析
    review_text = "《流浪地球2》太震撼了！特效一流，剧情紧凑，给9分！"
    result = chain.run(review=review_text)
    
    print("原始输出:", result)
    
    # 解析为结构化对象
    parsed_result = parser.parse(result)
    print("\n解析后的结构化数据:")
    print(f"电影: {parsed_result.title}")
    print(f"评分: {parsed_result.rating}")
    print(f"摘要: {parsed_result.summary}")
    print(f"情感: {parsed_result.sentiment}")


def custom_chain_example():
    """
    自定义链示例
    实现一个代码生成和解释的链
    """
    from langchain.chains import TransformChain
    
    # 代码生成链
    code_prompt = PromptTemplate(
        input_variables=["task"],
        template="用Python写一个函数来完成：{task}\n只返回代码，不要解释。"
    )
    code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
    
    # 代码解释链
    explain_prompt = PromptTemplate(
        input_variables=["code"],
        template="解释以下Python代码的功能：\n```python\n{code}\n```"
    )
    explain_chain = LLMChain(llm=llm, prompt=explain_prompt, output_key="explanation")
    
    # 使用SequentialChain组合
    from langchain.chains import SequentialChain
    
    overall_chain = SequentialChain(
        chains=[code_chain, explain_chain],
        input_variables=["task"],
        output_variables=["code", "explanation"],
        verbose=True
    )
    
    result = overall_chain({"task": "计算斐波那契数列的第n项"})
    print("\n生成的代码:")
    print(result["code"])
    print("\n代码解释:")
    print(result["explanation"])


if __name__ == "__main__":
    print("Day 3: LangChain入门示例\n")
    
    # 示例1: 基础PromptTemplate
    print("="*50)
    print("示例1: PromptTemplate")
    print("="*50)
    basic_prompt_template()
    print()
    
    # 示例2: ChatPromptTemplate
    print("="*50)
    print("示例2: ChatPromptTemplate")
    print("="*50)
    chat_prompt_template_example()
    print()
    
    # 示例3: 简单链
    print("="*50)
    print("示例3: LLMChain")
    print("="*50)
    simple_chain_example()
    print()
    
    # 示例4: 输出解析器
    print("="*50)
    print("示例4: 输出解析器")
    print("="*50)
    output_parser_example()
    print()
    
    # 练习任务
    print("\n" + "="*50)
    print("练习任务：")
    print("="*50)
    print("1. 创建一个翻译链，支持多种语言")
    print("2. 实现一个问答链，结合上下文回答问题")
    print("3. 使用输出解析器提取文章的关键信息")
    print("4. 设计一个多步骤的内容生成链")
