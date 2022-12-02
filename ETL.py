import requests
from bs4 import BeautifulSoup
import csv
import os

url_site = "http://books.toscrape.com/index.html"

list_links_all_categories = []
list_links_all_books = []

def requests_beautifulsoup_url (url_requests):  # Get the url and analyse its html
    requests_url = requests.get(url_requests)
    beautifulsoup_url = BeautifulSoup(requests_url.text, "html.parser")
    return beautifulsoup_url

def collect_links_all_categories (url_of_the_site):

    # stock all links obtained by the function 
    # allows to have a single array of elements
    list_links_all_categories_in_function = []

    requests_beautifulsoup = requests_beautifulsoup_url(url_of_the_site)
    recovery_navigation_bar = requests_beautifulsoup.find(name="ul",attrs={"class":"nav nav-list"}) # collect the first "ul" tag with the "nav nav-list" attribute
    recovery_second_ul = recovery_navigation_bar.find("ul") # collect the first "ul" in the variable "recovery_navigation_bar"
    recovery_a_tags = recovery_second_ul.find_all("a") # collect all "a" tags in the variable "recovery_second_ul"
    for a in recovery_a_tags:
        partial_link_categorie = a["href"] # retrieve the link in the tag
        link_categorie = "http://books.toscrape.com/" + a["href"] # get an active link
        list_links_all_categories_in_function.append(link_categorie) # add the active link in the list
    return list_links_all_categories_in_function

def collect_url_all_books (setting):

    def number_of_pages_in_category (url_categorie):  # get number of pages in category
        requests_beautifulsoup = requests_beautifulsoup_url(url_categorie)
        if requests_beautifulsoup.find(name="li", attrs={"class":"current"}) == None:
            number_of_pages = 1
        else: 
           number_of_pages = int(requests_beautifulsoup.find(name="li", attrs={"class":"current"}).text.split()[3])
        return number_of_pages
    
    def url_books (setting):

        list_all_url_books = []
        for i in list_links_all_categories :

            # stock all links obtained by the function 
            # allows to have a single array that contains multiple arrays
            list_book_category = [] 

            number_of_pages_2 = number_of_pages_in_category(i)    
            for r in range(number_of_pages_2):
                url_page_categorie = i.replace("index",f"page-{r+1}") # recovery of the correct url for categories containing several pages
                if (r == 0): # if the category contains only one page
                    url_page_categorie = i 
                requests_beautifulsoup = requests_beautifulsoup_url(url_page_categorie)
                div_tags_2 = requests_beautifulsoup.find_all(name="div", attrs={"class":"image_container"}) # collect all "div" tags
                for div in div_tags_2:
                    collect_a_tags_2 = div.find_all("a") # collect all "a" tags
                    for a in collect_a_tags_2 :
                        partial_link_book_2 = a["href"].strip("../../../") # retrieve the link in the tag, and remove the unwanted
                        link_book_2 = "http://books.toscrape.com/catalogue/" + partial_link_book_2 # get an active link
                        list_all_url_books.append(link_book_2) # add the active link in the list
                        list_book_category.append(link_book_2) # add the active link in the list
                        
            name_category_file_csv = i.replace("http://books.toscrape.com/catalogue/category/books/","").replace("/index.html","") # get the title of the csv file          
            list_tmp = book_information(list_book_category) # call function "book information" which retrieves the information of each book
            create_csv(name_category_file_csv, list_tmp) # create a csv file for the category
            
        return list_all_url_books
 
    return url_books(setting)

def book_information (book_url):
    
    # allows to have a single array that contains multiple arrays
    list_all_book_information = []
    for i in book_url:

        # allows to have a single array of elements
        list_all_info_book =[]
        requests_beautifulsoup = requests_beautifulsoup_url(i)
        
        # get the informations of the book

        product_page_url = i
        a = product_page_url + " "
        list_all_info_book.append(a)

        title = requests_beautifulsoup.find("h1").text 
        list_all_info_book.append(title)

        price_including_tax = requests_beautifulsoup.find_all('td')[3].text
        c = price_including_tax.strip("Â") 
        list_all_info_book.append(c)

        price_excluding_tax = requests_beautifulsoup.find_all("td")[2].text
        d = price_excluding_tax.strip("Â") 
        list_all_info_book.append(d)

        universal_product_code = requests_beautifulsoup.find_all('td')[0].text
        list_all_info_book.append(universal_product_code) 

        number_available = requests_beautifulsoup.find_all("td")[5].text
        list_all_info_book.append(number_available)

        category = requests_beautifulsoup.find(name="ul", attrs={"breadcrumb"}).find_all('a')[2].text
        list_all_info_book.append(category)

        review_rating = requests_beautifulsoup.find(name="p",attrs={"class":"star-rating"})
        star_review_rating = review_rating ["class"][1] + "stars"     
        list_all_info_book.append(star_review_rating)

        image_url = requests_beautifulsoup.find('img')["src"].strip("../..")
        image_url_2 = "http://books.toscrape.com/" + image_url + " "
        list_all_info_book.append(image_url_2)

        product_description = requests_beautifulsoup.find_all('p')[3].text
        list_all_info_book.append(product_description)

        list_all_book_information.append(list_all_info_book) # add the active link in the list
    return list_all_book_information

def create_csv (csv_name,all_book_information_for_one_category):
    csv_files = "csv_files"
    if not os.path.exists(csv_files):
        os.mkdir(csv_files) #folder creation
    en_tete = ["product_page_url","title","price_including_tax","price_excluding_tax","universal_product_code","number_available","category","review_rating","image_url","product_description"]
    with open( csv_files + "\\" + csv_name + ".csv", "a", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=";")
        writer.writerow(en_tete)
        for i in all_book_information_for_one_category:
            writer.writerow(i)


list_links_all_categories = collect_links_all_categories(url_site)

list_links_all_books =  collect_url_all_books(url_site)