from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AJ Core")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# THIS IS YOUR FRONTEND INSIDE THE BACKEND
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AJ Core</title>
<style>
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; display: flex; justify-content: center; }
  .container { max-width: 700px; width: 100%; background: #1e293b; padding: 25px; border-radius: 16px; box-shadow: 0 0 20px rgba(0,0,0,0.4); }
  h1 { text-align: center; color: #38bdf8; }
  #chat { height: 400px; overflow-y: auto; border: 1px solid #334155; padding: 15px; border-radius: 10px; margin-bottom: 15px; background: #0f172a; }
  .msg { margin: 8px 0; padding: 10px 14px; border-radius: 12px; max-width: 80%; }
  .user { background: #38bdf8; color: #0f172a; margin-left: auto; text-align: right; }
  .bot { background: #334155; color: #e2e8f0; margin-right: auto; }
  .input-area { display: flex; gap: 10px; }
  input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #e2e8f0; outline: none; }
  button { padding: 12px 20px; border-radius: 8px; border: none; background: #38bdf8; color: #0f172a; font-weight: bold; cursor: pointer; }
  button:hover { background: #0ea5e9; }
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
</body>
</html>
"""

# ROUTE 1: SERVE THE UI
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return HTML_CODE

# ROUTE 2: HANDLE CHAT
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    
    # THIS IS WHERE AJ CORE BRAIN GOES
    # For now it just echoes. Replace with your AI logic
    reply = f"AJ Core heard you: {user_msg}"
    
    return JSONResponse({"reply": reply})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
