#! /bin/bash
sudo docker build -t runway-overload . 
sudo docker run --rm -p 1337:1337  --name runway-overload runway-overload 
