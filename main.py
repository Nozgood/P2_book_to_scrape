import requests
import csv
from bs4 import BeautifulSoup

links = []
books = []

for i in range(1, 11, 1):
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
        upcValue = ""
        priceWithTax = ""
        priceWithoutTax = ""
        availableValue = ""
        imgUrl = ""
        bookPage = BeautifulSoup(res.text, "html.parser")

        # Get the title of the book
        titleBook = bookPage.find("div", class_="col-sm-6 product_main").find("h1").string

        # Get the UPC, price (excl/incl tax), availability information from the table in the html page
        productInfoTable = bookPage.find("table")
        allTr = productInfoTable.findAll("tr")
        for tr in allTr:
            titleTr = tr.find("th").string
            if titleTr == "UPC":
                upcValue = tr.find("td").string
            elif titleTr == "Price (excl. tax)":
                priceWithTax = tr.find("td").string.replace("Â", "")
            elif titleTr == "Price (incl. tax)":
                priceWithoutTax = tr.find("td").string.replace("Â", "")
            elif titleTr == "Availability":
                availabilitySentence = tr.find("td").string.split("(")
                sentenceSplit = availabilitySentence[1].split()
                availableValue = sentenceSplit[0]

        # get the product description
        pTags = bookPage.findAll("p")
        description = pTags[3].text

        # get the category
        breadCrumb = bookPage.find("ul", class_="breadcrumb")
        liBreadCrumb = breadCrumb.findAll("li")
        category = liBreadCrumb[2].text.replace("\n", "").replace("ô", 'o')

        # get the review rating
        pTagStars = bookPage.find("p", class_="star-rating")
        classPtagStars = pTagStars["class"]
        reviewRating = classPtagStars[1]

        # get the image url
        imgTag = bookPage.find("div", class_="item active").find("img")
        imgUrl = imgTag["src"].replace("../../", "https://books.toscrape.com/")

        # TODO: replace the dictionary by the sending to csv file (do i have to store before all the datas ??

        book = [
            links[i],
            titleBook,
            upcValue,
            priceWithTax,
            priceWithoutTax,
            availableValue,
            imgUrl,
            description,
            category,
            reviewRating,
        ]
        books.append(book)
    else:
        print("bad res from fetching book url")


headers = ["product_page_url", "title", "upc", "price_including_tax", "price_exluding_tax", "number_available", "image_url", "description", "category", "review_rating"]
with open('test.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for book in books:
        writer.writerow(book)
    print("test.csv created")