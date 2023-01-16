# book_to_scrape

## What is it ? 
Book_to_scrape is a scrapper which will extracts all the wanted informations about all the pages available on the website : `http://books.toscrape.com/`
It's a beta version, so it may have some issues to fix or somethings to upgrade 
The scrapper will get this informations on each book : 
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
- 
The program is not automatic, you need to launch it to extract all the needed informations 
Follow the steps below to discover how to

### Installation
In the root of the project : 
  - in a terminal type : `python3 -m venv venv` (if you use python 2.x, type python2) and this command : `pip3 install -r requirements.txt`
  - Finally, always in the terminal, type the command python3 main.py 

All the extracted datas will go to a folder named `data` (already created)

Just let the program runs alone and enjoy the extracted datas ! 