"""Tests for helper functions for authenticating to google APIs found in src/common/google_api_helpers.py"""

import os
from pathlib import Path

from src.common.google_api_helpers import (
    get_google_creds,
    get_path_to_google_creds
)


def test_get_path_to_google_creds() -> None:
    """
    Use pathlib to get path to google creds.

    :return: a pathlib.Path object
    """
    actual = get_path_to_google_creds()
    relative_path = Path(__file__).parent.parent.parent
    expected = Path(os.path.join(relative_path, "google_creds/client_secret.json"))
    assert actual == expected


def test_get_google_creds() -> None:
    """
    Test the get_google_creds() function.

    :return: None
    """
    get_google_creds()
