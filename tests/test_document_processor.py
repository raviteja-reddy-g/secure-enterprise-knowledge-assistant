import unittest

from app.document_processor import clean_text, split_document


class TestDocumentProcessor(unittest.TestCase):

    def test_clean_text_removes_extra_whitespace(self):
        text = "Enterprise   knowledge\n\nassistant   project"

        result = clean_text(text)

        self.assertEqual(
            result,
            "Enterprise knowledge assistant project"
        )

    def test_clean_text_removes_leading_and_trailing_spaces(self):
        text = "   Secure enterprise AI   "

        result = clean_text(text)

        self.assertEqual(
            result,
            "Secure enterprise AI"
        )

    def test_split_document_returns_chunks(self):
        text = (
            "Enterprise knowledge systems help employees "
            "retrieve internal information efficiently. "
        ) * 20

        chunks = split_document(
            text,
            chunk_size=200,
            chunk_overlap=20
        )

        self.assertGreater(
            len(chunks),
            1
        )

    def test_split_document_preserves_content(self):
        text = (
            "Amazon S3 stores enterprise documents. "
            "FAISS provides semantic vector search."
        )

        chunks = split_document(
            text,
            chunk_size=100,
            chunk_overlap=10
        )

        combined_text = " ".join(chunks)

        self.assertIn(
            "Amazon S3",
            combined_text
        )

        self.assertIn(
            "FAISS",
            combined_text
        )
