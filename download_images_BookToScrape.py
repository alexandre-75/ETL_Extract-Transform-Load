import requests
from bs4 import BeautifulSoup
import os

url_site = "http://books.toscrape.com/index.html"

list_links_all_categories =[]
list_links_images = []
 
def requests_beautifulsoup_url (url): # Get the url and analyse its html

    requests_url = requests.get(url)
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

list_links_all_categories = collect_links_all_categories(url_site)

def download_url_images (url_category):

    def number_of_pages_in_category (url_category): # get number of pages in category

        requests_beautifulsoup = requests_beautifulsoup_url(url_category)
        if requests_beautifulsoup.find(name="li", attrs={"class":"current"}) == None:
            number_of_pages = 1
        else:
            number_of_pages = int(requests_beautifulsoup.find(name="li", attrs={"class":"current"}).text.split()[3])
        return number_of_pages

    def url_images (setting):

        list_all = []
        for i in list_links_all_categories :
            number_of_pages_2 = number_of_pages_in_category(i)    
            for r in range(number_of_pages_2):
                url_page_categorie = i.replace("index",f"page-{r+1}") # recovery of the correct url for categories containing several pages
                if (r == 0): # if the category contains only one page
                    url_page_categorie = i
                requests_beautifulsoup = requests_beautifulsoup_url(url_page_categorie)               
                div_tags = requests_beautifulsoup.find_all(name="div", attrs={"class":"image_container"})
                for div in div_tags:
                    collect_img_tags = div.find_all("img") # collect all "img" tags
                    #print(collect_img_tags)
                    for img in collect_img_tags :
                        image_url = img["src"].strip("../..") # retrieve the link in the tag, and remove the unwanted
                        image_url_2 = "http://books.toscrape.com/" + image_url # get an active link
                        list_all.append(image_url_2)  # add the active link in the list

        return list_all
    return url_images(url_category)

list_links_images = download_url_images(url_site)
 
def folder_create (folder_name, list_link_img):
    try:
        os.mkdir(folder_name)
        for i, url in enumerate(list_link_img) :
            file_name = folder_name +"\\"+ f'image_{i}.jpg'   
            img_data = requests.get(url, verify=False)
            with open (file_name, 'wb') as handler:
                handler.write(img_data.content)
    except Exception as inst:
        print(inst)
    
folder_create("images_BookToScrape", list_links_images)