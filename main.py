from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI(title="AJ Core")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AJ Core</title>
<style>
body { font-family: 'Segoe UI', sans-serif; background: #0F172A; color: #E2E8F0; margin: 0; padding: 20px; display: flex; justify-content: center; }
.container { max-width: 700px; width: 100%; background: #1E293B; padding: 25px; border-radius: 16px; }
h1 { text-align: center; color: #3B82F6; }
#chat { height: 400px; overflow-y: auto; border: 1px solid #334155; padding: 15px; border-radius: 10px; margin-bottom: 15px; background: #0F172A; }
.msg { padding: 10px; margin: 10px 0; border-radius: 8px; max-width: 80%; }
.user { background: #3B82F6; color: white; margin-left: auto; text-align: right; }
.bot { background: #334155; color: #E2E8F0; margin-right: auto; }
.input-area { display: flex; gap: 10px; }
input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0F172A; color: #E2E8F0; }
button { padding: 12px 20px; border-radius: 8px; border: none; background: #3B82F6; color: white; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>
<div class="container">
<h1>👑 AJ Core</h1>
<div id="chat"></div>
<div class="input-area">
<input id="msg" placeholder="Ask AJ Core anything..." onkeypress="if(event.key==='Enter') sendMsg()">
<button onclick="sendMsg()">Send</button>
</div>
</div>
<script>
const chat = document.getElementById('chat');
function addMsg(text, sender) {
const div = document.createElement('div');
div.className = 'msg ' + sender;
div.innerText = text;
chat.appendChild(div);
chat.scrollTop = chat.scrollHeight;
}
async function sendMsg() {
const input = document.getElementById('msg');
const text = input.value.trim();
if(!text) return;
addMsg(text, 'user');
input.value = '';
try {
const res = await fetch('/chat', {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({message: text})
});
const data = await res.json();
addMsg(data.reply, 'bot');
} catch(e) {
addMsg('Error: Could not reach AJ Core', 'bot');
}
}
addMsg('Hello! I am AJ Core. How can I help you today?', 'bot');
</script>
</div>
</body>
</html>
"""

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return HTML_CODE

@app.post("/chat")
async def chat(msg: Message):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": msg.message}]
    )
    return {"reply": response.choices[0].message.content}
