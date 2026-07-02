# AI Chat Demo

这是一个学习用的小型 AI 聊天机器人 Demo，用来练习如何在 Python 项目里调用大模型 API，并把模型能力接到一个简单 Web 页面上。

这个项目对应阶段一的“最低要求项目”：前端输入问题，后端调用大模型 API，然后把模型回答返回给页面。

## 已实现功能

- 前端输入问题
- 后端通过 FastAPI 提供 `/chat` 接口
- 后端调用兼容 OpenAI 格式的大模型 API
- 支持基础 `system` Prompt
- 使用 `messages` 组织对话内容
- 从模型返回结果中取出回答并展示
- API Key 通过环境变量读取，不写死在代码里
- 命令行版本支持多轮对话
- 命令行版本支持流式输出

## 技术栈

```text
前端：HTML / CSS / JavaScript
后端：Python FastAPI
模型：OpenAI 或兼容 OpenAI API 格式的模型服务
```

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

如果使用 DeepSeek、通义、Kimi 等兼容 OpenAI API 格式的模型服务，可以把 `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 改成对应平台的值。

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

输入下面内容可以退出程序：

```text
exit
```

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

## Web 调用流程

```text
浏览器输入问题
  -> 前端通过 fetch 请求 /chat
  -> FastAPI 后端收到请求
  -> 后端构造 messages
  -> 后端调用大模型 API
  -> 后端返回模型回答
  -> 浏览器显示回答
```

## 当前限制

- 前端页面还没有实现 SSE 流式输出。
- Web 版会等后端拿到完整回答后再一次性显示。
- 目前只有基础聊天功能，还没有做总结、翻译、代码解释等文本处理功能。
- Prompt 还写在后端代码里，没有拆成独立模板文件。
- 模型调用逻辑还没有单独封装成 `llm.py`。

后续可以继续升级成 AI 文本处理工具，例如增加文本总结、中英翻译、代码解释、周报生成等功能。

## 安全提醒

- `.env` 里可能有真实 API Key，不能提交。
- `.venv/` 是本地虚拟环境，不能提交。
- 输入 token 和输出 token 都可能计费，测试时注意控制 `max_tokens`。
