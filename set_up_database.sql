DROP DATABASE IF EXISTS elearn_db;
CREATE DATABASE elearn_db;
CREATE USER 'elearn_dev'@'localhost' IDENTIFIED BY 'elearn_pwd';
GRANT ALL PRIVILEGES ON elearn_db.* TO 'elearn_dev'@'localhost';
