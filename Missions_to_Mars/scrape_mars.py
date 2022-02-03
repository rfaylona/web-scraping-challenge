#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_data = {}

    # # NASA Mars News

    redplnt_url = "https://redplanetscience.com/"

    browser = init_browser()
    browser.visit(redplnt_url)
    time.sleep(4)
    soup = BeautifulSoup(browser.html, 'html.parser')

    news_title = soup.find_all("div", class_="content_title")[0].get_text()
    news_title

    news_paragraph = soup.find_all("div", class_="article_teaser_body")[0].get_text()

    browser.quit()

    # # JPL Mars Space Images - Featured Image

    jpl_url = 'https://spaceimages-mars.com'
    browser = init_browser()
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image = soup.find('img', class_="headerimage fade-in").get('src')
    featured_image_url = f"{jpl_url}/{featured_image}"

    browser.quit()

    # # Mars Facts

    mars_facts_url = "https://galaxyfacts-mars.com"
    mars_facts_df = pd.read_html(mars_facts_url)[1]

    mars_facts_df.columns = ["description", "value"]
    mars_facts_df["description"] = mars_facts_df["description"].str.replace(":","")

    mars_facts_df.set_index("description", inplace=True) 
    mars_facts_html = mars_facts_df.to_html()

    # # Mars Hemispheres

    hemispheres_url = 'https://marshemispheres.com/'

    browser = init_browser()
    browser.visit(hemispheres_url)

    hemispheres = ["Cerberus","Schiaparelli","Syrtis","Valles"]
    hemisphere_image_urls = []

    for hemi in hemispheres:
        new_dict = {}

        browser.click_link_by_partial_text(hemi)
        hemispheres_html = browser.html
        soup = BeautifulSoup(hemispheres_html, 'html.parser')
        new_dict["title"] = soup.find("h2").get_text().replace("Enhanced","").strip()
        img_url = soup.find_all("div", class_="downloads")[0].find_all("a")[0]["href"]
        new_dict["img_url"] = f'{hemispheres_url}{img_url}' 
        hemisphere_image_urls.append(new_dict)
    
        browser.back()



    browser.quit()

    mars_data = {
        "nasa_mars_title":news_title,
        "nasa_mars_paragraph":news_paragraph,
        "jpl_image":featured_image_url,
        "mars_facts":mars_facts_html,
        "mars_hemisphere":hemisphere_image_urls
    }

    return mars_data

if __name__ == "__main__":
    print(scrape())