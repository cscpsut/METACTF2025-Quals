#!/bin/bash

sudo docker rm -f crypto_challenge_name
sudo docker rmi -f crypto_challenge_name
sudo docker build -t crypto_challenge_name .
sudo docker run -p 1337:1337 crypto_challenge_name