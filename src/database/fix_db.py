import sqlite3

def fix_database():
    conn = sqlite3.connect("data/github_peru.db")
    cursor = conn.cursor()
    
    # Check existing columns in repos
    cursor.execute("PRAGMA table_info(repos)")
    columns = [row[1] for row in cursor.fetchall()]
    
    required_columns = [
        ('readme', 'TEXT'),
        ('industry_code', 'TEXT'),
        ('industry_name', 'TEXT'),
        ('confidence', 'TEXT'),
        ('reasoning', 'TEXT')
    ]
    
    for col_name, col_type in required_columns:
        if col_name not in columns:
            print(f"Adding column {col_name} to repos table...")
            cursor.execute(f"ALTER TABLE repos ADD COLUMN {col_name} {col_type}")
    
    conn.commit()
    conn.close()
    print("Database fixed.")

if __name__ == "__main__":
    fix_database()
