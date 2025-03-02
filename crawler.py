import requests
from bs4 import BeautifulSoup

def crawl_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            print("Found Link:", link['href'])

crawl_website("https://example.com")  # Yahan test ke liye kisi bhi website ka URL daal sakte ho
