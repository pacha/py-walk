import pytest

from gitignore_match import walk


@pytest.fixture(scope="session")
def all_paths(fixtures_path):
    def get_all_children(path):
        for child in path.iterdir():
            yield from get_all_children_rec(child)

    def get_all_children_rec(path):
        if path.is_dir():
            for child in path.iterdir():
                yield from get_all_children_rec(child)
        yield path

    tree = fixtures_path / "file-trees" / "dir1"
    all_paths = sorted([str(path) for path in get_all_children(tree)])
    return all_paths


def test_walk_no_filters(fixtures_path, all_paths):
    """Test no filters."""
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = sorted([str(path) for path in walk(tree)])
    assert walked_paths == all_paths


def test_walk_exclude(fixtures_path, all_paths):
    """Test exclude filter."""
    tree = fixtures_path / "file-trees" / "dir1"
    expected_paths = [path_str for path_str in all_paths if ".txt" not in path_str]
    walked_paths = sorted([str(path) for path in walk(tree, exclude="*.txt")])
    assert walked_paths == expected_paths


def test_walk_include(fixtures_path, all_paths):
    """Test include filter."""
    tree = fixtures_path / "file-trees" / "dir1"
    expected_paths = [
        path_str for path_str in all_paths if "dir2" in path_str or "dir5" in path_str
    ]
    walked_paths = sorted([str(path) for path in walk(tree, include="dir[25]")])
    assert walked_paths == expected_paths
