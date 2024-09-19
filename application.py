from fastapi import FastAPI, Depends, HTTPException
from transformers import pipeline
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# Simple API key authentication
API_KEY = "f2b77caf8c87de875317b4f18e2e71a1"
api_key_header = APIKeyHeader(name="Authorization")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return True

# HuggingFace BERT model
model = pipeline("fill-mask", model="bert-base-uncased")

@app.get("/predict/")
async def predict(text: str, authorized: bool = Depends(verify_api_key)):
    results = model(text)
    return results
