#!/usr/bin/bash

set -e
source .env

cd src/agileengine/; gunicorn --bind 0.0.0.0:5000 manage:app --reload
