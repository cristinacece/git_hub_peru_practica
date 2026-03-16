# Database Models Schema
# This file serves as documentation for the SQLite schema

USER_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE,
    name TEXT,
    company TEXT,
    blog TEXT,
    location TEXT,
    email TEXT,
    hireable BOOLEAN,
    bio TEXT,
    followers INTEGER,
    following INTEGER,
    public_repos INTEGER,
    created_at TEXT,
    updated_at TEXT,
    type TEXT,
    site_admin BOOLEAN,
    year INTEGER,
    total_stars_received INTEGER,
    avg_stars_per_repo REAL,
    total_forks_received INTEGER,
    account_age_days INTEGER,
    repos_per_year REAL,
    follower_ratio REAL,
    h_index INTEGER
)
"""

REPO_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS repos (
    id INTEGER PRIMARY KEY,
    name TEXT,
    full_name TEXT UNIQUE,
    description TEXT,
    owner_login TEXT,
    html_url TEXT,
    stargazers_count INTEGER,
    forks_count INTEGER,
    watchers_count INTEGER,
    language TEXT,
    created_at TEXT,
    updated_at TEXT,
    pushed_at TEXT,
    size INTEGER,
    visibility TEXT,
    fork BOOLEAN,
    open_issues_count INTEGER,
    license_name TEXT,
    topics TEXT,
    readme TEXT,
    industry_code TEXT,
    industry_name TEXT,
    confidence TEXT,
    reasoning TEXT,
    FOREIGN KEY (owner_login) REFERENCES users (login)
)
"""
