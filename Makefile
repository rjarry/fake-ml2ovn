# Copyright (c) 2023 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

PYTHON = python3
PIP = $(PYTHON) -m pip
VIRTUALENV = $(PYTHON) -m venv
VENV = .venv
in_venv = . $(VENV)/bin/activate &&

.PHONY: all
all: lint

$(VENV)/bin/activate:
	$(VIRTUALENV) $(VENV)

$(VENV)/.stamp: $(VENV)/bin/activate requirements-dev.txt pyproject.toml
	$(in_venv) $(PIP) install -U -r requirements-dev.txt
	@touch $@

PY_FILES = $(shell git ls-files -- '*.py' 2>/dev/null || find * -name '*.py')
J ?= $(shell nproc)

.PHONY: lint
lint: $(VENV)/.stamp
	@echo "[black]"
	@$(in_venv) $(PYTHON) -m black -q -t py36 --diff --check $(PY_FILES) || \
		{ echo "Use 'make format' to fix the problems."; exit 1; }
	@echo "[isort]"
	@$(in_venv) $(PYTHON) -m isort -j$(J) --diff --check-only $(PY_FILES) || \
		{ echo "Use 'make format' to fix the problems."; exit 1; }
	@echo "[pylint]"
	@$(in_venv) $(PYTHON) -m pylint $(PY_FILES)

.PHONY: format
format: $(VENV)/.stamp
	@echo "[isort]"
	@$(in_venv) $(PYTHON) -m isort -j$(J) $(PY_FILES)
	@echo "[black]"
	@$(in_venv) $(PYTHON) -m black -q -t py36 $(PY_FILES)

.PHONY: sdist
sdist: $(VENV)/.stamp $(PYFILES)
	$(in_venv) $(PYTHON) -m build --sdist

.PHONY: upload
upload: $(VENV)/.stamp $(PYFILES)
	rm -f dist/*
	$(in_venv) $(PYTHON) -m build --sdist
	$(in_venv) $(PYTHON) -m twine upload -s dist/*
