import json
import os
import pytest
from .fixtures import project_dir, book_dir


@pytest.fixture
def figure_dir(book_dir):
    return os.path.join(book_dir, "figures")


@pytest.fixture
def data_dir(book_dir):
    return os.path.join(book_dir, "data")


@pytest.fixture
def credit_file(project_dir):
    return os.path.join(project_dir, "data_credits.json")


def test_every_figure_has_a_credit(figure_dir, credit_file):
    figure_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    image_files = {
        f for f in os.listdir(figure_dir) if os.path.splitext(f)[1] in figure_extensions
    }
    image_credits = json.load(open(credit_file))["figures"]
    covered_image_files = {v["filename"] for v in image_credits.values()}
    missing_credits = set(image_files) - covered_image_files
    assert not missing_credits, f"Missing credits for {missing_credits}"


def test_every_datafile_has_a_credit(data_dir, credit_file):
    data_extensions = [".txt", ".csv", ".json", ".gz"]
    data_files = {
        f for f in os.listdir(data_dir) if os.path.splitext(f)[1] in data_extensions
    }
    data_credits = json.load(open(credit_file))["data"]
    covered_data_files = {v["filename"] for v in data_credits.values()}
    missing_credits = set(data_files) - covered_data_files
    assert not missing_credits, f"Missing credits for {missing_credits}"


def test_every_credit_has_a_figure(figure_dir, credit_file):
    figure_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    image_files = {
        f for f in os.listdir(figure_dir) if os.path.splitext(f)[1] in figure_extensions
    }
    image_credits = json.load(open(credit_file))["figures"]
    covered_image_files = {v["filename"] for v in image_credits.values()}
    extra_credits = covered_image_files - image_files
    assert not extra_credits, f"Extra credits for {extra_credits}"


def test_every_credit_has_a_datafile(data_dir, credit_file):
    data_extensions = [".txt", ".csv", ".json", ".gz"]
    data_files = {
        f for f in os.listdir(data_dir) if os.path.splitext(f)[1] in data_extensions
    }
    data_credits = json.load(open(credit_file))["data"]
    covered_data_files = {v["filename"] for v in data_credits.values()}
    extra_credits = covered_data_files - data_files
    assert not extra_credits, f"Extra credits for {extra_credits}"


def test_credit_has_correct_format(credit_file):
    required_fields = ["filename", "author", "description", "source", "url", "license"]
    credits = json.load(open(credit_file))
    bad_credits = dict()
    for scope, scope_credits in credits.items():
        curr_bad = {
            k: v
            for k, v in scope_credits.items()
            if not all(f in v for f in required_fields)
        }
        if curr_bad:
            bad_credits[scope] = curr_bad
    assert not bad_credits, f"Bad credits: {bad_credits}"
