import sys
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

P = 53
M = 2**64


def fetch_page(url):
    print("Fetching:", url)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("ERROR fetching page:", e)
        return ""


def extract_content(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    body_text = soup.get_text(separator=" ")
    body_text = re.sub(r"\s+", " ", body_text).strip()

    links = []
    for a in soup.find_all("a", href=True):
        full_url = urljoin(base_url, a["href"])
        links.append(full_url)

    return title, body_text, links


def word_frequencies(text):
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def polynomial_hash(word):
    hash_value = 0
    power = 1
    for char in word:
        hash_value = (hash_value + ord(char) * power) % M
        power = (power * P) % M
    return hash_value


def compute_simhash(freq):
    vector = [0] * 64
    for word, weight in freq.items():
        h = polynomial_hash(word)
        for i in range(64):
            if h & (1 << i):
                vector[i] += weight
            else:
                vector[i] -= weight

    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)
    return simhash


def count_common_bits(h1, h2):
    xor = h1 ^ h2
    diff = bin(xor).count("1")
    return 64 - diff


def process_url(url):
    html = fetch_page(url)

    if not html:
        print("No HTML returned.\n")
        return 0

    title, body, links = extract_content(html, url)

    print("\nTITLE:\n", title)
    print("\nBODY:\n", body[:500])  # print first 500 chars only (safe)
    print("\nLINKS:")
    for link in links:
        print(link)

    freq = word_frequencies(body)
    return compute_simhash(freq)


def main():
    print("Program started")

    if len(sys.argv) != 3:
        print("Usage: python script.py <url1> <url2>")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    h1 = process_url(url1)
    h2 = process_url(url2)

    print("\nSimhash 1:", h1)
    print("Simhash 2:", h2)
    print("Common bits:", count_common_bits(h1, h2))


if __name__ == "__main__":
    main()