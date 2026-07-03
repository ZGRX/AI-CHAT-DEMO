from llm import call_llm
from prompts import PROMPTS
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

#客户端发来的 JSON 里必须有一个 message 字段，而且它是字符串
class Message(BaseModel):
    role: str
    content: str


class ProcessRequest(BaseModel):
    task: str
    text: str = ""
    messages: list[Message] | None = None

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/process")
def process(request: ProcessRequest):
    system_prompt = PROMPTS.get(request.task)
    if system_prompt is None:
        return {"error": "不支持的任务类型"}

    model_messages = [
        {"role": "system", "content": system_prompt},
    ]

    if request.messages:
        model_messages.extend(message.model_dump() for message in request.messages)
    else:
        model_messages.append({"role": "user", "content": request.text})

    answer = call_llm(model_messages)
    return {"answer": answer}
