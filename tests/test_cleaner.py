import pytest
from unittest.mock import MagicMock, patch
from gitclean.cleaner import find_large_files
from rich.console import Console

console = Console()

@patch("gitclean.cleaner.Repo")
def test_find_large_files_no_results(mock_repo):
    """
    Test that the function outputs 'No large files' message when nothing exceeds threshold.
    """
    # Setup mock repo with fake commit and blob (size < threshold)
    fake_blob = MagicMock()
    fake_blob.type = "blob"
    fake_blob.size = 1024  # < 1KB
    fake_blob.path = "tiny_file.txt"

    fake_commit = MagicMock()
    fake_commit.tree.traverse.return_value = [fake_blob]
    mock_repo.return_value.iter_commits.return_value = [fake_commit]

    with console.capture() as capture:
        find_large_files(threshold_mb=1)

    output = capture.get()
    assert "No large files found" in output
