"""Tests for helper functions for authenticating to google APIs found in src/common/google_api_helpers.py"""

from src.common.google_api_helpers import get_google_creds


def test_get_google_creds() -> None:
    """
    Test the get_google_creds() function.

    :return: None
    """
    get_google_creds()
