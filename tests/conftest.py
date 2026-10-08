"""Pytest configuration and global test fixtures."""

import pytest

from training_nomination.db.session import init_db


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    """Initialize test database tables and seed baseline accounts before running tests."""
    init_db()
