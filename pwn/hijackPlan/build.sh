#! /bin/bash
sudo docker build -t hijack-plane . 
sudo docker run --rm -p 7444:7444 -e FLAG=METACTF{PLACEHOLDER} --name hijack-plane hijack-plane 

