#!/bin/bash

# Ensure the certificates are placed in the correct path for Render (optional)
mkdir -p /opt/render/.postgresql
cp ./certs/root.crt /opt/render/.postgresql/root.crt

# upgrade pip
pip install --upgrade pip

# Install any dependencies if needed (optional)
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Other deployment-related steps can go here
