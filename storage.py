import sqlite3

# Database setup
conn = sqlite3.connect("nova_search.db")
cursor = conn.cursor()

# Table for storing search data
cursor.execute("""
CREATE TABLE IF NOT EXISTS search_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT
)
""")
conn.commit()
conn.close()
