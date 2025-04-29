    -- create database and table for streamlog
    CREATE DATABASE IF NOT EXISTS streamlog;
    USE streamlog;  

    -- Create User table
    CREATE TABLE IF NOT EXISTS User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        age INT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

    -- Create Movie table
    CREATE TABLE IF NOT EXISTS Movie (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        genre VARCHAR(50) NOT NULL,
        duration INT ,
        release_year INT ,
        rating FLOAT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

    -- 建立 WatchLog 表
    CREATE TABLE IF NOT EXISTS WatchLog (
        watch_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        watch_date DATE,
        mood VARCHAR(20),
        rating INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    -- 建立 UserNote 表
    CREATE TABLE IF NOT EXISTS UserNote (
        note_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        like_count INT DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;