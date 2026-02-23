import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
P=53
M=2**64
def fetch_page(url):
    headers={"User-Agent": "Mozilla/5.0"}
    try:
        response=requests.get(url,headers=headers,timeout=15)
        response.raise_for_status()
        return response.text
    except:
        print("Error while fetching:", url)
        return ""

def extract_Page_content(html,base_url):
    soup = BeautifulSoup(html,"html.parser")

    for tag in soup(["script","style"]):
        tag.decompose()

    title= ""
    if soup.title and soup.title.string:
        title=soup.title.string.strip()

    body_text=soup.get_text(separator=" ")
    body_text= " ".join(body_text.split())

    links= []
    for a in soup.find_all("a", href=True):
        links.append(urljoin(base_url, a["href"]))

    return title,body_text,links

def word_frequencies(text):
    text=text.lower()
    freq= {}
    word= ""

    for ch in text:
        if ch.isalnum():
            word += ch
        else:
            if word != "":
                if word in freq:
                    freq[word]+= 1
                else:
                    freq[word]= 1
                word = ""

    if word != "":
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq

def polynomial_hash_value(word):
    hash_value = 0
    power = 1
    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % M
        power = (power * P) % M

    return hash_value

def get_simhash_func(freq):
    vector= [0] * 64

    for word in freq:
        weight = freq[word]
        h= polynomial_hash_value(word)

        for i in range(64):
            if h&(1<<i):
                vector[i] += weight
            else:
                vector[i] -= weight
    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)

    return simhash
def count_common_bits(h1, h2):
    xor= h1 ^ h2
    count = 0
    while xor:
        count+= xor & 1
        xor= xor >> 1
    return 64-count

def process_url(url):
    print("\nProcessing:", url)

    html = fetch_page(url)
    if html == "":
        return 0

    title,body,links= extract_Page_content(html, url)

    print("\nTitle:")
    print(title)

    print("\nNumber of links found:", len(links))

    freq = word_frequencies(body)
    return get_simhash_func(freq)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <url1> <url2>")
        sys.exit(1)

    h1= process_url(sys.argv[1])
    h2= process_url(sys.argv[2])

    print("\nSimhash 1:", h1)
    print("Simhash 2:", h2)
    print("Common bits:", count_common_bits(h1, h2))


if __name__ == "__main__":
    main()
