from fastapi import FastAPI, HTTPException

from app.models import QuestionRequest, AnswerResponse
from app.rag_service import answer_question

app = FastAPI(
    title="Secure Enterprise Knowledge Assistant",
    description="Enterprise RAG knowledge assistant API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Secure Enterprise Knowledge Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    try:
        answer = answer_question(request.question)

        return AnswerResponse(
            question=request.question,
            answer=answer
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
