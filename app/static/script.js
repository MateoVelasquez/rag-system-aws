document.getElementById("sendButton").addEventListener("click", sendMessage);

async function sendMessage() {
    let message = document.getElementById("userInput").value;
    if (!message.trim()) return;

    let chatbox = document.getElementById("chatbox");
    let loading = document.getElementById("loading");

    let userMessage = `<p class="message user"><strong>You:</strong> ${message}</p>`;
    chatbox.innerHTML += userMessage;

    loading.style.display = "block";

    try {
        let response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "question": message })
        });

        if (!response.ok) {
            let errorText = await response.text();
            chatbox.innerHTML += `<p class="message error"><strong>Error:</strong> ${errorText}</p>`;
        } else {
            let data = await response.json();
            chatbox.innerHTML += `<div class="message bot"><strong>Bot:</strong> <div class="bot-message">${marked.parse(data.answer)}</div></div>`;
        }
    } catch (error) {
        chatbox.innerHTML += `<p class="message error"><strong>Error:</strong> No se pudo conectar con el servidor.</p>`;
    }

    loading.style.display = "none";
    chatbox.scrollTop = chatbox.scrollHeight;
    document.getElementById("userInput").value = "";
}

// Función para obtener la información del RAG
async function fetchRAGInfo() {
    try {
        let response = await fetch("/app_info");
        if (!response.ok) throw new Error("Error fetching RAG info");

        let data = await response.json();
        document.getElementById("rag-info").innerHTML = `
            <div class="rag-info-container">
                <p><strong>LLM Model:</strong> ${data.llm_model}</p>
                <p><strong>Developer:</strong> ${data.developer}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Project Link:</strong> https://github.com/MateoVelasquez/rag-system-aws</p>
            </div>
        `;
    } catch (error) {
        console.error("Error fetching RAG info:", error);
    }
}

// Llamar la función al cargar la página
document.addEventListener("DOMContentLoaded", fetchRAGInfo);
