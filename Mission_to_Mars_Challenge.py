#!/usr/bin/env python
# coding: utf-8

# In[101]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[102]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[103]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[104]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[105]:


slide_elem.find('div', class_='content_title')


# In[106]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[107]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[108]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[109]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[110]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[111]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[112]:


# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[113]:


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()


# In[114]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[115]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[139]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
browser.visit(url)


# In[140]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Find the HTML tag that holds all the links to the full-resolution images, or find a common CSS element for the full-resolution image.
html = browser.html
hemishpere_image_soup = soup(html, "html.parser")
hemishpere_links = hemishpere_image_soup.find_all("div", class_="item")

for item in hemishpere_links:
    
    # Dict to hold URLS
    hemispheres = {}
    
    # Get title
    result_title = item.find('h3').text
    
    # get parent link
    result_partial_link = item.find('div', class_="description").a["href"]
    # append base link + partial link 
    full_result_link = base_url + result_partial_link
    browser.visit(full_result_link)
    
    html = browser.html
    hemishpere_soup = soup(html, "html.parser")
    
    # Get HREF from Wide Image Wrapper
    full_image_url = hemishpere_soup.find('div', class_="wide-image-wrapper").a["href"]
#     full_image_url = hemishpere_soup.find('div', id="wide-image").a["href"]
    image_title = result_title
        
    # Add to Hemisphere dict
    hemispheres["img_url"] = full_image_url
    hemispheres["title"] = image_title
    print(hemispheres["img_url"])
    
    # append dict to hemispehere list
    hemisphere_image_urls.append(hemispheres)
    

    


# In[141]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[142]:


# 5. Quit the browser
browser.quit()


# In[ ]:




