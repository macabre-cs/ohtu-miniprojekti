CREATE TABLE references_table (
  id SERIAL PRIMARY KEY,
  reference_type TEXT NOT NULL,
  cite_key TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  year INTEGER NOT NULL,
  url TEXT,
  publisher TEXT,
  chapter TEXT,
  journal TEXT,
  volume TEXT,
  pages TEXT,
  booktitle TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE reference_tags (
  reference_id INTEGER NOT NULL REFERENCES references_table(id) ON DELETE CASCADE,
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (reference_id, tag_id)
);
