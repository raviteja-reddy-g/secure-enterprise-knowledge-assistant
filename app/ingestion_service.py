from app.document_processor import split_document
from app.s3_loader import list_documents, load_document
from app.vector_store import create_vector_store, save_vector_store


def ingest_documents():
    """Load documents from S3 and build the local vector store."""

    document_keys = list_documents()

    if not document_keys:
        raise ValueError(
            "No supported documents were found in the S3 bucket."
        )

    all_chunks = []

    for key in document_keys:
        document_text = load_document(key)

        chunks = split_document(document_text)

        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError(
            "No document chunks were created."
        )

    vector_store = create_vector_store(all_chunks)

    save_vector_store(vector_store)

    return {
        "documents_processed": len(document_keys),
        "chunks_created": len(all_chunks),
    }
