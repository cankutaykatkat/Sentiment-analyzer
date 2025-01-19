import sqlite3
import os

# Path to the database file
db_path = os.path.join(os.path.dirname(__file__), 'feedback.db')

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the old feedback table if it exists
    cursor.execute("DROP TABLE IF EXISTS feedback")

    # Create the feedback table with the new schema
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
    print("Feedback table updated successfully!")
except sqlite3.Error as e:
    print(f"Error updating feedback table: {e}")
