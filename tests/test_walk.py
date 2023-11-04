from textwrap import dedent

from py_walk import walk
from py_walk.logs import log


def test_walk_all(fixtures_path):
    all_paths = [
        "dir2",
        "dir2/dir3",
        "dir2/dir3/bar.txt",
        "dir2/dir3/foo.png",
        "dir4",
        "dir4/bat.txt",
        "dir4/baz.txt",
        "dir5",
        "dir5/one.dat",
        "dir5/two.dat",
        "foo.txt",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree)
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == all_paths


def test_walk_ignore_dir(fixtures_path):
    paths = [
        "dir2",
        "dir4",
        "dir4/bat.txt",
        "dir4/baz.txt",
        "dir5",
        "dir5/one.dat",
        "dir5/two.dat",
        "foo.txt",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, ignore="dir3")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_ignore_dir_match_extension(fixtures_path):
    paths = [
        "dir4/bat.txt",
        "dir4/baz.txt",
        "foo.txt",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, ignore="dir3", match="*.txt")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_match_extension(fixtures_path):
    paths = [
        "dir2/dir3/bar.txt",
        "dir2/dir3/foo.png",
        "dir4/bat.txt",
        "dir4/baz.txt",
        "foo.txt",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(
        tree,
        match=dedent(
            """
        *.txt
        *.png
    """
        ),
    )
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_match_only_files(fixtures_path):
    paths = [
        "dir2/dir3/bar.txt",
        "dir2/dir3/foo.png",
        "dir4/bat.txt",
        "dir4/baz.txt",
        "dir5/one.dat",
        "dir5/two.dat",
        "foo.txt",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, mode="only-files")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_match_only_dirs(fixtures_path):
    paths = [
        "dir2",
        "dir2/dir3",
        "dir4",
        "dir5",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, mode="only-dirs")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_match_only_dirs_filtered(fixtures_path):
    paths = [
        "dir4",
        "dir5",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, ignore="dir2", mode="only-dirs")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_match_only_dirs_matched(fixtures_path):
    paths = [
        "dir2",
        "dir2/dir3",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, match="dir2", mode="only-dirs")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths


def test_walk_ignore_match_mode(fixtures_path):
    paths = [
        "dir2/dir3/bar.txt",
        "dir2/dir3/foo.png",
        "dir5/one.dat",
        "dir5/two.dat",
    ]
    tree = fixtures_path / "file-trees" / "dir1"
    walked_paths = walk(tree, ignore="dir4", match="d*/", mode="only-files")
    walked_path_str = sorted([str(path.relative_to(tree)) for path in walked_paths])
    assert walked_path_str == paths
