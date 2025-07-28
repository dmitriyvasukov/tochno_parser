from bs4 import BeautifulSoup
import requests 

url = "https://tochno.st/datasets"

response = requests.get(url, timeout=10)

soup = BeautifulSoup(response.text, 'html.parser')

container = soup.find('div', class_='data-sets-container')


links = container.find_all('a')

hrefs = [url.removesuffix("/datasets") + a['href'] for a in links]


with open("urls.txt", "w", encoding="utf-8") as f:
    for href in hrefs:
        f.write(href + "\n")

