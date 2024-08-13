import sqlite3

def init_db():
    conn = sqlite3.connect('britannia.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            definition TEXT NOT NULL,
            upvotes INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            definition_id INTEGER,
            content TEXT NOT NULL,
            FOREIGN KEY (definition_id) REFERENCES definitions (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
