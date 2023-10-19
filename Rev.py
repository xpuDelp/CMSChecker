# Made by Samarpreet ! 

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to check if the website is using WordPress
def is_wordpress(url):
    response = requests.get(url)
    headers = response.headers

    # Check for common WordPress headers
    if 'x-powered-by' in headers and 'wordpress' in headers['x-powered-by'].lower():
        return True

    # Check for common WordPress paths in the HTML source
    soup = BeautifulSoup(response.text, 'html.parser')
    common_wordpress_paths = ['/wp-content/', '/wp-includes/', '/wp-admin/']

    for path in common_wordpress_paths:
        if path in response.text:
            return True

    return False

# Function to check if the website is using Laravel
def is_laravel(url):
    response = requests.get(url)
    
    # Check for common Laravel paths in the HTML source
    common_laravel_paths = ['/public/', '/vendor/', '/bootstrap/']

    for path in common_laravel_paths:
        if path in response.text:
            return True

    return False

# Read the list of domains from a text file
with open('domains.txt', 'r') as domains_file:
    domains = [line.strip() for line in domains_file]

# Function to process a single URL
def process_url(url):
    try:
        # Add 'http://' or 'https://' if not already present
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        print(f"Checking {url}:")
        if is_wordpress(url):
            print(f"{url} is using WordPress.")
            with open('wordpress.txt', 'a') as wordpress_file:
                wordpress_file.write(url + "\n")
        elif is_laravel(url):
            print(f"{url} is using Laravel.")
            with open('laravel.txt', 'a') as laravel_file:
                laravel_file.write(url + "\n")
        else:
            print(f"{url} does not appear to be using WordPress or Laravel.")
        print()
    except Exception as e:
        print(f"An error occurred with {url}: {str(e)}")
        print("Skipping this domain.")

# Use a ThreadPoolExecutor for concurrent processing
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_url, domains)
