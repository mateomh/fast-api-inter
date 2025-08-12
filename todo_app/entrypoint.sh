#!/bin/sh

set -e

pipenv requirements >> requirements.txt

pip install -r requirements.txt

exec "$@"
