import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()#读取当前目录里的 .env
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_BASE_URL")
)

model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

messages = [
    {"role": "system", "content": "你是一个可爱的猫娘。"},
]
#加一个while True使之可以持续输出
while True:
    question = input("你：")
    
    if question == 'exit':
        break

    messages.append({"role":"user","content":question})

    try:
        #用 client 这个 OpenAI 客户端，进入“聊天”功能，使用“补全/生成回复”接口，创建一次请求。
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
            stream=True,
        )
        print("AI：", end="", flush=True)#正常情况下print输出会放在缓冲区，flush = True让马上显现
        answer = ""
        for chunk in stream:
            text_piece = chunk.choices[0].delta.content#delta 是流式返回时API/SDK对象里的字段名。

            if text_piece:
                print(text_piece, end="", flush=True)
                answer += text_piece

        print()

        messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        print("调用 API 失败：")
        print(e)
