import requests
import sqlite3
from bs4 import BeautifulSoup
from collections import Counter
import re

# Database setup
conn = sqlite3.connect("search_data.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS search_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    keywords TEXT
                 )''')
conn.commit()

visited_urls = set()

# Stopwords jo remove karne hain
COMMON_WORDS = set([
    "the", "and", "for", "that", "with", "this", "from", "your", "more", "have",
    "was", "his", "about", "main", "english", "other", "articles", "article",
    "search", "content", "featured", "edit", "pages"
])

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered_words = [word for word in words if word not in COMMON_WORDS]
    return Counter(filtered_words).most_common(10)  # Top 10 keywords

def crawl_website(url):
    if url in visited_urls or "#" in url:  # Agar URL pehle visit ho chuka ya anchor link hai, toh skip karo
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            keywords = extract_keywords(text)

            cursor.execute("INSERT OR IGNORE INTO search_results (url, keywords) VALUES (?, ?)", 
                           (url, str(keywords)))
            conn.commit()

            print(f"\nCrawled: {url}")
            print(f"Top Keywords: {keywords}")

            for link in soup.find_all('a', href=True):
                absolute_url = requests.compat.urljoin(url, link['href'])
                if absolute_url.startswith("http") and "wikipedia.org" in absolute_url:  
                    crawl_website(absolute_url)

    except Exception as e:
        print(f"Error crawling {url}: {e}")

# Start Crawling
crawl_website("https://wikipedia.org")  

conn.close()