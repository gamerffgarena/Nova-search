import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP errors ke liye

        soup = BeautifulSoup(response.text, 'html.parser')
        found_links = set()  # Duplicate links remove karne ke liye

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])  # Relative URL ko full URL me convert karo
            found_links.add(full_url)

        print("\nFound Links:")
        for l in found_links:
            print(l)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Test crawler
crawl_website("https://gamerffgarena.github.io/Nova-search/")