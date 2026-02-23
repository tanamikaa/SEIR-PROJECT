import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        html = fetch_page(url)
    except Exception as e:
        print("Error fetching page:")
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    print(title)

    body_text = soup.get_text(separator=" ")
    body_text = " ".join(body_text.split())
    print(body_text)

    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        print(full_url)

if __name__ == "__main__":
    main()
