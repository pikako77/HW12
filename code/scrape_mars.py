from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
import time
import requests

def scrape_all():

    # Initiate headless driver for deployment
    #browser = init_browser()

    # Run all scraping functions and store in dictionary.
    # data = {
    #     "news_title": news_title,
    #     "news_paragraph": news_paragraph,
    #     "featured_image": featured_image(browser),
    #     "hemispheres": hemispheres(browser),
    #     "weather": twitter_weather(browser),
    #     "facts": mars_facts(),
    #     "last_modified": dt.datetime.now()
    # }
    news_title, news_paragraph = get_news()

    data = {}


    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": get_img_url() ,
        
        "weather": get_weather(),
        "facts": get_fact_table(),
        "hemispheres":get_hemi_url()
        #"last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    #browser.quit()
    return data

# def scrape():
#     scrape_dict ={}

#     #print ("Scrapping news ...")
#     scrape_dict = {"news", get_news()}

#     #print ("Scrapping Mars image ...")
#     scrape_dict.update(get_img_url())

#     #print ("Scrapping weather ...")
#     scrape_dict.update(get_weather())

#     #print ("Scrapping fact table ...")
#     scrape_dict.update(get_fact_table())

#     #print ("Scrapping hemisphere url ...")
#     scrape_hemi= get_hemi_url()

#     return scrape_dict,scrape_hemi


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#--------------------------------
# get news title and body
def get_news():
    # get news
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url) 

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title')
    nasa_news_title = news_title.text
    news_body_title = news_soup.find('div', class_='article_teaser_body')
    nasa_news_body = news_body_title.text

    # nasa_news_dict = {"title": nasa_news_title , 
    #                   "news_text" : nasa_news_body}

    browser.quit()
    #return nasa_news_dict
    return nasa_news_title,nasa_news_body

#--------------------------------
# get Mars image url
def get_img_url():
    #img_dict = {}

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)

    found_img= browser.find_by_id("full_image")
    found_img.click()
    time.sleep(5)

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    featured_image_url = f'https://www.jpl.nasa.gov{img_url_rel}'

   # img_dict ={'Mars_img_url': featured_image_url}

    browser.quit()
    #return img_dict
    return featured_image_url

#--------------------------------
# get weather tweet. Last one is a no data comment
# Get one before last
def get_weather():
    #weather_dict = {}

    browser = init_browser()

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    
    ## last tweet. Uncomment when radar are back
    #mars_weather = weather_soup.select_one('div.js-tweet-text-container p').get_text()
    #mars_weather
    ## End - last tweet. Uncomment when radar are back

    # One before last tweet -> comment when radars are back
    mars_weather = weather_soup.find_all('p',class_="tweet-text")[3].text
    # End  - One before last tweet -> comment when radars are back
    
    #weather_dict = {"weather" : mars_weather}

    browser.quit()

   # return weather_dict
    return mars_weather



#--------------------------------
# get fact table
def get_fact_table():
    #fact_dict = {}


    url = 'https://space-facts.com/mars/'
    df =  pd.read_html(url)

    Mars_table_df = df[1]
    Mars_table_df.columns = ['Description', 'Value']
    #Mars_table_df.set_index('Description', inplace = True)
    html_fact_table_df = Mars_table_df.to_html(header = True, index = False)
    #fact_dict={"fact_table":Mars_table_df}

    #return fact_dict
    return html_fact_table_df


#--------------------------------
# get hemisphere img url
def get_hemi_url():
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    img_info=[]
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}  
    
        # For some reason, there is no "back" button on the image page
        # I reloaded the home page to get the link of other image
        browser.visit(url)
        browser.find_by_css("a.product-item h3")[i].click() 
    
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
        # click on "sample"
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
      
        img_info.append(hemisphere)
    
    browser.quit()

    #return img_info
    return img_info

    

############
## main
# main_dict,url_list = scrape_all()
#main_dict = scrape_all()
#print(main_dict)
# print()
# print(url_list)