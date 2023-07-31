#!/bin/bash

# Setup the server
sudo apt-get -y install build-essential python3-dev
# apt-get -y install docker.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Run the container
docker-compose up -d