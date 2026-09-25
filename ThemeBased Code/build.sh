#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip, setuptools, and wheel for prebuilt binary wheel support
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install --no-cache-dir -r requirements.txt
