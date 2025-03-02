import requests
import sqlite3
from bs4 import BeautifulSoup
from collections import Counter
import re

# Database setup
conn = sqlite3.connect("search_data.db")
cursor = conn.cursor()

# Table create kar rahe hain
cursor.execute('''CREATE TABLE IF NOT EXISTS search_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    keywords TEXT
                 )''')
conn.commit()

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Sab words nikal rahe hain
    common_words = set(["the", "and", "to", "of", "a", "in", "is", "it", "you", "that"])  # Common words remove karne ke liye
    filtered_words = [word for word in words if word not in common_words]
    return Counter(filtered_words).most_common(10)  # Top 10 keywords

def crawl_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            keywords = extract_keywords(text)

            cursor.execute("INSERT OR IGNORE INTO search_results (url, keywords) VALUES (?, ?)", 
                           (url, str(keywords)))
            conn.commit()

            print(f"Crawled: {url}")
            print(f"Top Keywords: {keywords}\n")

            # Dusre links ke liye crawl karna
            for link in soup.find_all('a', href=True):
                absolute_url = requests.compat.urljoin(url, link['href'])
                crawl_website(absolute_url)  # Recursive call

    except Exception as e:
        print(f"Error crawling {url}: {e}")

# Starting point
crawl_website("https://google.com")  # Yaha tum apni website bhi de sakte ho

# Database close
conn.close()