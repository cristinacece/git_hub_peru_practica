import os
import requests
import json
import pandas as pd
import random
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

INPUT_FILE = "data/users_peru_full.csv"
OUTPUT_JSON = "data/sample_repos_full.json"
OUTPUT_CSV = "data/sample_repos_full.csv"

def fetch_all_user_repos(username):
    all_repos = []
    page = 1
    per_page = 100
    
    print(f"  Fetching repos for {username}...")
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            if len(repos) < per_page:
                break
            page += 1
        elif response.status_code == 403:  # Rate limit
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_duration = max(reset_time - int(time.time()), 60)
            print(f"    Rate limit reached. Waiting {sleep_duration}s...")
            time.sleep(sleep_duration + 5)
            continue
        else:
            print(f"    Error {response.status_code} for {username}")
            break
            
    return all_repos

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Load users and pick 10 at random
    df_users = pd.read_csv(INPUT_FILE)
    available_users = df_users['login'].tolist()
    
    sample_size = min(10, len(available_users))
    sample_usernames = random.sample(available_users, sample_size)
    
    print(f"Selected 10 random users: {', '.join(sample_usernames)}")
    
    all_sample_repos = []
    
    for username in sample_usernames:
        repos = fetch_all_user_repos(username)
        all_sample_repos.extend(repos)
        print(f"    Found {len(repos)} repositories.")

    if not all_sample_repos:
        print("No repositories found for the selected users.")
        return

    # Save full JSON
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(all_sample_repos, f, indent=4)
    print(f"\nFull JSON saved to {OUTPUT_JSON}")

    # Flatten and save CSV
    # Using json_normalize to flatten nested objects like 'owner' and 'license'
    df_repos = pd.json_normalize(all_sample_repos)
    df_repos.to_csv(OUTPUT_CSV, index=False)
    print(f"Full CSV saved to {OUTPUT_CSV} (Total rows: {len(df_repos)}, Total columns: {len(df_repos.columns)})")

if __name__ == "__main__":
    main()
