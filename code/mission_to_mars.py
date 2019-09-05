#!/usr/bin/env python
# coding: utf-8

# # Homework 12 - Web scraping
# ## Mission to mars

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News
# Scrape and get NASA latest news

# In[3]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url) 


# In[4]:


html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')


# In[5]:


news_title = news_soup.find('div', class_='content_title')
nasa_news_title = news_title.get_text()
nasa_news_title


# In[6]:


news_body_title = news_soup.find('div', class_='article_teaser_body')
nasa_news_body = news_body_title.get_text()
nasa_news_body


# ### JPL Mars Space Images - Featured Image

# In[7]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[8]:


found_img= browser.find_by_id("full_image")
found_img.click()


# In[10]:


more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()


# In[11]:


html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')


# In[12]:


img_url_rel = img_soup.select_one('figure.lede a img').get("src")
featured_image_url = f'https://www.jpl.nasa.gov{img_url_rel}'
featured_image_url


# ### Mars Weather

# In[13]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html
weather_soup = BeautifulSoup(html, 'html.parser')


# In[16]:


mars_weather_tmp = weather_soup.select_one('div.js-tweet-text-container p')
mars_weather = mars_weather_tmp.get_text()


# ### Mars Facts 
# Get Mars number

# In[17]:


url = 'https://space-facts.com/mars/'
browser.visit(url)


# In[18]:


html = browser.html
fact_soup = BeautifulSoup(html, 'html.parser')
fact_soup


# In[19]:


legend= fact_soup.find_all('td' , class_='column-1')
data = fact_soup.find_all('td' , class_='column-2')

print(legend )
print()
print(data)


# In[20]:


legend_text = []

for i in range(len(legend)):
    legend_text.append(legend[i].text)
    
print(legend_text)
len(legend_text) 


# In[21]:


data_text = []

for i in range(len(data)):
    data_text.append(data[i].text)
    
print(data_text)
len(data_text)


# In[22]:


table = pd.DataFrame()
table['data_label '] = legend_text
table['data'] = data_text
table


# #### other method usind pandas

# In[23]:


df =  pd.read_html(url)
df


# In[24]:


Mars_earth_table_df = df[0]
Mars_earth_table_df


# In[25]:


Mars_table_df = df[1]
Mars_table_df


# ### Mars Hemispheres

# In[26]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[27]:


img_info=[]
links = browser.find_by_css("a.product-item h3")
len(links)


# In[28]:


for i in range(len(links)):
    print(links[i].text)


# In[31]:


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
    
    # For some reason, there is no "back" button on the image page
    # I reloaded the home page to get the link of other image
    browser.visit(url)
    browser.find_by_css("a.product-item h3")[i].click()
    
    


# In[32]:


img_info


# In[ ]:




