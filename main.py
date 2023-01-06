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
        upcValue = ""
        priceWithTax = ""
        priceWithoutTax = ""
        availableValue = ""
        imgUrl = ""
        bookPage = BeautifulSoup(res.text, "html.parser")

        # Get the title of the book
        titleBook = bookPage.find("div", class_="col-sm-6 product_main").find("h1").string

        # Get the UPC, price (excl/incl tax), availability information from the html page
        productInfoTable = bookPage.find("table")
        allTr = productInfoTable.findAll("tr")
        for tr in allTr:
            titleTr = tr.find("th").string
            if titleTr == "UPC":
                upcValue = tr.find("td").string
            elif titleTr == "Price (excl. tax)":
                priceWithTax = tr.find("td").string
            elif titleTr == "Price (incl. tax)":
                priceWithoutTax = tr.find("td").string
            elif titleTr == "Availability":
                availabilitySentence = tr.find("td").string.split("(")
                sentenceSplit = availabilitySentence[1].split()
                availableValue = sentenceSplit[0]

        # get the product description
        pTags = bookPage.findAll("p")
        description = pTags[3].string

        # get the category
        breadCrumb = bookPage.find("ul", class_="breadcrumb")
        liBreadCrumb = breadCrumb.findAll("li")
        category = liBreadCrumb[2].text
        print(category)

        # get the review rating
        pTagStars = bookPage.find("p", class_="star-rating")
        classPtagStars = pTagStars["class"]
        reviewRating = classPtagStars[1]

        # get the image url
        imgTag = bookPage.find("div", class_="item active").find("img")
        imgUrl = imgTag["src"].replace("../../", "https://books.toscrape.com/")

        # initiate the dictionary # at the end it will be replace by csv export
        book = dict(
            url=links[i],
            title=titleBook,
            upc=upcValue,
            price_including_tax=priceWithTax,
            price_excluding_tax=priceWithoutTax,
            number_available=availableValue,
            image_url=imgUrl,
            product_description=description,
            category=category,
            review_rating=reviewRating,
        )
        books.append(book)
    else:
        print("bad res from fetching book url")
print(books)