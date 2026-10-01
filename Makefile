# {{PROJECT_NAME}} — canonical commands. Claude Code uses these rather than raw tool calls
# wherever a target exists (CLAUDE.md §5). Two tiers:
#   tool-free tier  : help, check, check-refs, check-evidence, check-docs, test-hooks, status
#                     -- run anywhere, including CI and cloud containers with no toolchain
#   toolchain tier  : check-env, setup, test, stages, codegen, codegen-check, report
#                     -- need one or more of the scientific tools installed locally
SHELL       := /usr/bin/env bash
PY          ?= scripts/py
TOPIC       ?= {{DEFAULT_TOPIC}}

.PHONY: help check-env setup test test-julia test-python stages codegen codegen-check \
        check check-refs check-evidence check-docs check-init test-hooks test-checks test-library test-env lint-ste status fetch-source \
        libraries search-library report new-record clean-logs

help: ## list targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-16s %s\n",$$1,$$2}'

# --- tool-free tier ----------------------------------------------------------------

check: test-hooks test-checks test-library test-env check-refs check-evidence check-docs ## all repository checks (no scientific toolchain needed)

check-init: ## fail if {{PLACEHOLDERS}} remain (expected to fail in the template itself)
	@$(PY) scripts/check_docs.py init

test-hooks: ## self-test the Claude Code hooks with synthetic payloads
	@scripts/test_hooks.sh

test-checks: ## self-test the repository checkers (reference resolution answers for a clone)
	@$(PY) scripts/test_checks.py

test-library: ## self-test the Zotero/Calibre tools against synthetic databases (read-only, import, BibTeX)
	@$(PY) scripts/test_library.py

test-env: ## self-test how scripts pick the Python environment (fake uv; no network)
	@scripts/test_env.sh

lint-ste: ## screen Markdown for the measurable ASD-STE100 rules (report only; FILE=... for one file)
	@$(PY) scripts/check_ste.py $(FILE)

check-refs: ## fail if a file path cited in Markdown no longer resolves
	@$(PY) scripts/check_docs.py refs

check-evidence: ## fail if an [E: file, "label"] evidence tag cites a label absent from the file
	@$(PY) scripts/check_docs.py evidence

check-docs: ## staleness guard: ownership declared, record consistency, stale write-ups
	@$(PY) scripts/check_docs.py stale

status: ## print docs/STATUS.md
	@cat docs/STATUS.md

new-record: ## scaffold a validation record with the required provenance fields
	@$(PY) scripts/new_record.py

fetch-source: ## fetch a source: arXiv LaTeX SOURCE + figures + PDF (ID=<arxiv-id|doi> LABEL=<name>)
	@$(PY) scripts/fetch_source.py "$(ID)" "$(LABEL)" $(FETCH_FLAGS)

libraries: ## report the PI's local Zotero/Calibre libraries (read-only)
	@$(PY) scripts/library.py status

search-library: ## targeted search of the local libraries (AUTHOR=... or TITLE=... or DOI=...)
	@$(PY) scripts/library.py search \
	  $(if $(AUTHOR),--author "$(AUTHOR)") $(if $(TITLE),--title "$(TITLE)") $(if $(DOI),--doi "$(DOI)")

clean-logs: ## remove tool logs
	rm -rf logs/*

# --- toolchain tier ----------------------------------------------------------------

check-env: ## report which tools and local libraries are present (never fails by default)
	@scripts/check_env.sh

setup: ## create/instantiate the language environments that are present
	@scripts/setup_env.sh

test: test-julia test-python ## run every present language's tests

test-julia: ## Julia unit/regression tests (skipped if julia is absent)
	@scripts/run_tests.sh julia

test-python: ## Python unit/regression tests (skipped if python is absent)
	@scripts/run_tests.sh python

stages: ## run symbolic/$(TOPIC)/stages.txt in declared order (any mix of languages)
	@scripts/run_stages.sh $(TOPIC) stage

codegen: ## run the export stages for $(TOPIC) -> symbolic/generated/<lang>/
	@scripts/run_stages.sh $(TOPIC) export

codegen-check: codegen ## regenerate hand-off code and fail on any diff from git
	@git diff --exit-code -- symbolic/generated/ && echo "generated code reproducible"

report: ## render reports/$(TOPIC)_report.md -> .pdf (pandoc + xelatex)
	@scripts/report_pdf.sh $(TOPIC)
