#!/bin/bash
service mariadb start

ROOT_PASS='REDACTED'

APP_USER='appuser'
APP_PASS='REDACTED'

mysql -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('$ROOT_PASS');CREATE DATABASE IF NOT EXISTS traveliny;CREATE USER '$APP_USER'@'localhost' IDENTIFIED BY '$APP_PASS';GRANT SELECT, INSERT, UPDATE ON traveliny.* TO '$APP_USER'@'localhost';FLUSH PRIVILEGES;USE traveliny;CREATE TABLE users (    id INT AUTO_INCREMENT PRIMARY KEY,    username VARCHAR(255) NOT NULL,    password VARCHAR(255) NOT NULL,    name TEXT);INSERT INTO users (username, password, name) VALUES ('test', 'test', 'Test User');"