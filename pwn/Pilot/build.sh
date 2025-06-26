#! /bin/bash
sudo docker build -t pilot . 
sudo docker run --rm -p 7444:7444 -e FLAG=METACTF{PLACEHOLDER} --name pilot pilot
