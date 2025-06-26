#!/bin/bash

sudo docker rm -f misc_warmup_seizure
sudo docker rmi -f misc_warmup_seizure
sudo docker build -t misc_warmup_seizure .
sudo docker run -d -p 1337:1337 --name misc_warmup_seizure misc_warmup_seizure
