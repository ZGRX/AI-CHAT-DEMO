const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");

function addMessage(role, content) {
    const message = document.createElement("div");
    message.className = `message ${role}`;
    message.textContent = content;
    messages.appendChild(message);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const userText = input.value.trim();

    if (!userText) {
        return;
    }

    addMessage("user", `你：${userText}`);
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: userText,
            }),
        });

        const data = await response.json();

        addMessage("assistant", `AI：${data.answer}`);
    } catch (error) {
        addMessage("error", "请求失败，请检查后端服务。");
    }
});