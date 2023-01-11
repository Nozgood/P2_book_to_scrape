import requests
import os
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
res = requests.get(url)
dirPath = "/Users/nowfeel/Python/book_to_scrape/images/"

if res.ok:
    page = BeautifulSoup(res.text, "html.parser")
    imgTag = page.find("div", class_="item active").find("img")
    imgLink = "https://books.toscrape.com/media" + imgTag["src"].split("media")[1]
    imgName = imgTag["alt"]
    print(imgLink)
    # creating a file jgp and writing the img in (using bytes) and save it to an images directory
    finalPath = os.path.join(dirPath + imgName.replace(" ", "-") + ".jpg")
    with open(finalPath, "wb") as file:
        imgScrap = requests.get(imgLink)
        if res.ok:
            file.write(imgScrap.content)
