import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def check_count():
    url = "https://api.github.com/search/users?q=location:peru"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print(f"Total users found in Peru: {data['total_count']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_count()
