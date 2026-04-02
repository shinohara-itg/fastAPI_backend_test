import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not API_KEY:
    raise ValueError("AZURE_OPENAI_API_KEY is not set")

if not ENDPOINT:
    raise ValueError("AZURE_OPENAI_ENDPOINT is not set")

if not DEPLOYMENT_NAME:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT is not set")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://purple-sand-003dc1600.1.azurestaticapps.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=API_KEY,
    base_url=f"{ENDPOINT}/openai/v1/",
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    print("chat endpoint called")
    print(f"user message: {req.message}")

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "あなたは簡潔で親切なアシスタントです。"
                },
                {
                    "role": "user",
                    "content": req.message
                }
            ],
            temperature=0.7,
        )

        answer = response.choices[0].message.content
        print("azure openai success")

        return {"reply": answer}

    except Exception as e:
        print(f"azure openai error: {str(e)}")
        return {"reply": f"エラーが発生しました: {str(e)}"}