from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "AJ Core is LIVE 🚀"}

@app.get("/health")
def health():
    return {"ok": True}
