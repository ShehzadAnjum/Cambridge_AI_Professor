#!/usr/bin/env python3
"""Quick script to check if gceguide.com is accessible."""

import requests
import sys

URLS = [
    "https://gceguide.com/",
    "https://gceguide.com/past-papers/A-AS-Level/Accounting-9706/",
    "https://gceguide.com/past-papers/A-AS-Level/Economics-9708/",
    "https://gceguide.com/past-papers/A-AS-Level/Mathematics-9709/",
    "https://gceguide.com/past-papers/A-AS-Level/English-General-Paper-8021/",
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Checking gceguide.com accessibility...")
print("=" * 60)

all_accessible = True
for url in URLS:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        status = "✓" if response.status_code == 200 else "✗"
        print(f"{status} {url}: {response.status_code}")
        if response.status_code != 200:
            all_accessible = False
    except Exception as e:
        print(f"✗ {url}: Error - {e}")
        all_accessible = False

print("=" * 60)
if all_accessible:
    print("All URLs are accessible! You can run download_past_papers.py now.")
    sys.exit(0)
else:
    print("Some URLs are not accessible. The website may be down.")
    print("Please try again later or check your internet connection.")
    sys.exit(1)


