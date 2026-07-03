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

    if (button.disabled) {
        return;
    }

    const userText = input.value.trim();

    if (!userText) {
        return;
    }

    const task = taskSelect.value;

    addMessage("user", `你：${userText}`);
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

        const response = await fetch("/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }

        addMessage("assistant", `AI：${data.answer}`);

        history.push({
            role: "assistant",
            content: data.answer,
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
