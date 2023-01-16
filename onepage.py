import requests
import os
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
res = requests.get(url)
imgDirPath = "/Users/nowfeel/Python/book_to_scrape/"

if res.ok:
    print("hello")
    page = BeautifulSoup(res.text, "html.parser")
    pTags = page.findAll("p")
    description = pTags[3].text

    # creating a file jgp and writing the img in (using bytes) and save it to an images directory
    finalPath = os.path.join(imgDirPath + imgName + ".jpg")
    with open(finalPath, "wb") as file:
        imgScrap = requests.get(imgLink)
        if res.ok:
            file.write(imgScrap.content)


