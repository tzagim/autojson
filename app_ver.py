import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

RSS_URL = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/rss?path=/xiaomi.eu/Xiaomi.eu-app"

# Read the current date from app_ver.txt
def read_current_date(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Write the new date to app_ver.txt
def write_new_date(file_path, date_str):
    with open(file_path, 'w') as file:
        file.write(date_str)

# RSS feed
response = requests.get(RSS_URL)
response.raise_for_status()  # Check if the request was successful

# Parse the RSS feed content using 'xml' parser
soup = BeautifulSoup(response.content, 'xml')

# Find all <item> elements
items = soup.find_all('item')

# Ensure there are items in the feed
if not items:
    print("No items found in the RSS feed.")
    exit(1)

# Extract the latest version title from the first <item>
latest_version = items[0].find('title').text

# Use a regular expression to extract the date part (assuming the date format is YYYY.MM.DD)
match = re.search(r'\d{4}\.\d{2}\.\d{2}', latest_version)
if match:
    new_date_str = match.group(0)
else:
    print("No date found in the latest version string.")
    exit(1)

# Read the current date from app_ver.txt
current_date_str = read_current_date('app_ver.txt')

# Check if the new date is different from the current date
if current_date_str:
    if new_date_str != current_date_str:
        write_new_date('app_ver.txt', new_date_str)
        print(f"app=Updated app_ver.txt to '{new_date_str}'")
    else:
        print('app=No update needed')
else:
    # If app_ver.txt does not exist, create it with the new date
    write_new_date('app_ver.txt', new_date_str)
    print(f"app_ver.txt not found. Created with the new date '{new_date_str}'.")
