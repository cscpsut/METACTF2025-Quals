#!/bin/bash
sudo docker rm -f meta-24-path-finder
sudo docker rmi -f meta-24-path-finder
sudo docker build -t meta-24-path-finder .
sudo docker run -d -p 1337:1337 --name meta-24-path-finder meta-24-path-finder