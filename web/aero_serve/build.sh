#!/bin/bash
docker rm -f meta25-web-aeroserve
docker rmi -f meta25-web-aeroserve
docker build -t meta25-web-aeroserve .
docker run -d -p 1337:1337 -e "FLAG=METACTF{Fake_Flag}" --name "meta25-web-aeroserve" -v "${PWD}/source/templates:/app/templates" "meta25-web-aeroserve"
