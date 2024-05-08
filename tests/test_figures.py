import json
import os
import pytest
from .fixtures import project_dir, book_dir


@pytest.fixture
def figure_dir(book_dir):
    return os.path.join(book_dir, "figures")


@pytest.fixture
def image_credit_file(project_dir):
    return os.path.join(project_dir, "image_credits.json")


def test_every_figure_has_a_credit(figure_dir, image_credit_file):
    figure_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    image_files = {
        f for f in os.listdir(figure_dir) if os.path.splitext(f)[1] in figure_extensions
    }
    image_credits = json.load(open(image_credit_file))
    covered_image_files = {v["filename"] for v in image_credits.values()}
    missing_credits = set(image_files) - covered_image_files
    assert not missing_credits, f"Missing credits for {missing_credits}"


def test_every_credit_has_a_figure(figure_dir, image_credit_file):
    figure_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    image_files = {
        f for f in os.listdir(figure_dir) if os.path.splitext(f)[1] in figure_extensions
    }
    image_credits = json.load(open(image_credit_file))
    covered_image_files = {v["filename"] for v in image_credits.values()}
    extra_credits = covered_image_files - image_files
    assert not extra_credits, f"Extra credits for {extra_credits}"


def test_credit_has_correct_format(image_credit_file):
    required_fields = ["filename", "author", "description", "source", "url", "license"]
    image_credits = json.load(open(image_credit_file))
    bad_credits = {
        k: v
        for k, v in image_credits.items()
        if not all(f in v for f in required_fields)
    }
    assert not bad_credits, f"Bad credits for {bad_credits}"
