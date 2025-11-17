CREATE TABLE references_table (
  id SERIAL PRIMARY KEY,
  cite_key TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  year INTEGER,
  publisher TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);