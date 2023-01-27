import requests
import os
import csv
from bs4 import BeautifulSoup

# TODO: AJOUTER LE PATH DATAS EN VARIABLE D'ENVIRONNEMENT
# init variables
parentUrl = "https://books.toscrape.com/"
categoriesLinks = []
headers = ["product_page_url",
           "title",
           "upc",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "image_url",
           "description",
           "category",
           "review_rating",
           ]
books = []

# Getting the categories
homeUrl = "https://books.toscrape.com/index.html"
res = requests.get(homeUrl)
if res.ok:
    indexPage = BeautifulSoup(res.content, "html.parser")
    categoriesContainer = indexPage.find("ul", class_="nav nav-list")
    categoriesList = categoriesContainer.find("ul").findAll("li")
    for i in range(len(categoriesList)):
        categoriesLinks.append(categoriesList[i].find("a")["href"])
else:
    print("bad response from fetching")

# Scrap for each category
for i in range(len(categoriesLinks)):
    categoryReq = requests.get(parentUrl + categoriesLinks[i])
    categoryTitleStr = str(categoriesLinks[i]).split("/")[3]
    if categoryReq.ok:
        categoryPage = BeautifulSoup(categoryReq.content, "html.parser")
        categoryTitle = categoryPage.find("div", class_="page-header action").find("h1").text
        csvFileName = "scraps-books-" + categoryTitle + ".csv"
        imgDirPath = "/Users/nowfeel/Python/book_to_scrape/data/images/" + categoryTitle + "/"
        numberBooksCategory = int(categoryPage.find("form", class_="form-horizontal").find("strong").text)
        if numberBooksCategory < 21:
            allArticles = categoryPage.find("ol", class_="row").findAll("article", class_="product_pod")
            # extract the link for each book
            for article in allArticles:
                linkBook = article.find("div", class_="image_container").find("a")["href"].split("../")
                formatLinkBook = parentUrl + "catalogue/" + linkBook[3]
                bookReq = requests.get(formatLinkBook)
                if bookReq.ok:
                    bookPage = BeautifulSoup(bookReq.content, "html.parser")
                    upcValue = ""
                    priceWithTax = ""
                    priceWithoutTax = ""
                    availableValue = ""
                    imgUrl = ""
                    titleBook = bookPage.find("div", class_="col-sm-6 product_main").find("h1").string
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
                    pTags = bookPage.findAll("p")
                    description = pTags[3].text
                    breadCrumb = bookPage.find("ul", class_="breadcrumb")
                    category = breadCrumb.findAll("a")[2].text
                    pTagStars = bookPage.find("p", class_="star-rating")
                    classPTagStars = pTagStars["class"]
                    reviewRating = classPTagStars[1]
                    imgTag = bookPage.find("div", class_="item active").find("img")
                    imgTitle = imgTag["alt"]
                    imgUrl = imgTag["src"].replace("../../", "https://books.toscrape.com/")

                    book = [
                        formatLinkBook,
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
                    print("error during getting the book")
        else:
            categoryNumberPages = int(categoryPage.find("li", class_="current").text.split("of ")[1])
            print(categoryNumberPages)
            for indexCategoryPage in range(1, categoryNumberPages + 1, 1):
                urlCategoryIndex = "https://books.toscrape.com/catalogue/category/books/" + categoryTitleStr + "/page-" + str(indexCategoryPage) + ".html"
                print(urlCategoryIndex)
                reqCategoryIndex = requests.get(urlCategoryIndex)
                if reqCategoryIndex.ok:
                    categoryIndexPage = BeautifulSoup(reqCategoryIndex.content, "html.parser")
                    allArticles = categoryPage.find("ol", class_="row").findAll("article", class_="product_pod")
                    # extract the link for each book
                    for article in allArticles:
                        linkBook = article.find("div", class_="image_container").find("a")["href"].split("../")
                        formatLinkBook = parentUrl + "catalogue/" + linkBook[3]
                        bookReq = requests.get(formatLinkBook)
                        if bookReq.ok:
                            bookPage = BeautifulSoup(bookReq.content, "html.parser")
                            upcValue = ""
                            priceWithTax = ""
                            priceWithoutTax = ""
                            availableValue = ""
                            imgUrl = ""
                            titleBook = bookPage.find("div", class_="col-sm-6 product_main").find("h1").string
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
                            pTags = bookPage.findAll("p")
                            description = pTags[3].text
                            breadCrumb = bookPage.find("ul", class_="breadcrumb")
                            category = breadCrumb.findAll("a")[2].text
                            pTagStars = bookPage.find("p", class_="star-rating")
                            classPTagStars = pTagStars["class"]
                            reviewRating = classPTagStars[1]
                            imgTag = bookPage.find("div", class_="item active").find("img")
                            imgTitle = imgTag["alt"]
                            imgUrl = imgTag["src"].replace("../../", "https://books.toscrape.com/")

                            book = [
                                formatLinkBook,
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
                    print("error during fetching the different category's pages")
    with open('/Users/nowfeel/Python/book_to_scrape/data/' + csvFileName, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for book in books:
            writer.writerow(book)
        print("\n CSV File for category: '" + categoryTitle + "' created \n")
    os.mkdir(imgDirPath)
    for book in books:
        path = os.path.join(imgDirPath + book[1].replace(" ", "-").replace("/", "-") + ".jpg")
        with open(path, "wb") as file:
            imgScrap = requests.get(book[6])
            if res.ok:
                file.write(imgScrap.content)
            else:
                print("error during image's download")
    books.clear()
else:
    print("error during getting the books corresponding to the category")

