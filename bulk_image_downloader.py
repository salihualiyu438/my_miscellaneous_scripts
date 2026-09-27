import requests, os
from bs4 import BeautifulSoup

url = "https://www.bing.com/images/search?q=nigerian+bandits+images"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

os.makedirs("images", exist_ok=True)

for i, img in enumerate(soup.find_all("img")):
    src = img.get("src")
    if src and src.startswith("http"):
        try:
            data = requests.get(src).content
            with open(f"images/{i}.jpg", "wb") as f:
                f.write(data)
        except:
            pass
