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

INPUT_USERS_FILE = "data/users_peru_full.csv"
TEMP_JSON = "data/repos_1200_users_progress.json"
OUTPUT_CSV = "data/repos_1200_users.csv"

def fetch_all_user_repos(username):
    all_repos = []
    page = 1
    per_page = 100
    
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
            print(f"\nRate limit reached. Waiting {sleep_duration} seconds until reset...")
            time.sleep(sleep_duration + 5)
            continue
        elif response.status_code == 404:
            print(f"\nUser {username} not found (404). Skipping.")
            return []
        else:
            print(f"\nError {response.status_code} for {username}. Skipping.")
            break
            
    return all_repos

def main():
    if not os.path.exists(INPUT_USERS_FILE):
        print(f"Error: {INPUT_USERS_FILE} not found.")
        return

    # Load users
    df_users = pd.read_csv(INPUT_USERS_FILE)
    all_logins = df_users['login'].unique().tolist()
    
    # Load or initialize progress
    processed_data = []
    processed_logins = set()
    
    if os.path.exists(TEMP_JSON):
        with open(TEMP_JSON, "r") as f:
            processed_data = json.load(f)
            # Identify which logins are already in the data
            for repo in processed_data:
                processed_logins.add(repo.get('owner', {}).get('login'))
        print(f"Resuming from progress. Found {len(processed_logins)} users already processed.")

    # Determine 1200 random users (if not already picked)
    # We use a seed for consistency in selection, but only among those not processed if starting fresh
    random.seed(42)
    selected_logins_pool = random.sample(all_logins, min(1200, len(all_logins)))
    
    # Filter out already processed
    remaining_logins = [l for l in selected_logins_pool if l not in processed_logins]
    total_to_process = len(selected_logins_pool)
    
    print(f"Target: {total_to_process} users. Missing to process: {len(remaining_logins)}")

    try:
        count = len(processed_logins)
        for username in remaining_logins:
            repos = fetch_all_user_repos(username)
            if repos:
                processed_data.extend(repos)
            
            processed_logins.add(username)
            count += 1
            
            # Progress display
            print(f"Progress: {count}/{total_to_process} (User: {username}, Found: {len(repos)} repos)", end='\r')
            
            # Periodic save (every 20 users)
            if count % 20 == 0:
                with open(TEMP_JSON, "w") as f:
                    json.dump(processed_data, f, indent=4)
                # Update CSV periodically too
                if processed_data:
                    df_temp = pd.json_normalize(processed_data)
                    df_temp.to_csv(OUTPUT_CSV, index=False)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Saving current progress...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        if processed_data:
            print("\nFinalizing and saving data...")
            with open(TEMP_JSON, "w") as f:
                json.dump(processed_data, f, indent=4)
            
            # Final CSV conversion with all columns
            df_final = pd.json_normalize(processed_data)
            df_final.to_csv(OUTPUT_CSV, index=False)
            print(f"Data saved to {OUTPUT_CSV}. Total repos: {len(df_final)}, Total columns: {len(df_final.columns)}")
            
            if len(processed_logins) >= total_to_process:
                print("Task complete. You can now use the CSV file.")

if __name__ == "__main__":
    main()
