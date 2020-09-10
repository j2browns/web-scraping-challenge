#Setting up functions
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time

def scrape()

##########################Code for getting featured stories from NASA mars mission site#####################
# NASA mars site information
#using request and soup
nasa_url = "https://mars.nasa.gov/news/"
nasa_response = requests.get(nasa_url)

################ Create BeautifulSoup object; parse with 'html.parser' ###############
nasa_soup = BeautifulSoup(nasa_response.text, 'lxml')

# results are returned as an iterable list
nasa_results = nasa_soup.find_all('div', class_="slide")
nasa_list = []
for result in nasa_results:
     # Error handling
    try:
        # Identify and return title and URL
        title = result.find('div', class_="content_title").text
        text = result.find('div', class_="rollover_description_inner").text

        # Print results only if title, price, and link are available
        if (title and text):
            nasa_list.append({"Nasa_Title":title.replace("\n",""),"Nasa_Text":text.replace("\n","")})

    except AttributeError as e:
        print(e)

#####Code for getting featured mars image from JPL site######

#setup for splinter
executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit/'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
mars_images = soup.find_all('li', class_='slide')
#print(mars_image)
i=0
n=2
mars_images_url = []
for mars_image in mars_images:
    image_link = mars_image.find('a')["data-fancybox-href"]
    mars_images_url.append(image_link)
    i+=1
    if i == n:
        break
browser.quit()

#######Getting information table from Space-Facts######