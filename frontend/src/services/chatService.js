// frontend/src/services/chatService.js
export const sendMessage = async (message, onChunk) => {
  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) throw new Error("Network response not ok");

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let fullReply = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      // ✅ Split by lines since Ollama sends JSONL
      const lines = chunk.split("\n").filter((line) => line.trim() !== "");
      for (const line of lines) {
        try {
          const data = JSON.parse(line);
          if (data.response) {
            fullReply += data.response;
            if (onChunk) onChunk(fullReply);
          }
        } catch (err) {
          // ignore incomplete chunks
        }
      }
    }

    return fullReply.trim() || "⚠️ No reply.";
  } catch (err) {
    console.error("Chat streaming error:", err);
    return "⚠️ Connection error.";
  }
};