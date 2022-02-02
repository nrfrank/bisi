#!/bin/bash

set -e

scripts_dir=$(dirname $0)
project_dir=$scripts_dir/..

pytest -m "not integration" --cov=src "$project_dir/tests"
pytest -m "integration" "$project_dir/tests"
