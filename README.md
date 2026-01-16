# AI Agent 14天速成学习计划

基于Boss直聘AI Agent岗位要求设计的系统化学习计划，帮助你快速掌握AI Agent开发技能。

## 📚 项目简介

本项目提供完整的14天AI Agent学习路径，包括：
- 详细的每日学习计划
- 配套的代码示例
- 实战项目模板
- 丰富的学习资源

## 🎯 学习目标

- 掌握大模型API使用和Prompt Engineering
- 熟练使用LangChain等主流框架
- 理解Agent的核心概念和架构设计
- 具备开发实际AI Agent应用的能力

## 📖 学习计划

详细学习计划请查看：[学习计划.md](./学习计划.md)

### 第一周：基础理论与环境搭建
- Day 1: AI Agent概述
- Day 2: 大模型基础
- Day 3: LangChain入门
- Day 4: Memory机制
- Day 5: Tools和Function Calling
- Day 6: Agent架构设计
- Day 7: 第一周总结与项目

### 第二周：进阶应用与实战
- Day 8: 多Agent系统
- Day 9: RAG进阶
- Day 10: Agent安全与可靠性
- Day 11: 性能优化
- Day 12: 生产级部署
- Day 13: 行业应用案例
- Day 14: 毕业项目

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/ruyuzhiyu/agent_learning.git
cd agent_learning
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

### 4. 运行示例代码
```bash
# Day 2示例：大模型基础
python examples/day02_llm_basics.py

# Day 3示例：LangChain入门
python examples/day03_langchain_intro.py

# 其他示例...
```

## 📁 项目结构

```
agent_learning/
├── 学习计划.md          # 详细的14天学习计划
├── RESOURCES.md         # 学习资源汇总
├── README.md            # 项目说明
├── requirements.txt     # Python依赖
├── .env.example         # 环境变量示例
├── examples/            # 每日代码示例
│   ├── day02_llm_basics.py
│   ├── day03_langchain_intro.py
│   ├── day04_memory_systems.py
│   ├── day05_tools_functions.py
│   ├── day06_agent_patterns.py
│   └── ...
└── projects/            # 实战项目
    ├── week1_personal_assistant/
    └── industry_cases/
```

## 💡 学习建议

1. **循序渐进**：按照Day 1-14的顺序学习，不要跳过基础部分
2. **动手实践**：每天完成代码练习，理论结合实践
3. **记录总结**：建立学习笔记，记录问题和心得
4. **社区交流**：遇到问题及时查找资料或求助社区
5. **项目驱动**：尽快开始自己的小项目，学以致用

## 🔧 环境要求

- Python 3.8+
- OpenAI/Anthropic/Google API密钥（至少一个）
- 基本的Python编程知识
- 了解基本的命令行操作

## 📚 学习资源

详细资源列表请查看：[RESOURCES.md](./RESOURCES.md)

### 推荐框架
- [LangChain](https://python.langchain.com/)
- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://www.crewai.io/)

### API服务
- [OpenAI](https://platform.openai.com/)
- [Anthropic Claude](https://www.anthropic.com/)
- [Google Gemini](https://ai.google.dev/)

## ⚠️ 注意事项

- API调用需要付费，建议先使用免费额度测试
- 代码示例仅供学习参考，生产环境需要更多优化
- 保护好API密钥，不要提交到公开仓库

## 🤝 贡献

欢迎提交Issue和Pull Request来改进本项目！

## 📄 License

MIT License

## 📧 联系方式

如有问题或建议，欢迎提Issue讨论。

---

**祝学习顺利！坚持14天，成为AI Agent开发者！** 🚀
