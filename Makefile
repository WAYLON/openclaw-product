VENV_DIR ?= .venv
VENV_PYTHON := $(VENV_DIR)/bin/python3
PYTHON ?= $(if $(wildcard $(VENV_PYTHON)),$(VENV_PYTHON),python3)

.PHONY: venv bootstrap doctor quality install-all check-packages delivery-check acceptance ci

venv:
	python3 -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

bootstrap:
	$(PYTHON) installer/bootstrap_project.py run

doctor:
	./agent-platform doctor

quality:
	$(PYTHON) scripts/quality_check.py

check-packages:
	$(PYTHON) scripts/check_all_packages.py

delivery-check:
	$(PYTHON) scripts/delivery_check.py

acceptance:
	$(PYTHON) scripts/acceptance_check.py

ci:
	@if [ ! -x "$(VENV_PYTHON)" ]; then echo "请先执行 make venv"; exit 1; fi
	$(MAKE) quality
	$(MAKE) check-packages
	$(MAKE) delivery-check
	$(PYTHON) installer/bootstrap_project.py check
	./agent-platform doctor

install-all:
	for agent in education-agent stock-agent loan-agent social-media-agent news-agent sales-agent; do \
		./agent-platform agent install $$agent || exit 1; \
	done
