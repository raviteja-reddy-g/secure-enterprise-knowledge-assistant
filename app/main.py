from fastapi import Depends, FastAPI, HTTPException

from app.ingestion_service import ingest_documents
from app.models import AnswerResponse, QuestionRequest
from app.rag_service import answer_question
from app.security import require_admin, require_reader


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


@app.post(
    "/ask",
    response_model=AnswerResponse,
    dependencies=[Depends(require_reader)]
)
def ask_question(request: QuestionRequest):
    try:
        answer = answer_question(request.question)

        return AnswerResponse(
            question=request.question,
            answer=answer
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the question."
        )


@app.post(
    "/admin/ingest",
    dependencies=[Depends(require_admin)]
)
def ingest_knowledge_base():
    try:
        return ingest_documents()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to ingest documents."
        )
