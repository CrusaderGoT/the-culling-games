#!/usr/bin/env bash

# Create the .postgresql directory
mkdir -p /opt/render/.postgresql

# Copy the root.crt file to the .postgresql directory
cp certs/root.crt /opt/render/.postgresql/

# Install dependencies
pip install -r requirements.txt

# Any other build steps...
