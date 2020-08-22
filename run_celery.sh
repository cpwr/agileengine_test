#!/usr/bin/bash
set -e

cd src/agileengine/; celery -A tasks worker -Q images --loglevel=debug --beat
