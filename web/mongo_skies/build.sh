sudo docker build -t royal-skies-login .
sudo docker run -d -p 3000:3000 -e "FLAG=METACTF{welcome_on_board}" --name skies-login royal-skies-login