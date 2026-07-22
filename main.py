from fastapi import FastAPI
import os

app = FastAPI(title="AJ Core")

@app.get("/")
def root():
    return {"status": "AJ Core is LIVE", "message": "Hello from AJ"}

@app.get("/health")
def health():
    return {
        "serpapi": "loaded" if os.getenv("SERPAPI_KEY") else "missing",
        "openai": "loaded" if os.getenv("OPENAI_KEY") else "missing",
        "gemini": "loaded" if os.getenv("GEMINI_KEY") else "missing"
    }
