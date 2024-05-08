import os

import pytest


@pytest.fixture
def project_dir():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(this_dir, "..")
    return os.path.abspath(project_dir)


@pytest.fixture
def book_dir(project_dir):
    book_dir = os.path.join(project_dir, "MLConnectedWorldBook")
    book_dir = os.path.abspath(book_dir)
    return book_dir
