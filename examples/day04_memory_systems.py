"""
Day 4: Memory机制示例代码
学习目标：理解Agent的记忆系统和RAG基础
"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.chains import ConversationChain
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# 初始化LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def buffer_memory_example():
    """
    ConversationBufferMemory示例
    保存完整的对话历史
    """
    print("ConversationBufferMemory示例：")
    
    # 创建记忆组件
    memory = ConversationBufferMemory()
    
    # 创建对话链
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True  # 显示提示词和记忆
    )
    
    # 进行多轮对话
    print("\n用户: 我叫张三")
    response1 = conversation.predict(input="我叫张三")
    print(f"AI: {response1}\n")
    
    print("用户: 我喜欢打篮球")
    response2 = conversation.predict(input="我喜欢打篮球")
    print(f"AI: {response2}\n")
    
    print("用户: 你还记得我的名字吗？")
    response3 = conversation.predict(input="你还记得我的名字吗？")
    print(f"AI: {response3}\n")
    
    # 查看记忆内容
    print("当前记忆内容:")
    print(memory.load_memory_variables({}))


def window_memory_example():
    """
    ConversationBufferWindowMemory示例
    只保留最近K轮对话
    """
    print("\nConversationBufferWindowMemory示例：")
    
    # 只保留最近2轮对话
    memory = ConversationBufferWindowMemory(k=2)
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # 进行多轮对话
    conversation.predict(input="我叫李四")
    conversation.predict(input="我住在北京")
    conversation.predict(input="我是程序员")
    
    # 这时应该只记得最近2轮
    response = conversation.predict(input="你还记得我的名字吗？")
    print(f"AI: {response}")
    print("(因为只保留2轮对话，可能不记得名字)")


def summary_memory_example():
    """
    ConversationSummaryMemory示例
    使用LLM总结历史对话
    """
    print("\nConversationSummaryMemory示例：")
    
    memory = ConversationSummaryMemory(llm=llm)
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # 进行对话
    conversation.predict(input="我在一家AI公司工作")
    conversation.predict(input="我们公司主要做智能客服")
    
    # 查看总结后的记忆
    print("\n总结后的记忆:")
    print(memory.load_memory_variables({}))


def vector_store_example():
    """
    向量数据库示例
    使用Chroma存储和检索文档
    """
    print("\n向量数据库示例：")
    
    # 准备一些文档
    texts = [
        "LangChain是一个用于开发LLM应用的框架。",
        "AI Agent可以自主完成任务，包括感知、推理和行动。",
        "RAG技术结合了检索和生成，提高了回答的准确性。",
        "向量数据库使用embedding进行语义检索。",
        "Prompt Engineering是设计提示词的艺术和科学。"
    ]
    
    # 创建embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # 创建向量数据库
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    # 语义检索
    query = "什么是RAG？"
    docs = vectorstore.similarity_search(query, k=2)
    
    print(f"\n查询: {query}")
    print("检索结果:")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.page_content}")


def simple_rag_example():
    """
    简单的RAG（检索增强生成）示例
    """
    print("\nRAG示例：")
    
    # 准备知识库
    knowledge_base = [
        "Python是一种高级编程语言，广泛用于数据科学和AI开发。",
        "LangChain提供了Memory、Chains、Agents等组件。",
        "向量数据库可以存储和检索高维向量，用于语义搜索。",
        "Embedding将文本转换为向量表示，捕捉语义信息。"
    ]
    
    # 创建向量数据库
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = Chroma.from_texts(
        texts=knowledge_base,
        embedding=embeddings
    )
    
    # 创建RAG链
    from langchain.chains import RetrievalQA
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True
    )
    
    # 提问
    question = "LangChain有哪些组件？"
    result = qa_chain({"query": question})
    
    print(f"\n问题: {question}")
    print(f"回答: {result['result']}")
    print("\n使用的源文档:")
    for doc in result['source_documents']:
        print(f"- {doc.page_content}")


def conversation_with_memory_and_rag():
    """
    结合对话记忆和RAG的示例
    """
    print("\n结合Memory和RAG的对话系统：")
    
    # 知识库
    knowledge = [
        "公司成立于2020年，专注于AI Agent开发。",
        "我们的产品包括智能客服、代码助手和数据分析工具。",
        "公司位于北京中关村，员工100人。"
    ]
    
    # 创建向量数据库
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = Chroma.from_texts(texts=knowledge, embedding=embeddings)
    
    # 创建带记忆的RAG链
    from langchain.chains import ConversationalRetrievalChain
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    
    # 多轮对话
    print("\n用户: 公司是什么时候成立的？")
    response1 = qa({"question": "公司是什么时候成立的？"})
    print(f"AI: {response1['answer']}\n")
    
    print("用户: 有多少员工？")
    response2 = qa({"question": "有多少员工？"})
    print(f"AI: {response2['answer']}\n")


if __name__ == "__main__":
    print("Day 4: Memory机制示例\n")
    print("="*60)
    
    # 示例1: Buffer Memory
    buffer_memory_example()
    
    print("\n" + "="*60)
    
    # 示例2: Window Memory
    window_memory_example()
    
    print("\n" + "="*60)
    
    # 示例3: 向量数据库
    vector_store_example()
    
    print("\n" + "="*60)
    
    # 示例4: RAG
    simple_rag_example()
    
    # 练习任务
    print("\n" + "="*60)
    print("练习任务：")
    print("="*60)
    print("1. 比较不同Memory类型的适用场景")
    print("2. 实现一个基于文档的问答系统")
    print("3. 优化RAG的检索效果（调整k值、chunk大小）")
    print("4. 结合Memory和RAG实现智能客服")
