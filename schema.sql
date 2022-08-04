CREATE TABLE IF NOT EXISTS illustrators(
    id INTEGER PRIMARY KEY,
    name TEXT,
    urls TEXT,
    rank INTEGER,
    keywords TEXT,
    category_ranks TEXT,
    created_at TEXT DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')),
    updated_at TEXT DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime'))
);