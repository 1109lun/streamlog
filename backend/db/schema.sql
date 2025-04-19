-- Note: Please replace 'your_password' with your actual password
CREATE USER IF NOT EXISTS 'streamlog_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON streamlog.* TO 'streamlog_user'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS streamlog;

USE streamlog;

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    source VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_timestamp ON logs(timestamp);
CREATE INDEX idx_level ON logs(level);
CREATE INDEX idx_source ON logs(source);