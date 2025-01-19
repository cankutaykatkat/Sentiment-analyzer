import sqlite3

def inspect_db():
    db_path = 'app/database/feedback.db'
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        print(f"Connected to database: {db_path}")

        # Get a cursor object
        cursor = conn.cursor()

        # List all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")

        # Describe the feedback table if it exists
        if ('feedback',) in tables:
            print("\nTable structure for 'feedback':")
            cursor.execute("PRAGMA table_info(feedback);")
            columns = cursor.fetchall()
            for column in columns:
                print(f"{column[1]} ({column[2]})")

        conn.close()
        print("\nDatabase inspection complete.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_db()
