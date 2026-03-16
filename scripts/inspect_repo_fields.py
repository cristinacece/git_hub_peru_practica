import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def inspect_repo_fields():
    # Use mabelolivera10 as a sample since we saw her earlier
    username = "mabelolivera10"
    url = f"https://api.github.com/users/{username}/repos?per_page=1"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repos = response.json()
        if repos:
            repo = repos[0]
            print(f"Sample data from repo: {repo['name']}")
            print("\nAvailable columns (keys) at repository level:")
            keys = list(repo.keys())
            print(keys)
            
            # Save to a file for reference
            os.makedirs("data", exist_ok=True)
            with open("data/sample_repo_fields.json", "w") as f:
                json.dump(repo, f, indent=4)
            print("\nFull sample repo data saved to data/sample_repo_fields.json")
        else:
            print("No repos found for this user.")
    else:
        print(f"Error fetching repos: {response.status_code}")

if __name__ == "__main__":
    inspect_repo_fields()
