import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}" if not endpoint.startswith("http") else endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("Rate limit exceeded or forbidden.")
            return None
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
