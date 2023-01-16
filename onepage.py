import requests
import os
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
res = requests.get(url).content
imgDirPath = "/Users/nowfeel/Python/book_to_scrape/"

page = BeautifulSoup(res, "html.parser")

pTags = page.find("p", class_="").text
print(pTags)

