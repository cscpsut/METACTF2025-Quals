#!/bin/bash
sudo docker rm -f phantom_login
sudo docker rmi -f phantom_login
sudo docker build -t phantom_login .
sudo docker run -p 1337:1337 --rm -e FLAG=METACTF{FAKE_FLAG_FOR_TESTING} phantom_login