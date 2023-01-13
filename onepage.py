import requests
import os
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"
res = requests.get(url)
imgDirPath = "/Users/nowfeel/Python/book_to_scrape/"

if res.ok:
    print("hello")
    page = BeautifulSoup(res.text, "html.parser")
    imgTag = page.find("div", class_="item active").find("img")
    imgLink = "https://books.toscrape.com/media" + imgTag["src"].split("media")[1]
    imgName = imgTag["alt"].replace("/", "-").replace("-", "--").replace("#", "+")
    print(imgLink)
    # creating a file jgp and writing the img in (using bytes) and save it to an images directory
    finalPath = os.path.join(imgDirPath + imgName + ".jpg")
    with open(finalPath, "wb") as file:
        imgScrap = requests.get(imgLink)
        if res.ok:
            file.write(imgScrap.content)


