import os
import sqlite3
import requests
import base64
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

DB_PATH = "data/github_peru.db"

def get_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            content_base64 = resp.json()['content']
            content = base64.b64decode(content_base64).decode('utf-8', errors='ignore')
            return content[:2000] # Limit for classification cost/token limit
        elif resp.status_code == 403: # Rate limit
            return "RATE_LIMIT"
        else:
            return ""
    except:
        return ""

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get 1100 repos that don't have readme yet, prioritizing by stars
    cursor.execute("""
        SELECT id, owner_login, name, full_name 
        FROM repos 
        WHERE readme IS NULL OR readme = ''
        ORDER BY stargazers_count DESC
        LIMIT 1050
    """)
    repos = cursor.fetchall()
    
    print(f"Starting to fetch READMEs for {len(repos)} repositories...")
    
    processed = 0
    for repo_id, owner, name, full_name in repos:
        content = get_readme(owner, name)
        
        if content == "RATE_LIMIT":
            print("\nRate limit reached. Stopping for now.")
            break
            
        cursor.execute("UPDATE repos SET readme = ? WHERE id = ?", (content, repo_id))
        processed += 1
        
        if processed % 10 == 0:
            conn.commit()
            print(f"Processed {processed}/{len(repos)}...", end='\r')
            
    conn.commit()
    conn.close()
    print(f"\nDone. Processed {processed} repositories.")

if __name__ == "__main__":
    main()
