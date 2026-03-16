import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def check_years():
    for year in range(2008, 2027):
        url = f"https://api.github.com/search/users?q=location:peru created:{year}-01-01..{year}-12-31"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            count = resp.json()['total_count']
            print(f"{year}: {count}")
        else:
            print(f"{year}: Error {resp.status_code}")

if __name__ == "__main__":
    check_years()
