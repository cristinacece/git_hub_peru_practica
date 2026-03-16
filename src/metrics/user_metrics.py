import sqlite3
import pandas as pd
from datetime import datetime
import os

class MetricsCalculator:
    def __init__(self, db_path="data/github_peru.db"):
        self.db_path = db_path
        
    def calculate_user_metrics(self):
        conn = sqlite3.connect(self.db_path)
        
        # Load data
        df_users = pd.read_sql_query("SELECT * FROM users", conn)
        # Drop calculated columns if they exist to avoid _x / _y collisions
        cols_to_drop = ['total_stars_received', 'avg_stars_per_repo', 'total_forks_received', 'account_age_days', 'repos_per_year', 'follower_ratio', 'h_index']
        df_users = df_users.drop(columns=[c for c in cols_to_drop if c in df_users.columns])
        
        df_repos = pd.read_sql_query("SELECT owner_login, stargazers_count, forks_count FROM repos WHERE fork=0", conn)
        
        # 1. Activity Metrics
        repo_stats = df_repos.groupby('owner_login').agg({
            'stargazers_count': ['sum', 'mean'],
            'forks_count': 'sum'
        }).reset_index()
        repo_stats.columns = ['login', 'total_stars_received', 'avg_stars_per_repo', 'total_forks_received']
        
        # Merge with users
        df_metrics = pd.merge(df_users, repo_stats, on='login', how='left').fillna(0)
        
        # 2. Account Age
        from datetime import timezone
        today = datetime.now(timezone.utc)
        df_metrics['created_at'] = pd.to_datetime(df_metrics['created_at'])
        df_metrics['account_age_days'] = (today - df_metrics['created_at']).dt.days
        df_metrics['repos_per_year'] = df_metrics['public_repos'] / (df_metrics['account_age_days'] / 365.25)
        
        # 3. Influence Metrics
        df_metrics['follower_ratio'] = df_metrics['followers'] / (df_metrics['following'] + 1)
        
        # 4. H-Index (Developer influence)
        # Definition: h-index is k if k of their repos have at least k stars
        def calculate_h_index(stars_list):
            stars_list = sorted(stars_list, reverse=True)
            h = 0
            for i, stars in enumerate(stars_list):
                if stars >= i + 1:
                    h = i + 1
                else:
                    break
            return h
        
        h_indices = df_repos.groupby('owner_login')['stargazers_count'].apply(lambda x: calculate_h_index(list(x))).reset_index()
        h_indices.columns = ['login', 'h_index']
        
        # Final merge
        df_final = pd.merge(df_metrics, h_indices, on='login', how='left').fillna(0)
        
        # Add new columns to users table if they don't exist
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        
        new_cols = [
            ('total_stars_received', 'INTEGER'),
            ('avg_stars_per_repo', 'REAL'),
            ('total_forks_received', 'INTEGER'),
            ('account_age_days', 'INTEGER'),
            ('repos_per_year', 'REAL'),
            ('follower_ratio', 'REAL'),
            ('h_index', 'INTEGER')
        ]
        
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
        
        # Update users table
        for _, row in df_final.iterrows():
            cursor.execute("""
                UPDATE users SET 
                    total_stars_received = ?, 
                    avg_stars_per_repo = ?, 
                    total_forks_received = ?, 
                    account_age_days = ?, 
                    repos_per_year = ?, 
                    follower_ratio = ?, 
                    h_index = ?
                WHERE login = ?
            """, (
                int(row['total_stars_received']),
                float(row['avg_stars_per_repo']),
                int(row['total_forks_received']),
                int(row['account_age_days']),
                float(row['repos_per_year']),
                float(row['follower_ratio']),
                int(row['h_index']),
                row['login']
            ))
            
        conn.commit()
        
        # Export to CSV for structural compliance
        output_csv = "data/metrics/user_metrics.csv"
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df_final.to_csv(output_csv, index=False)
        
        conn.close()
        print(f"User metrics updated in DB and saved to {output_csv}")


def calculate_user_metrics():
    calc = MetricsCalculator()
    calc.calculate_user_metrics()

if __name__ == "__main__":
    calculate_user_metrics()

