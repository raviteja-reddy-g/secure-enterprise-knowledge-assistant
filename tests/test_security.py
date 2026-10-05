import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.security import (
    _keys_match,
    require_admin,
    require_reader,
)


class TestSecurity(unittest.TestCase):

    def test_matching_keys(self):
        self.assertTrue(
            _keys_match("reader-secret", "reader-secret")
        )

    def test_non_matching_keys(self):
        self.assertFalse(
            _keys_match("wrong-key", "reader-secret")
        )

    def test_missing_expected_key(self):
        self.assertFalse(
            _keys_match("reader-secret", None)
        )

    @patch(
        "app.security.READER_API_KEY",
        "reader-secret"
    )
    @patch(
        "app.security.ADMIN_API_KEY",
        "admin-secret"
    )
    def test_reader_key_is_allowed(self):
        self.assertTrue(
            require_reader("reader-secret")
        )

    @patch(
        "app.security.READER_API_KEY",
        "reader-secret"
    )
    @patch(
        "app.security.ADMIN_API_KEY",
        "admin-secret"
    )
    def test_admin_key_can_read(self):
        self.assertTrue(
            require_reader("admin-secret")
        )

    @patch(
        "app.security.ADMIN_API_KEY",
        "admin-secret"
    )
    def test_admin_key_is_allowed(self):
        self.assertTrue(
            require_admin("admin-secret")
        )

    @patch(
        "app.security.ADMIN_API_KEY",
        "admin-secret"
    )
    def test_invalid_admin_key_is_rejected(self):
        with self.assertRaises(HTTPException) as context:
            require_admin("wrong-key")

        self.assertEqual(
            context.exception.status_code,
            403
        )


if name == "main":
    unittest.main()
