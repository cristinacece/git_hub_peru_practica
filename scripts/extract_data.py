import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extraction.repo_extractor import GitHubRepoExtractor

def run_extraction():
    print("Starting specialized data extraction...")
    # This acts as the official entry point for data collection
    # In a full run, this would iterate over many users
    print("Connecting to GitHub API...")
    # For demonstration purposes, we initialize the extractor
    # extractor = GitHubRepoExtractor()
    # extractor.collect_repos_from_user("mriscoc") 
    print("Extraction logic ready in src/extraction/repo_extractor.py")
    print("Process completed (Demo Mode).")

if __name__ == "__main__":
    run_extraction()
