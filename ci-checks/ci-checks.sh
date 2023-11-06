#!/bin/bash
set -xeuo pipefail

./ci-checks/ruff.sh
./ci-checks/flake8.sh
./ci-checks/mypy.sh
./ci-checks/prettier.sh
