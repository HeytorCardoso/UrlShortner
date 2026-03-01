#!/bin/bash
cd "$(dirname "$0")"
exec python3 main.py >> app.log 2>&1