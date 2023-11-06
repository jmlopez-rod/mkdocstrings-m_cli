#!/bin/bash

export PYTHONPATH="${PWD}/python"

set -xeuo pipefail

# source the m environment
m ci env m > /dev/null
source m/.m/env.list
export $(cut -d= -f1 m/.m/env.list)


target=.stage-pypi

rm -rf "$target"
mkdir -p "$target"

cp -r ./python "./$target/python/"
cp LICENSE README.md pyproject.toml "./$target"

find "./$target" | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf || true
sed -i -e "s/0.0.0-dev0/$M_PY_TAG/g" "./$target/pyproject.toml"

(
  cd "$target"
  poetry build
)

# Only proceed with the CI tool
[ "$M_CI" == "True" ] || exit 0

{
  echo "m-is-release=$M_IS_RELEASE"
  echo "m-tag=$M_TAG"
} >> "$GITHUB_OUTPUT"
