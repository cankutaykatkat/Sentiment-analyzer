import sqlite3
import os

# Path to the database file
db_path = os.path.join(os.path.dirname(__file__), 'feedback.db')

# Initialize the database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create feedback table with additional columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        user_agent TEXT NOT NULL,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
except sqlite3.Error as e:
    print(f"Error initializing database: {e}")
