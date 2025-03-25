import pytest
import os


@pytest.fixture(scope="session")
def directory() -> str:
    """Return the root directory of the project"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
