ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
BIN_DIR := $(ROOT_DIR)/bin
SRC_DIR := $(ROOT_DIR)/src
TF_DIR := $(ROOT_DIR)/terraform

CORES ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

.DEFAULT_GOAL := list
.ONESHELL:
# .ONESHELL runs a recipe's lines in ONE shell, so without -e only the LAST line decides the
# target's exit status, and a failing check early in a recipe reports success.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

# smk's checks: format, lint, types and the commit hook, rewritten on every render. ci runs them
# through `checks`, which smkproj.toml's Checks chooses.
include $(ROOT_DIR)/.smk/checks.mk
# Each language's build, test and clean, and each feature's targets, rewritten on every render: one
# file per language under .smk/lang/ and per feature under .smk/features/, which hook themselves into
# build, test and clean below. A language added to smkproj.toml's Languages reaches make here.
include $(ROOT_DIR)/.smk/targets.mk

###############################################################################
#                                   Build                                     #
###############################################################################
# The languages' files give these their work (build: build-csharp); make joins the prerequisites of
# every rule for a target, so this file's rules stay empty and a repository adds its own targets after them.
.PHONY: build test clean ci
clean:

build:

test:

# The one command a CI runner calls: everything a change must pass before it merges.
ci: build test

###############################################################################
#                                 Terraform                                   #
###############################################################################
tf-ci: tf-ci-init
	@cd $(TF_DIR)/ci
	terraform plan

tf-ci-init:
	@cd $(TF_DIR)/ci
	terraform init

tf-ci-bootstrap: tf-ci-init
	@cd $(TF_DIR)/ci
	terraform apply -auto-approve $(addprefix -target=,$(shell grep -v -e "^#" -e "^$$" $(TF_DIR)/ci/bootstrap.targets))

tf-ci-apply: tf-ci-init
	@cd $(TF_DIR)/ci
	terraform apply -auto-approve

tf-ci-upgrade:
	@cd $(TF_DIR)/ci
	terraform init -upgrade

tf-ci-output:
	@cd $(TF_DIR)/ci
	@terraform output -json

###############################################################################
#                                 Utilities                                   #
###############################################################################

# https://stackoverflow.com/a/26339924/11547115
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
