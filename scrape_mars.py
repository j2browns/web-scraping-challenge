#Setting up functions
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time

def scrape():
    ###########################################################################################################
    ##########################Code for getting featured stories from NASA mars mission site####################
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

    ############################################################################
    #############Code for getting featured mars image from JPL site#############
    #setup for splinter
    executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_images = soup.find_all('footer')
    test_1 = mars_images[0].find('a', class_='button fancybox')["data-fancybox-href"]
    image = test_1
    image_link = "http://www.jpl.nasa.gov"+image
    print(image_link)
    browser.quit()

    ###############################################################
    #######Getting information table from Space-Facts##############
    #setup for splinter
    executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)
    #tables is a list of dataframes.  Inspection found table[0] is desired one.
    mars_facts = tables[0].copy()
    mars_facts.rename(columns = {0:"Parameter", 1:"Value"}, inplace=True) #renaming headings so make sense.
    mars_html = mars_facts.to_html(index = False)
    browser.quit()

    #############################################################################################
    #########Getting information from Astrogeology Site - link to image page and title###########
    #setup for splinter
    executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2) #added delay to make sure loads OK without issues
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    base_url = "https://astrogeology.usgs.gov" #base to add on to hemisphere page in next section
    results = soup.find_all('div', class_='description')

    hemisphere=[] #variable to hold hemisphere information

    for result in results:
        try:
            test = result.find('a')["href"]#image page link from this location
            name = result.find('h3').text #name of image
            combine_url = base_url+test#add base to image location for next section where get image
            hemisphere.append({"title":name, "img_url":combine_url})
        except AttributeError as e:
            print(e)
    browser.quit()

    ############Taking links from above and opening to get images##########################
    #setup for splinter
    link=[] #variable to hold final link name
    for i in range(0,len(hemisphere)):
        executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=True)
        url = hemisphere[i]['img_url']
        browser.visit(url)
        time.sleep(2) #added delay to make sure loads OK without issues

        html_1 = browser.html

        #stepping through various levels in html to get to link
        soup_1 = BeautifulSoup(html_1, 'html.parser')
        test = soup_1.find('div', class_ = 'container')
        test_1 = test.find('div', class_= 'downloads')
        test_2 = test_1.find('ul')
        test_3 = test_2.find_all('li')
        link.append(test_3[0].find('a')["href"]) #first list element is desired link, second is for Tiff that does not open correctly
        browser.quit()

    #below replaces hemisphere page link with hemisphere image link
    for i in range(0,len(hemisphere)):
        hemisphere[i]["img_url"]=link[i]

    print(hemisphere)
    print('************************')


    #creating output dictionary
    output_dictionnary = {}
    output_dictionnary = {"Title":nasa_list[0]["Nasa_Title"],"Text":nasa_list[0]["Nasa_Text"]}
    output_dictionnary["Featured_Image"] = image_link
    output_dictionnary["Mars_Table"] = mars_html
    output_dictionnary.update({"Hemi_0":hemisphere[0]["title"],"Hemi_0_Img":hemisphere[0]["img_url"]})
    output_dictionnary.update({"Hemi_1":hemisphere[1]["title"],"Hemi_1_Img":hemisphere[1]["img_url"]})
    output_dictionnary.update({"Hemi_2":hemisphere[2]["title"],"Hemi_2_Img":hemisphere[2]["img_url"]})
    output_dictionnary.update({"Hemi_3":hemisphere[3]["title"],"Hemi_3_Img":hemisphere[3]["img_url"]})

    print("Output Dictionnary:")
    print(output_dictionnary)
    return output_dictionnary
