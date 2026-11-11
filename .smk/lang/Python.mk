# smk { overwrite: true }
# Python's test and clean, rewritten on every render. .smk/targets.mk includes this file, and make joins its hooks
# (test: test-python) with the Makefile's own test and clean. Python has no build step.
.PHONY: test-python clean-python
test: test-python
clean: clean-python

# The unittest suite from the repository root: with no arguments unittest discovers every test*.py in a package (a
# directory with __init__.py) under it. TEST_ARGS goes to python3 -m unittest: make test TEST_ARGS=tests.test_parse.
# Python 3.12 and later exit 5 when no test ran, so an empty suite fails.
test-python:
	cd "$(SMK_ROOT)" && python3 -m unittest $(TEST_ARGS)

# What Python and its checks derive: every __pycache__/ outside .git and .venv, the ruff and mypy caches, and out/.
clean-python:
	cd "$(SMK_ROOT)" && find . \( -name .git -o -name .venv \) -prune -o -type d -name __pycache__ -prune -exec rm -rf {} + && rm -rf .mypy_cache .ruff_cache out
