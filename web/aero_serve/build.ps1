docker stop metactf25-aeroserve
docker rm -f metactf25-aeroserve
docker rmi -f metactf25-aeroserve
docker build -t metactf25-aeroserve .
docker run -d -p 1337:1337 -e "FLAG=METACTF{Fake_Flag}" --rm --name "metactf25-aeroserve" -v "${PWD}/source/templates:/app/templates" "metactf25-aeroserve"