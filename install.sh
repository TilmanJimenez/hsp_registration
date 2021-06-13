#!/bin/bash

#TODO: Check OS and addapt download
echo "Getting you a geckodriver"
curl https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-macos.tar.gz -OL
tar xvf geckodriver-v0.29.1-macos.tar.gz
rm geckodriver-v0.29.1-macos.tar.gz

echo "Creating venv"
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
deactivate
