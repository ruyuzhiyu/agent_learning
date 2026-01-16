"""
环境测试脚本
用于验证开发环境是否正确配置
"""

import sys


def test_python_version():
    """测试Python版本"""
    print("="*60)
    print("测试1: Python版本")
    print("="*60)
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python版本符合要求 (>= 3.8)")
        return True
    else:
        print("✗ Python版本过低，需要 Python 3.8+")
        return False


def test_dependencies():
    """测试依赖包"""
    print("\n" + "="*60)
    print("测试2: 依赖包")
    print("="*60)
    
    required_packages = [
        'langchain',
        'openai',
        'pydantic',
    ]
    
    all_ok = True
    
    for package in required_packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {package}: {version}")
        except ImportError:
            print(f"✗ {package}: 未安装")
            all_ok = False
    
    return all_ok


def test_env_config():
    """测试环境变量配置"""
    print("\n" + "="*60)
    print("测试3: 环境变量")
    print("="*60)
    
    import os
    from dotenv import load_dotenv
    
    # 尝试加载.env文件
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        # 只显示前几个字符
        masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 20 else "***"
        print(f"✓ OPENAI_API_KEY: {masked_key}")
        return True
    else:
        print("✗ OPENAI_API_KEY: 未设置")
        print("  请在.env文件中配置API密钥")
        return False


def test_simple_llm_call():
    """测试简单的LLM调用"""
    print("\n" + "="*60)
    print("测试4: LLM API调用（可选）")
    print("="*60)
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⊘ 跳过（未配置API密钥）")
        return None
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key,
            max_tokens=50
        )
        
        print("正在测试API调用...")
        response = llm.invoke("Say 'Hello, AI Agent!' in Chinese")
        print(f"✓ API调用成功")
        print(f"  响应: {response.content}")
        return True
        
    except Exception as e:
        print(f"✗ API调用失败: {str(e)}")
        print("  可能的原因：")
        print("  - API密钥不正确")
        print("  - 网络连接问题")
        print("  - API配额不足")
        return False


def main():
    """主函数"""
    print("\n" + "🔧 AI Agent学习环境测试" + "\n")
    
    results = []
    
    # 运行测试
    results.append(("Python版本", test_python_version()))
    results.append(("依赖包", test_dependencies()))
    results.append(("环境变量", test_env_config()))
    
    # API测试（可选）
    api_result = test_simple_llm_call()
    if api_result is not None:
        results.append(("API调用", api_result))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    # 判断是否可以开始学习
    critical_tests = results[:3]  # 前3个测试是必需的
    all_critical_pass = all(r[1] for r in critical_tests)
    
    print("\n" + "="*60)
    if all_critical_pass:
        print("🎉 环境配置完成！可以开始学习了！")
        print("\n下一步：")
        print("1. 阅读 学习计划.md")
        print("2. 运行示例: python examples/day02_llm_basics.py")
        print("3. 开始Day 1的学习")
    else:
        print("⚠️  环境配置不完整")
        print("\n请先完成：")
        if not results[0][1]:
            print("- 升级Python到3.8+版本")
        if not results[1][1]:
            print("- 安装依赖: pip install -r requirements.txt")
        if not results[2][1]:
            print("- 配置API密钥: cp .env.example .env 并编辑.env文件")
    
    print("="*60 + "\n")
    
    return all_critical_pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
