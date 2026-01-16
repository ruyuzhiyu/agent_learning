import os
import sys
from openai import OpenAI

# 设置控制台编码为 UTF-8，解决 Windows 下 emoji 显示问题
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    # 对于 input() 函数，需要设置环境变量
    os.environ["PYTHONIOENCODING"] = "utf-8"

# 假设你已经配置了环境变量，或者直接在这里填入(仅测试用)
# os.environ["OPENAI_API_KEY"] = "sk-..." 

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-773a8f5edf5344b78d45df54595d1aef"),  # 优先从环境变量读取，否则使用默认值
    base_url = "https://api.deepseek.com/v1"
)

def chat_loop():
    print("🤖 Bot: 你好！我是你的 AI 助手。输入 'exit' 退出。")
    
    # 打开日志文件，'a'表示追加模式，buffer=1表示行缓冲(实时写入)
    with open("logs.txt", "a", encoding="utf-8", buffering=1) as log_file:
        while True:
            user_input = input("\n👤 User: ")
            if user_input.lower() == 'exit':
                break
            
            # 记录用户问题
            log_file.write(f"User: {user_input}\n")
            
            print("🤖 Bot: ", end="", flush=True)
            log_file.write("Bot: ")
            
            # 调用 API (流式输出)
            stream = client.chat.completions.create(
                model="deepseek-chat", # 或 gpt-4
                messages=[
                    {"role": "system", "content": "你是一个傲娇毒舌的十七岁阳光少年，说话精准，不拖泥带水！惜字如金，每句话末尾都加个喵"},
                    {"role": "user", "content": user_input},
                ],
                stream=True,
            )
            
            response_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True) # 屏幕显示
                    response_text += content
            
            print() # 换行
            # 记录完整回答
            log_file.write(f"{response_text}\n")
            log_file.write("-" * 20 + "\n")

if __name__ == "__main__":
    chat_loop()