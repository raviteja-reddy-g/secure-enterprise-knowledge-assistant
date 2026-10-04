from typing import List

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import VECTOR_STORE_PATH


def get_embedding_model():
    """Create the embedding model used for semantic search."""

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks: List[str]):
    """Create a FAISS vector store from document chunks."""

    if not chunks:
        raise ValueError("No document chunks were provided.")

    embeddings = get_embedding_model()

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vector_store


def save_vector_store(vector_store):
    """Save the FAISS index locally."""

    vector_store.save_local(VECTOR_STORE_PATH)


def load_vector_store():
    """Load an existing FAISS vector store."""

    embeddings = get_embedding_model()

    return FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
