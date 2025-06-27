# METACTF2025-Quals
![image](https://github.com/user-attachments/assets/bcce8564-ba29-4d3b-a0ab-6bbee9354340)

![image](https://github.com/user-attachments/assets/c00689a3-0a12-4d5e-924a-f3ca81e3b5c9)

This repository contains all the challenges from the METACTF2025 qualifiers.


- OSINT: 3
- WEB: 5
- Crypto: 4
- Forensics: 5
- PWN 3
- REV: 4
- MISC: 2
- Warm-up: 4

All the challenges containes the source code and the writeup  

## How to run docker challenges
All docker challenges takes their flags from the ENV var `FLAG`, so in order to find the flag in your instance make sure to add `-e FLAG=METACTF{PLACEHOLDER}` to the last line in the challenge `build.sh`:
```sh
#!/bin/bash
sudo docker rm -f meta-24-path-finder
sudo docker rmi -f meta-24-path-finder
sudo docker build -t meta-24-path-finder .
sudo docker run -d -p 1337:1337 -e FLAG=METACTF{PLACEHOLDER} --name meta-24-path-finder meta-24-path-finder
```
then connect to `localhost` and the first port number after `-p` 
