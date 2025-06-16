    -- create database and table for streamlog
    CREATE DATABASE IF NOT EXISTS streamlog;
    USE streamlog;  

    -- Create User table
    CREATE TABLE IF NOT EXISTS User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        age INT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

    -- Create Movie table
    CREATE TABLE IF NOT EXISTS Movie (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        genre VARCHAR(50) NOT NULL,
        duration INT ,
        release_year INT ,
        rating FLOAT,
        image_url VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

    -- Create WatchLog table
    CREATE TABLE IF NOT EXISTS WatchLog (
        watch_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        watch_date DATE,
        mood VARCHAR(20),
        rating FLOAT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    -- Create UserNote table
    CREATE TABLE IF NOT EXISTS UserNote (
        note_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    -- Create NoteLike table
    CREATE TABLE IF NOT EXISTS NoteLike (
        note_id INT NOT NULL,
        user_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (note_id, user_id),
        FOREIGN KEY (note_id) REFERENCES UserNote(note_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    -- Create MovieFavorite table
    CREATE TABLE IF NOT EXISTS MovieFavorite (
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;