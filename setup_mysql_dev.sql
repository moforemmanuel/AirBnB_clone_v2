-- Creates a MySQL server with:
--   Database hbnb_dev_db.
--   User hbnb_dev with password hbnb_dev_pwd in localhost.
--   Grants all privileges for hbnb_dev on hbnb_dev_db.
--   Grants SELECT privilege for hbnb_dev on performance_schema.

-- Create hbnb_dev_db database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Switch to hbnb_dev_db database
USE hbnb_dev_db;

-- Create user hbnb_dev
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant usage on hbnb_dev_db to hbnb_dev
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost';
-- Grant Select previledges on performance_schema to hbnb_dev
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
-- Grant all previledges on hbnb_dev_db to hbnb_dev
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
-- Flush all previledges
FLUSH PRIVILEGES;
