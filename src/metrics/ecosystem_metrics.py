import sqlite3
import pandas as pd
import json
import os

def calculate_ecosystem_metrics(db_path="data/github_peru.db", output_path="data/metrics/ecosystem_metrics.json"):
    conn = sqlite3.connect(db_path)
    
    # Total Users
    users_count = pd.read_sql_query("SELECT COUNT(*) as count FROM users", conn)['count'][0]
    
    # Total Repos (excluding forks)
    repos_count = pd.read_sql_query("SELECT COUNT(*) as count FROM repos WHERE fork=0", conn)['count'][0]
    
    # Language Distribution
    lang_dist = pd.read_sql_query("SELECT language, COUNT(*) as count FROM repos WHERE fork=0 GROUP BY language", conn).to_dict('records')
    
    # Top Industries
    industry_dist = pd.read_sql_query("SELECT industry_name, COUNT(*) as count FROM repos WHERE industry_name IS NOT NULL GROUP BY industry_name", conn).to_dict('records')
    
    metrics = {
        "total_users": int(users_count),
        "total_repositories": int(repos_count),
        "languages": lang_dist,
        "industries": industry_dist,
        "updated_at": pd.Timestamp.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    conn.close()
    print(f"Ecosystem metrics saved to {output_path}")

if __name__ == "__main__":
    calculate_ecosystem_metrics()
