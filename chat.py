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
    {"role": "system", "content": "你是一个简洁、耐心的中文助手。"},
    {"role": "user", "content": "请用一句话解释什么是 API。"},
]

try:
    #用 client 这个 OpenAI 客户端，进入“聊天”功能，使用“补全/生成回复”接口，创建一次请求。
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )
    #choices 是“候选回答列表”
    #这个 message 通常包含：role和content
    answer = response.choices[0].message.content
    print(answer)

except Exception as e:
    print("调用 API 失败：")
    print(e)