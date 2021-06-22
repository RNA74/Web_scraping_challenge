from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

# Visit redplanetscience.com
    url = 'https://redplanetscience.com/'
    browser.visit(url)
 

    time.sleep(1)

    # Scrape page into Soup 
    html = browser.html
    news_soup = BeautifulSoup(html,'html.parser')


    # Get the new title
    quotes = news_soup.select_one('div.list_text')
    New_title =quotes.find('div',class_='content_title').get_text()

    # Get the new paragraph 
    News_p = quotes.find('div', class_= 'article_teaser_body').get_text()

    # JPL Mars Space Images - Featured Image
    # Visit the spaceimages-mars.com
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup 
    full_img_button = browser.find_by_tag('button')[1].click()

    # Scrape page into Soup 
    html = browser.html
    img_soup = BeautifulSoup(html,'html.parser')


    # Find the image for Mars
    images = img_soup.find('img', class_='fancybox-image').get('src')
    Mars_full_img = url + images

    # Mars Facts
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    time.sleep(1)

    ####Sort data in to a table

    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison ', 'Mars ', 'Earth']
    df.columns=['Description','Mars','Earth']
    df.set_index('Description', inplace=True)

    # Mars Hemispheres
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemi_img_url = []

    links = browser.find_by_css('a.product-item img')

    # Iterate through all links
    for i in range(len(links)):
        hemisphere = {}

        browser.find_by_css('a.product-item img')[i].click()

        link_elem = browser.links.find_by_text('Sample').first

        hemisphere['img_url']= link_elem['href']

        #Hemisphere title   
        hemisphere['title']= browser.find_by_css('h2.title').text

        #Append hemisphers list
        hemi_img_url.append(hemisphere)

        #Navigating
        browser.back()

    # Sort data in to a dictionary 
    Mars_data = {
        "New_title" : New_title,
        "full_img_button" : full_img_button,
        "Mars_full_img" : Mars_full_img,
        "hemisphere_images" : hemi_img_url['img_url'],
        "hemisphers_ titles" : hemi_img_url['title'],
    }

    # Close the browser after scraping
    browser.quit()


    # Return results

    return Mars_data



