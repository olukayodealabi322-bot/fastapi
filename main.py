from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AJ Core API")

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"status": "AJ Core is LIVE 🚀"}

@app.post("/chat")
def chat(q: Question):
    user_question = q.question.lower()
    
    if "hello" in user_question:
        answer = "Hello! I'm AJ Core. How can I help you?"
    elif "your name" in user_question:
        answer = "I'm AJ Core, your FastAPI assistant 🚀"
    elif "bye" in user_question:
        answer = "Goodbye! Come back anytime."
    else:
        answer = f"I got your question: '{q.question}'. I'm still learning to answer better 😅"
    
    return {"question": q.question, "answer": answer}
