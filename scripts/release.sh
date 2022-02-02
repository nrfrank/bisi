#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
  echo 'Can only release on the main branch'
  exit 1
fi

set -e

version_upgrade=$1

scripts_dir=$(dirname $0)
project_dir=$scripts_dir/..

echo 'Running tests...'
$scripts_dir/test.sh

echo "Bumping version: type=$version_upgrade"
bumpversion $version_upgrade

python -m build --wheel --sdist
twine upload dist/*

echo 'Pushing tag'
git push
git push origin --tags