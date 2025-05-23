CREATE DATABASE event_planner;
USE event_planner;

CREATE TABLE Events (
id INT AUTO_INCREMENT PRIMARY KEY,
name  VARCHAR(255) NOT NULL,
description TEXT,
event_date DATETIME NOT NULL,
location VARCHAR(255),
reminder BOOLEAN  DEFAULT FALSE,
reminder_time INT  COMMENT 'minutes before'
);
