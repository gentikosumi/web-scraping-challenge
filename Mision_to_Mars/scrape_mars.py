


# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}


# Mars news

def scrape_news():
    try:

        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'

        # Retrieve page with the requests module
        response = requests.get(url)


        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')


        # Extract title text
        news = soup.find_all('div', class_="content_title")
        # print(len (news))
        
        news_title = soup.find('div', class_="content_title").find('a').text

        mars_info['news_title']= news_title       


        # Extract description text
        results = soup.find_all('div', class_="rollover_description_inner")
                
        news_p = soup.find('div', class_="rollover_description_inner").text

        mars_info['news_p']= news_p

        return mars_info
    
    finally:
        browser.quit()


def scrape_image():
    try:
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)


        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)


        # Retrieve page with the requests module
        response = requests.get(url)

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Examine the results, then determine element that contains sought info
        # print(soup.prettify())

        articles = soup.find_all('a', class_="fancybox")
        articles
        img_list = []
        url_list = []
        featured_image_url = []
        for article in articles:
            img_url = article["data-fancybox-href"]
            url_list.append(img_url)
            # print(url_list)

        featured_image = ['https://www.jpl.nasa.gov/' + url for url in url_list ]
        featured_image_url = featured_image[0]

        mars_info['featured_image_url'] = featured_image_url

        return mars_info
        
    finally:

        browser.quit()



    # __Mars Weather

def scrape_weather ():
    
    try:
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)

        # Retrieve page with the requests module
        response = requests.get(url)

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())

        # The latest Mars weather tweet from the page
        tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in tweets:
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                print(mars_weather)
                break
            else:
                pass

        mars_info['mars_weather'] = mars_weather

        return mars_info

    finally:
        browser.quit()


# Mars Facts

def scrape_facts():

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables

    mars_df = tables[0]
    mars_df.columns = ['Fact', 'Measurement']

    mars_df.set_index('Fact')
    mars_df

    facts = mars_df.to_html()
    mars_info['mars_facts'] = facts

    return mars_info
    

        # Mars hemisphere

def scrape_hemispheres ():
    try:

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)

        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)


        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())

        results = soup.find_all('div', class_="item")
        # print(results)

        # Store the main url
        base_url = 'https://astrogeology.usgs.gov'

        hemisphere_image_urls = []

        for result in results:
            # scrape the title 
            title = result.find('h3').text
    
    
            # Identify and return link to listing
            link = result.find('a', class_='itemLink product-item')['href']
    
            # Visit the link that contains the full image website 
            browser.visit(base_url + link)
    
            # HTML Object of individual hemisphere information website 
            link = browser.html
    
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( link, 'html.parser')
    
            # Retrieve full image source 
            img_url = base_url + soup.find('img', class_='wide-image')['src']
    
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

 
  
        mars_info['hemisphere_image_urls'] = hemisphere_image_urls

        return mars_info

    finally:

        browser.quit()

        



