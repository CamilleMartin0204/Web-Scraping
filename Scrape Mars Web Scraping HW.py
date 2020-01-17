#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 

def scrape():
    with Browser(headless=True) as browser:
        returnDictionary = {}

        # Get the latest NASA news
        browser.visit('https://mars.nasa.gov/news/')        
        html_doc = browser.html

        soup = BeautifulSoup(html_doc, 'html.parser')

        news_p = soup.find_all(class_='article_teaser_body')[0].get_text()
        soup.head
        news_title = soup.find_all(class_='content_title')[0].a.get_text()

        #print(news_title)
        #print(news_p)
        returnDictionary["news_title"] = news_title
        returnDictionary["news_p"] = news_p

        # Get the featured image on JPL
        browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

        listOfButtons = browser.find_by_css('.button.fancybox')
        fullImageButton = listOfButtons.first
        fullImageButton.click()

        imageElement = browser.find_by_css('.fancybox-image').first
        featured_image_url = imageElement._element.get_attribute('src')

        #print(featured_image_url)
        returnDictionary["featured_image_url"] = featured_image_url

        # Get the weather on Mars
        browser.visit('https://twitter.com/marswxreport?lang=en')

        tweetElement = browser.find_by_css('.TweetTextSize.TweetTextSize--normal.js-tweet-text.tweet-text').first

        mars_weather = tweetElement.text

        #print(mars_weather)        
        returnDictionary["mars_weather"] = mars_weather

        # Get facts about Mars
        browser.visit('https://space-facts.com/mars/')

        tableElement = browser.find_by_css('.tablepress.tablepress-id-p-mars').first
        tableParent = tableElement.find_by_xpath('..')

        marsDataFrame = pd.read_html(tableParent.html)
        mars_facts = marsDataFrame[0].to_html()

        #print(mars_facts)
        returnDictionary["mars_facts"] = mars_facts

        # Get the hemispheres images
        hemisphere_image_urls = []

        rootUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(rootUrl)

        hemisphereLinks = browser.find_by_css('.itemLink.product-item')    
        totalLinks = len(hemisphereLinks)

        links_to_follow = set()
        for currentLink in hemisphereLinks:
            link_url = currentLink._element.get_attribute('href') 
            if link_url not in links_to_follow:
                links_to_follow.add(link_url)

        for hemi in links_to_follow:
            browser.visit (hemi)

            allLinks = browser.find_by_tag('a')
            hemi_img_url = ""
            for linkElement in allLinks:
                if linkElement._element.text == 'Sample':
                    hemi_img_url = linkElement._element.get_attribute('href') 
                    break

            hemi_name = browser.find_by_css('.title').first.text

            hemisphere_image_urls.append({"title" : hemi_name.replace(" Enhanced", ""), "img_url" : hemi_img_url})

        #print(hemisphere_image_urls)
        returnDictionary["hemisphere_image_urls"] = hemisphere_image_urls

        return returnDictionary

