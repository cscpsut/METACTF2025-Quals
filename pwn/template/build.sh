#!/bin/bash

sudo docker rm -f pwn_challenge_name
sudo docker rmi -f pwn_challenge_name
sudo docker build -t pwn_challenge_name .
sudo docker run -p 1337:1337 pwn_challenge_name