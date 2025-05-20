-- 插入三個使用者
INSERT INTO User (user_name, email, password, age) VALUES
('Alice', 'alice@example.com', '$2b$12$examplehashpassword1', 25),
('Bob', 'bob@example.com', '$2b$12$examplehashpassword2', 30),
('Charlie', 'charlie@example.com', '$2b$12$examplehashpassword3', 22);

-- 插入兩部電影
INSERT INTO Movie (title, genre, duration, release_year, rating) VALUES
('Inception', 'Sci-Fi', 148, 2010, 8.8),
('The Godfather', 'Crime', 175, 1972, 9.2);

-- 插入兩筆觀看紀錄
INSERT INTO WatchLog (user_id, movie_id, watch_date, mood, rating) VALUES
(1, 1, '2024-04-01', 'excited', 9),
(2, 2, '2024-04-02', 'thoughtful', 10);

-- 插入兩筆心得筆記
INSERT INTO UserNote (user_id, movie_id, content) VALUES
(1, 1, 'Amazing movie with mind-bending scenes!'),
(2, 2, 'A timeless classic. Highly recommended.');
