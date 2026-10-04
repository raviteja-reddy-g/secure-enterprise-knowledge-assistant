from langchain_aws import ChatBedrockConverse

from app.config import (
    AWS_REGION,
    BEDROCK_MODEL_ID,
    TOP_K_RESULTS,
)

from app.vector_store import load_vector_store


def get_llm():
    """Create the Amazon Bedrock chat model."""

    if not BEDROCK_MODEL_ID:
        raise ValueError(
            "BEDROCK_MODEL_ID is not configured."
        )

    return ChatBedrockConverse(
        model_id=BEDROCK_MODEL_ID,
        region_name=AWS_REGION,
        temperature=0
    )


def retrieve_context(question: str) -> str:
    """Retrieve the most relevant document chunks."""

    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=TOP_K_RESULTS
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context


def answer_question(question: str) -> str:
    """Answer a user question using retrieved enterprise context."""

    context = retrieve_context(question)

    if not context.strip():
        return (
            "I could not find enough information "
            "in the enterprise knowledge base."
        )

    prompt = f"""
You are a secure enterprise knowledge assistant.

Answer the user's question using only the
provided enterprise context.

If the answer is not supported by the context,
say that you do not have enough information.

Do not invent information.

Enterprise Context:
{context}

User Question:
{question}
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content
