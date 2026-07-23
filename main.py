from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI(title="AJ Core API")
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"status": "AJ Core is LIVE"}

@app.post("/chat")
def chat(q: Question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are AJ Core, a helpful AI assistant created by AJ."},
            {"role": "user", "content": q.question}
        ]
    )
    answer = response.choices[0].message.content
    return {"question": q.question, "answer": answer}
