import requests
import os
import csv
from bs4 import BeautifulSoup

# transform_datas accept a scrapped page and transform datas according to the business need
def transform_datas(pageToTransform):
    allArticles = pageToTransform.find("ol", class_="row").findAll("article", class_="product_pod")
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
            print("book: " + titleBook + " scrapped")

# store_datas accepts the different path to store, and do it (images and csv file)
def store_datas(csvName, imgPath, booksToStore):
    with open('/Users/nowfeel/Python/book_to_scrape/data/' + csvName, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for book in books:
            writer.writerow(book)
        print("\n CSV File for category: '" + categoryTitle + "' created \n")
    if not os.path.exists(imgPath):
        os.mkdir(imgPath)
    for book in booksToStore:
        path = os.path.join(imgPath + book[1].replace(" ", "-").replace("/", "-") + ".jpg")
        with open(path, "wb") as file:
            imgScrap = requests.get(book[6])
            if res.ok:
                file.write(imgScrap.content)
                print("image for book " + books[1] + " stored")
            else:
                print("error during image's download")
    books.clear()


parentUrl = "https://books.toscrape.com/"
homeUrl = "https://books.toscrape.com/index.html"
categoriesLinks = []
books = []
headers = [
    "product_page_url",
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
allBooksScrapped = 0

res = requests.get(homeUrl)
if res.ok:
    indexPage = BeautifulSoup(res.content, "html.parser")
    categoriesContainer = indexPage.find("ul", class_="nav nav-list")
    categoriesList = categoriesContainer.find("ul").findAll("li")
    for i in range(len(categoriesList)):
        categoriesLinks.append(categoriesList[i].find("a")["href"])
else:
    print("error during the fetching of the home page")

# Scrap for each category
for i in range(len(categoriesLinks)):
    categoryReq = requests.get(parentUrl + categoriesLinks[i])
    categoryTitleStr = str(categoriesLinks[i]).split("/")[3]
    print("Work on this category:  " + categoryTitleStr)
    if categoryReq.ok:
        categoryPage = BeautifulSoup(categoryReq.content, "html.parser")
        categoryTitle = categoryPage.find("div", class_="page-header action").find("h1").text
        csvFileName = "scraps-books-" + categoryTitle + ".csv"
        imgDirPath = "/Users/nowfeel/Python/book_to_scrape/data/images/" + categoryTitle + "/"
        numberBooksCategory = int(categoryPage.find("form", class_="form-horizontal").find("strong").text)
        if numberBooksCategory < 21:
            transform_datas(categoryPage)
            allBooksScrapped += int(len(books))
            store_datas(csvFileName, imgDirPath, books)
            print("total books scrapped: " + str(allBooksScrapped))
        else:
            categoryNumberPages = int(categoryPage.find("li", class_="current").text.split("of ")[1])
            for indexCategoryPage in range(1, categoryNumberPages + 1, 1):
                urlCategoryIndex = "https://books.toscrape.com/catalogue/category/books/" + categoryTitleStr \
                    + "/page-" + str(indexCategoryPage) + ".html"
                reqCategoryIndex = requests.get(urlCategoryIndex)
                if reqCategoryIndex.ok:
                    categoryIndexPage = BeautifulSoup(reqCategoryIndex.content, "html.parser")
                    transform_datas(categoryIndexPage)
                else:
                    print("error during the fetching of the different category's pages")
            allBooksScrapped = allBooksScrapped + len(books)
            store_datas(csvFileName, imgDirPath, books)
            print("total books scrapped: " + str(allBooksScrapped))
    else:
        print("error during the fetching of the category home page")
