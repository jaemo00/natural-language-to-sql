-- TODO: Insert sample data here
USE nl2sql_demo;

INSERT INTO users (name, age, city)
VALUES
    ('철수', 20, 'Seoul'),
    ('영희', 25, 'Busan'),
    ('민수', 30, 'Seoul'),
    ('지수', 22, 'Incheon');

INSERT INTO orders (user_id, product, price)
VALUES
    (1, '노트북', 1200000),
    (1, '마우스', 25000),
    (2, '키보드', 45000),
    (3, '모니터', 300000),
    (4, '헤드셋', 80000);
