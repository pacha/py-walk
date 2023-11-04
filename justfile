
project_dir := justfile_directory()

@help:
  just --list

@setup:
  pip install -e ".[dev]"

@test-all:
  pytest tests/

@test *params:
  pytest -x -o log_cli=true {{ params }}

@format:
  black {{ project_dir }}

@type-check:
  mypy {{ project_dir }}
