import sqlite3
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, db_path="data/github_peru.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Users table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT UNIQUE,
            name TEXT,
            company TEXT,
            blog TEXT,
            location TEXT,
            email TEXT,
            hireable BOOLEAN,
            bio TEXT,
            followers INTEGER,
            following INTEGER,
            public_repos INTEGER,
            created_at TEXT,
            updated_at TEXT,
            type TEXT,
            site_admin BOOLEAN,
            year INTEGER
        )
        """)

        # Repos table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY,
            name TEXT,
            full_name TEXT UNIQUE,
            description TEXT,
            owner_login TEXT,
            html_url TEXT,
            stargazers_count INTEGER,
            forks_count INTEGER,
            watchers_count INTEGER,
            language TEXT,
            created_at TEXT,
            updated_at TEXT,
            pushed_at TEXT,
            size INTEGER,
            visibility TEXT,
            fork BOOLEAN,
            open_issues_count INTEGER,
            license_name TEXT,
            topics TEXT,
            readme TEXT,
            industry_code TEXT,
            industry_name TEXT,
            confidence TEXT,
            reasoning TEXT,
            FOREIGN KEY (owner_login) REFERENCES users (login)
        )
        """)
        self.conn.commit()

    def import_users_from_csv(self, csv_path):
        if not os.path.exists(csv_path):
            print(f"File {csv_path} not found.")
            return
        
        df = pd.read_csv(csv_path)
        # Handle calculated fields
        df['year'] = pd.to_datetime(df['created_at']).dt.year
        
        # Select columns that exist in table
        columns = [
            'id', 'login', 'name', 'company', 'blog', 'location', 'email', 
            'hireable', 'bio', 'followers', 'following', 'public_repos', 
            'created_at', 'updated_at', 'type', 'site_admin', 'year'
        ]
        df_db = df[[c for c in columns if c in df.columns]]
        
        df_db.to_sql('users', self.conn, if_exists='replace', index=False)
        print(f"Imported {len(df_db)} users to database.")

    def import_repos_from_csv(self, csv_path):
        if not os.path.exists(csv_path):
            print(f"File {csv_path} not found.")
            return
        
        df = pd.read_csv(csv_path)
        
        # Rename columns if they don't match (specifically nested ones flattened by json_normalize)
        rename_map = {
            'owner.login': 'owner_login',
            'license.name': 'license_name'
        }
        df = df.rename(columns=rename_map)
        
        # Convert topics list to string if it's a list
        if 'topics' in df.columns:
            df['topics'] = df['topics'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

        # Basic columns
        columns = [
            'id', 'name', 'full_name', 'description', 'owner_login', 'html_url',
            'stargazers_count', 'forks_count', 'watchers_count', 'language',
            'created_at', 'updated_at', 'pushed_at', 'size', 'visibility',
            'fork', 'open_issues_count', 'license_name', 'topics'
        ]
        
        # Add any industry columns if they already exist (unlikely but safe)
        for extra in ['industry_code', 'industry_name', 'confidence', 'reasoning', 'readme']:
            if extra in df.columns:
                columns.append(extra)

        df_db = df[[c for c in columns if c in df.columns]]
        df_db.to_sql('repos', self.conn, if_exists='replace', index=False)
        print(f"Imported {len(df_db)} repos to database.")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
    db.import_users_from_csv("data/users_peru_full.csv")
    db.import_repos_from_csv("data/repos_1200_users.csv")
    db.close()
