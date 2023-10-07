
project_dir := justfile_directory()

export PYTHONPATH := project_dir

@help:
  just --list

@test-all:
  pytest --capture=no -o log_cli=false tests/

@test *params:
  pytest -x --capture=no -o log_cli=true {{ params }}

@format:
  black {{ project_dir }}

@type-check:
  mypy {{ project_dir }}/gitignore_match/

@cli:
  ipython
