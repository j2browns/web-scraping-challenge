#Setting up functions
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import scrape_mars

testing = scrape_mars.scrape()

print(testing)