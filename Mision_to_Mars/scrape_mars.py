


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

def scrape():
    browser = init_browser()
    listings = {}



    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # Extract title text
    news = soup.find_all('div', class_="content_title")
    print(len (news))


    # A blank list to hold the headlines
    news_title = []
    # Loop over div elements
    for new in news:
        # If new element has an anchor...
        if (new.a):
            # And the anchor has non-blank text...
            if (new.a.text):
                
                news_title.append(new)


    # Print only the headlines
    for x in range(6):
        print(news_title[x].text)        


    # Extract description text
    results = soup.find_all('div', class_="rollover_description_inner")
    print(results)

    # A blank list to hold the descriptions
    news_p = []
    # Loop over div elements
    for result in results:
        if (result.text):
        # Append the description to the list
            news_p.append(result)

    # Print only the description
    for x in range(6):
         print(news_p[x].text)



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
    #   print(url_list)

    featured_image_url = ['https://www.jpl.nasa.gov/' + url for url in url_list ]
    featured_image_url

    # __Mars Weather__

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    results = soup.find_all('p', class_="TweetTextSize")
    print(len (results))

    mars_tweet = []
    # Loop over div elements
    for result in results:
        if (result.text):
        # Append the description to the list
            mars_tweet.append(result)

    # Print only the tweets
    for x in range(20):
        print("------")
        print(mars_tweet[x].text)

    # The latest Mars weather tweet from the page
    mars_weather = mars_tweet[6].text
    print(mars_weather.strip("\n"))

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables

    mars_df = tables[0]
    mars_df.columns = ['Fact', 'Measurement']
    mars_df

    serie = pd.Series(mars_df['Fact'])
    mars_df['Fact'] = serie.str.strip(":")
    mars_df = mars_df.set_index('Fact')
    mars_df

    mars_facts = mars_df.to_html('mars_facts.html')
    mars_facts

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    results = soup.find_all('div', class_="description")
    print(results)

    base_url = 'https://astrogeology.usgs.gov'
    titles = []
    next_urls = []

    for result in results:
        # scrape the title 
        hem_title = result.find('h3').text
        titles.append(hem_title)
    
        # Identify and return link to listing
        link = result.a['href']
        hem_link = base_url + link
        next_urls.append(hem_link)
    

    titles
    next_urls

    img_url = []

    for next_url in next_urls:
        url = next_url
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_link = soup.find('img', class_="wide-image")
        final = img_link['src']
        img_final = base_url + final
        img_url.append(img_final)

    img_url    

    hemisphere_image_urls = []

    for i in range(max((len(titles), len(img_url)))):
    
        g = {titles[i]: img_url[i]}
        hemisphere_image_urls.append(g)
 
  
    hemisphere_image_urls

    return listings     





