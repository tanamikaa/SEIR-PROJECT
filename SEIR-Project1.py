import sys
import requests
from bs4 import BeautifulSoup

def main():
    # Check command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the URL:", e)
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # ------------------------
    # 1. Print Page Title
    # ------------------------
    if soup.title and soup.title.string:
        print(soup.title.string.strip())
    else:
        print("No Title Found")

    # ------------------------
    # 2. Print Page Body Text
    # ------------------------
    if soup.body:
        body_text = soup.body.get_text(separator="\n", strip=True)
        print(body_text)
    else:
        print("No Body Content Found")

    # ------------------------
    # 3. Print All Links
    # ------------------------
    for link in soup.find_all("a", href=True):
        print(link["href"])


if __name__ == "__main__":
    main()