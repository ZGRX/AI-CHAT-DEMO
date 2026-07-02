import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    timeout=15.0,
)

model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

#客户端发来的 JSON 里必须有一个 message 字段，而且它是字符串
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    start = time.perf_counter()
    print("收到前端问题：", request.message)

    messages = [
        {"role": "system", "content": "你是一个简洁、耐心的中文助手。"},
        {"role": "user", "content": request.message},
    ]

    print("开始调用模型")
#前端仍然是等后端拼完整个 answer后才显示，网页体验不是真正流式。Web 流式要后面做 SSE。
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=300,
        stream=True,
    )
    answer = ""
    for chunk in stream:
        text_piece = chunk.choices[0].delta.content
        if text_piece:
            answer += text_piece        
    

    after_api = time.perf_counter()
    print(f"模型返回了，模型耗时：{after_api - start:.2f} 秒")

    end = time.perf_counter()
    print(f"后端总耗时：{end - start:.2f} 秒")

    return {"answer": answer}