from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Question to ask the enterprise knowledge base"
    )


class AnswerResponse(BaseModel):
    question: str
    answer: str
