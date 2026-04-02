import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

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
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT')}/openai/v1/",
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "backend is running"}


@app.post("/chat")
def chat(req: ChatRequest):
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

        return {"reply": answer}

    except Exception as e:
        return {"reply": f"エラーが発生しました: {str(e)}"}