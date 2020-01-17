#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 

with Browser() as browser:

    # Get the latest NASA news
    browser.visit('https://mars.nasa.gov/news/')        
    html_doc = browser.html

    soup = BeautifulSoup(html_doc, 'html.parser')

    news_p = soup.find_all(class_='article_teaser_body')[0].get_text()
    soup.head
    news_title = soup.find_all(class_='content_title')[0].a.get_text()

    print(news_title)
    print(news_p)

    # Get the featured image on JPL
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    listOfButtons = browser.find_by_css('.button.fancybox')
    fullImageButton = listOfButtons.first
    fullImageButton.click()

    imageElement = browser.find_by_css('.fancybox-image').first
    featured_image_url = imageElement._element.get_attribute('src')

    print(featured_image_url)

    # Get the weather on Mars
    browser.visit('https://twitter.com/marswxreport?lang=en')

    tweetElement = browser.find_by_css('.TweetTextSize.TweetTextSize--normal.js-tweet-text.tweet-text').first

    mars_weather = tweetElement.text

    print(mars_weather)

    # Get facts about Mars
    browser.visit('https://space-facts.com/mars/')

    tableElement = browser.find_by_css('.tablepress.tablepress-id-p-mars').first
    tableParent = tableElement.find_by_xpath('..')

    mars_facts = pd.read_html(tableParent.html)

    print(mars_facts)

    # Get the hemispheres images
    hemisphere_image_urls = []

    rootUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(rootUrl)

    hemisphereLinks = browser.find_by_css('.itemLink.product-item')    
    totalLinks = len(hemisphereLinks)
    print("Found " + str(totalLinks) + " links")

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

    print(hemisphere_image_urls)


# In[ ]:


ASA's Briefcase-Size MarCO Satellite Picks Up Honors
The twin spacecraft, the first of their kind to fly into deep space, earn a Laureate from Aviation Week & Space Technology.
https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA23170_ip.jpg
InSight sol 365 (2019-12-06) low -98.8ºC (-145.8ºF) high -21.5ºC (-6.8ºF)
winds from the SSW at 5.7 m/s (12.7 mph) gusting to 20.2 m/s (45.2 mph)
pressure at 6.60 hPa
[                      0                              1
0  Equatorial Diameter:                       6,792 km
1       Polar Diameter:                       6,752 km
2                 Mass:  6.39 × 10^23 kg (0.11 Earths)
3                Moons:            2 (Phobos & Deimos)
4       Orbit Distance:       227,943,824 km (1.38 AU)
5         Orbit Period:           687 days (1.9 years)
6  Surface Temperature:                   -87 to -5 °C
7         First Record:              2nd millennium BC
8          Recorded By:           Egyptian astronomers]
Found 8 links
[{'title': 'Cerberus Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
 

