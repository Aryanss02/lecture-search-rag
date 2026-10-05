from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import (
    retrieve_context,
    build_context,
    generate_answer,
    build_sources
)

app = FastAPI()

# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Lecture Search API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    query = request.question

    results = retrieve_context(query)

    context = build_context(results)

    answer = generate_answer(
        query,
        context
    )

    sources = build_sources(results)

    return {
        "question": query,
        "answer": answer,
        "sources": sources
    }