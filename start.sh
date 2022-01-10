#!/bin/bash
set -e

# Invoke http.server
python -m http.server 7000 &

# create data.json file to get expected data
echo 'Creating data.json, this might take couple of minutes please wait'
python qa_utilities/get_test_data.py

bash
