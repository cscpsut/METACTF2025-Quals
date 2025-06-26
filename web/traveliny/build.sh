#!/bin/bash
sudo docker rm -f meta25-web-traveliny
sudo docker rmi -f meta25-web-traveliny
sudo docker build -t meta25-web-traveliny:latest .
sudo docker run -p 5000:5000 -e FLAG='METACTF{FAKE_FLAG_FOR_TESTING}' meta25-web-traveliny:latest