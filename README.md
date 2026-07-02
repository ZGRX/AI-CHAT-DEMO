# AI Chat Demo

这是一个学习用的小型 AI 聊天 Demo，用来练习如何在 Python 项目里调用大模型 API，并把它接到一个简单 Web 页面上。

主要目标是跑通这些基础能力：

- 用 Python 调用大模型聊天接口
- 使用 `messages` 传入 `system` / `user` / `assistant` 消息
- 从返回结果里取出模型回复
- 用环境变量管理 API Key，避免把密钥写进代码或上传到 GitHub
- 做一个 FastAPI 后端接口
- 做一个简单网页，通过浏览器向后端发送问题并显示回答
- 在命令行版本里体验流式输出

## 项目结构

```text
.
├── chat.py              # 命令行多轮聊天版本
├── chat_stream.py       # 命令行流式输出版本
├── main.py              # FastAPI Web 后端
├── static/
│   ├── index.html       # Web 页面结构
│   ├── app.js           # 前端请求 /chat 接口
│   └── style.css        # 页面样式
├── .gitignore
└── README.md
```

## 环境变量

项目通过环境变量读取 API 配置：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

如果使用兼容 OpenAI 格式的其他模型服务，可以把 `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 改成对应平台的值。

注意：不要把真实的 `.env` 文件提交到 GitHub。

## 安装依赖

建议使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv fastapi uvicorn
```

## 运行命令行版本

普通多轮对话：

```bash
python chat.py
```

命令行流式输出：

```bash
python chat_stream.py
```

输入：

```text
exit
```

可以退出程序。

## 运行 Web Demo

启动 FastAPI 后端：

```bash
uvicorn main:app --reload
```

然后在浏览器打开：

```text
http://127.0.0.1:8000
```

也可以访问 FastAPI 自动生成的接口文档：

```text
http://127.0.0.1:8000/docs
```

## 当前状态

这个 Demo 已经实现了基础 Web 聊天：

```text
浏览器输入问题
  -> FastAPI 后端收到请求
  -> 后端调用大模型 API
  -> 后端返回回答
  -> 浏览器显示回答
```

目前还没有实现前端页面的 SSE 流式输出。也就是说，网页会等后端拿到完整回答后再一次性显示。后续可以继续改成 `StreamingResponse` 或 SSE/fetch stream，让浏览器边收到边显示。

## 安全提醒

- `.env` 里可能有真实 API Key，不能提交。
- `.venv/` 是本地虚拟环境，不能提交。
- 输入 token 和输出 token 都可能计费，测试时注意控制 `max_tokens`。
