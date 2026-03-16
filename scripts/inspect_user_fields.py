import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {username}: {response.status_code}")
        return None

if __name__ == "__main__":
    # Get a sample user (first one from the search)
    search_url = "https://api.github.com/search/users?q=location:peru&per_page=1"
    search_resp = requests.get(search_url, headers=HEADERS)
    if search_resp.status_code == 200:
        sample_username = search_resp.json()['items'][0]['login']
        print(f"Fetching details for sample user: {sample_username}")
        details = get_user_details(sample_username)
        if details:
            print("\nAvailable columns (keys) at user level:")
            keys = list(details.keys())
            print(keys)
            
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            # Save to a file for inspection
            with open("data/sample_user_fields.json", "w") as f:
                json.dump(details, f, indent=4)
            print("\nFull sample data saved to data/sample_user_fields.json")
    else:
        print(f"Error searching: {search_resp.status_code}")
