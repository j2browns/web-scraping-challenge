# web-scraping-challenge

### Homework 12 Web Scraping

This assignment scrapes Mars related information from the web from a variety of sources:

* NASA web site ("https://mars.nasa.gov/news/") - featured stories about Mars
* JPL mars image site ('http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars') - a Mars related Feature Image
* 'https://space-facts.com/mars/' - table of interesting information about Mars
* 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' - detailed images of Mars Hemispheres

The ability to extract the necessary information from these sites is first demonstrated in a jupyter notebook (mission_to_mars.ipynb).  The functional code
was then transferred into a function in a python program (scrape_mars).  The scraping function of this program is called from a Flask Server in the 
Python code app.py.  The Flask server calls index.html which is used to display the information scraped from the web.

Two image files are included: Final Screen Image 1 and Final Screen Image 2.  The final screen would not fit in one view (had to scroll down to see images).  Therefore split into two images. These combined are the final screen.
