#! /bin/bash
set -e

echo "Code scanning"

echo "Running pylint"
pylint --fail-under=10.00  ./apps/ ./project/ ./common/ ./api/

echo "Running flake8"
flake8 .
