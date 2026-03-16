import os
import requests
import json
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

INPUT_FILE = "data/users_peru_all.json"
TEMP_FILE = "data/users_peru_enriched_temp.json"
OUTPUT_JSON = "data/users_peru_enriched.json"
OUTPUT_CSV = "data/users_peru_full.csv"

def fetch_user_details(username):
    url = f"https://api.github.com/users/{username}"
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403: # Rate limit
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_duration = max(reset_time - int(time.time()), 60)
            print(f"\nRate limit reached. Sleeping for {sleep_duration} seconds...")
            time.sleep(sleep_duration + 5)
            continue
        else:
            print(f"\nError fetching {username}: {response.status_code}")
            return None

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r") as f:
        basic_users = json.load(f)

    # Filter out organizations if any (though search was for users)
    usernames = [u['login'] for u in basic_users if u.get('type') == 'User']
    total = len(usernames)
    print(f"Total users to enrich: {total}")

    enriched_data = []
    processed_usernames = set()

    # Load progress if exists
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            enriched_data = json.load(f)
    elif os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r") as f:
            enriched_data = json.load(f)
            
    if enriched_data:
        processed_usernames = {u['login'] for u in enriched_data}
        print(f"Resuming from progress: {len(processed_usernames)} users already processed.")

    count = len(processed_usernames)
    
    try:
        for username in usernames:
            if username in processed_usernames:
                continue

            details = fetch_user_details(username)
            if details:
                enriched_data.append(details)
                processed_usernames.add(username)
            
            count += 1
            if count % 10 == 0 or count == total:
                print(f"Progress: {count}/{total} ({(count/total)*100:.2f}%)", end='\r')
                # Save checkpoint every 50 users
                if count % 50 == 0:
                    with open(TEMP_FILE, "w") as f:
                        json.dump(enriched_data, f, indent=4)
                    # Also save partial CSV for the user to see
                    pd.DataFrame(enriched_data).to_csv(OUTPUT_CSV, index=False)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Saving progress...")
    finally:
        # Save final JSON
        with open(OUTPUT_JSON, "w") as f:
            json.dump(enriched_data, f, indent=4)
        
        # Convert to CSV
        if enriched_data:
            df = pd.DataFrame(enriched_data)
            df.to_csv(OUTPUT_CSV, index=False)
            print(f"\nSuccess! Enriched data saved to {OUTPUT_CSV}")
            
            # Clean up temp file if finished
            if len(processed_usernames) == total:
                if os.path.exists(TEMP_FILE):
                    os.remove(TEMP_FILE)
        else:
            print("\nNo data to save.")

if __name__ == "__main__":
    main()
