const form = document.getElementById("chat-form");
const taskSelect = document.getElementById("task-select");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const button = form.querySelector("button");
const history = [];

function addMessage(role, content) {
    const message = document.createElement("div");
    message.className = `message ${role}`;
    message.textContent = content;
    messages.appendChild(message);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    //如果按钮已经禁用了，说明上一条消息还没发送完，直接退出，防止重复发送。
    if (button.disabled) {
        return;
    }
    //trim() 会去掉前后的空格。
    const userText = input.value.trim();

    if (!userText) {
        return;
    }

    const task = taskSelect.value;

    addMessage("user", `YOU：${userText}`);
    input.value = "";
    button.disabled = true;
    button.textContent = "发送中";
    input.disabled = true;
    taskSelect.disabled = true;

    try {
        history.push({
            role: "user",
            content: userText,
        });

        const requestBody = {
            task: task,
            messages: history,
        };
        //流式输出
        const response = await fetch("/process-stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok || !response.body) {
            throw new Error(`HTTP ${response.status}`);
        }

        const assistantMessage = document.createElement("div");
        assistantMessage.className = "message assistant";
        assistantMessage.textContent = "AI：";
        messages.appendChild(assistantMessage);

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let assistantText = "";
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(value, { stream: true });

            const events = buffer.split("\n\n");
            buffer = events.pop();

            for (const eventText of events) {
                const line = eventText
                    .split("\n")
                    .find((line) => line.startsWith("data: "));

                if (!line) {
                    continue;
                }

                const data = JSON.parse(line.slice(6));

                if (data.done) {
                    continue;
                }

                if (data.delta) {
                    assistantText += data.delta;
                    assistantMessage.textContent = `AI：${assistantText}`;
                }
            }
        }

        history.push({
            role: "assistant",
            content: assistantText,
        });
    } catch (error) {
        history.pop();
        addMessage("error", `请求失败：${error.message}`);
    } finally {
        button.disabled = false;
        button.textContent = "发送";
        input.disabled = false;
        taskSelect.disabled = false;
        input.focus();
    }

});
