DROP DATABASE IF EXISTS porto_dev_db;
CREATE DATABASE IF NOT EXISTS porto_dev_db;
CREATE USER IF NOT EXISTS 'porto_dev'@'localhost' IDENTIFIED BY 'porto_dev_pwd';
GRANT ALL PRIVILEGES ON `porto_dev_db`.* TO 'porto_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'porto_dev'@'localhost';
FLUSH PRIVILEGES;


