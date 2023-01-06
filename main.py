import requests
from bs4 import BeautifulSoup

links = []
books = []

for i in range(1, 2, 1):
    parentUrl = "https://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    res = requests.get(parentUrl)
    if res.ok:
        page = BeautifulSoup(res.text, 'html.parser')
        divLink = page.findAll("div", class_="image_container")
        for singleDiv in divLink:
            aTag = singleDiv.find("a")
            link = "https://books.toscrape.com/catalogue/" + aTag["href"]
            links.append(link)
    else:
        print("bad res from fetching")

for i in range(0, len(links), 1):
    print(i)
    res = requests.get(links[i])
    if res.ok:
        bookPage = BeautifulSoup(res.text, "html.parser")

        # Get the title of the book
        bookTitleDiv = bookPage.find("div", class_="col-sm-6 product_main")
        titleTag = bookTitleDiv.find("h1").string

        # get the upc
        # get the price including tax
        # get the price exluding tax
        # get the number available
        # get the product description
        # get the category
        # get the review rating
        # get the image_url

        # initiate the dictionary
        book = dict(
            url=links[i],
            title=titleTag,
        )
        books.append(book)
    else:
        print("bad res from fetching book url")
print(books)