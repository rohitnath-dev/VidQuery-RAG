from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import YouTubeRAG


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    youtube_url: str
    api_key: str
    question: str


@app.get("/")
def home():

    return {
        "message": "YouTube RAG API is running"
    }


@app.post("/chat")
def chat(data: ChatRequest):

    try:

        rag = YouTubeRAG(
            youtube_url=data.youtube_url,
            api_key=data.api_key
        )

        answer = rag.ask(data.question)

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
  }
