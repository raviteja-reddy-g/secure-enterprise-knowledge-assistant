import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """Clean unnecessary whitespace from document text."""

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_document(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
):
    """Split a document into smaller chunks for retrieval."""

    cleaned_text = clean_text(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(cleaned_text)

    return chunks
