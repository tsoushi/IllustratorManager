CREATE TABLE IF NOT EXISTS illustrators(
    id INT PRIMARY KEY,
    name TEXT,
    urls TEXT,
    rank INT,
    keywords TEXT,
    category_ranks TEXT,
    created_at TEXT DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')),
    updated_at TEXT DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime'))
);