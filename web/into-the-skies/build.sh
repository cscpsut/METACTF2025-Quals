#!/bin/bash
sudo docker rm -f into-the-skies
sudo docker rmi -f into-the-skies
sudo docker build -t into-the-skies .
sudo docker run -d -p 3000:3000 --name into-the-skies into-the-skies