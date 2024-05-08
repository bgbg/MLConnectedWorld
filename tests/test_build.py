import os
import pytest
import subprocess

from .fixtures import project_dir, book_dir


def test_build(project_dir, book_dir):
    """Test that jupyter-book build MLConnectedWorldBook works."""
    # Run the jupyter-book build command
    result = subprocess.run(
        ["jupyter-book", "build", book_dir], capture_output=True, text=True
    )
    assert result.returncode == 0, f"Build failed with error: {result.stderr}"
    build_path = os.path.join(book_dir, "_build")
    assert os.path.exists(
        build_path
    ), f"The build directory {build_path} does not exist."

    index_html = os.path.join(build_path, "html", "index.html")
    assert os.path.exists(index_html), f"index.html does not exist in {build_path}"

    print(result.stdout)  # Print the output of the build command for debugging
