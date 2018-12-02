def scrape():
    # coding: utf-8
    #import dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from datetime import datetime

    #Create empty dictionary
    mars_dict={}

    # Initialize browser
    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser("chrome", **executable_path, headless=False)

    #create function to start scraping
    def scrape_start(url1):
        # Initialize browser
        browser = init_browser()
        # Visit Nasa.gov news website  
        browser.visit(url1)
        # Scrape page into soup
        html = browser.html
        global soup
        soup = BeautifulSoup(html, "html.parser")

    #scrape news 
    def scrape_news(url):
        scrape_start(url1=url)
        soup1=soup
        res = soup1.find("section", class_="grid_gallery module list_view")
        #print (res.prettify())
        #Identify and return first news title
        news_title = res.find('div', class_="content_title").a.text
        #Identify and return first news paragraph
        news_p = res.find('div', class_="article_teaser_body").text
        print(news_title)
        print (news_p)
        #Add to dictionary
        mars_dict["news_title"]=news_title
        mars_dict["news_p"]=news_p
        return mars_dict
        
    scrape_news(url="https://mars.nasa.gov/news")

    #scrape jpl image (large)
    def scrape_img(url):
        #Scrape main page
        scrape_start(url1=url) #Call scraping start function
        soup1=soup
        res1 = soup1.find('a', class_="button fancybox") #get url behind 'Full Image' button on main page
        #create link to detailed page with large image
        url2="https://www.jpl.nasa.gov" + res1["data-link"]

        #Scrape page with large (full size) image
        scrape_start(url1=url2) #Call scraping start function
        soup_img=soup
        res_img=soup_img.find('figure', class_="lede").find('a').get('href') #get url for large sized image
        featured_image_url="https://www.jpl.nasa.gov" + res_img
        print (featured_image_url)
        #Add to dictionary
        mars_dict["featured_image_url"] = featured_image_url
        return mars_dict

    scrape_img(url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    #scrape tweet for weather
    def scrape_tweet(url):
        #Call scraping start function
        scrape_start(url1=url)
        soup1=soup
        # Find section
        res = soup.find("div", class_="js-tweet-text-container")
        
        #Identify and return first Mars weather tweet
        mars_weather = res.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        print (mars_weather)
        #Add to dictionary
        mars_dict["mars_weather"] = mars_weather
        return mars_dict
        
    scrape_tweet(url="https://twitter.com/marswxreport?lang=en")

    #scrape table
    url="http://space-facts.com/mars/"
    tables = pd.read_html(url)
    df=pd.DataFrame({'fact':tables[0][0],'value':tables[0][1]})
    table_html=df.to_html()
    table_html
    #Add to dictionary
    mars_dict["table_html"] = table_html

    #scrape hemisphere image urls
    def scrape_hem(url):
        #Scrape main page
        scrape_start(url1=url) #Call scraping start function
        soup1=soup
        res1 = soup1.find_all('div', class_="description") #get url behind 'Full Image' button on main page
        hemisphere_image_urls=[]
        for r in res1:
            d = {}
            name=r.a.h3.text.replace(" Enhanced","")
            link=r.a.get('href')
            #create link to detailed page with large image
            url2="https://astrogeology.usgs.gov" + link
            #Scrape page with large (full size) image
            scrape_start(url1=url2) #Call scraping start function
            soup_img=soup
            res_img=soup_img.find('div', class_="downloads").find('ul').find('li').find('a').get('href')
            img_url=res_img
            d['title'] = name
            d['img_url']=img_url
            hemisphere_image_urls.append(d)
        print (hemisphere_image_urls)
        mars_dict["hemisphere_image_urls"] = hemisphere_image_urls
        return mars_dict

    scrape_hem(url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    return mars_dict

    #get_ipython().system('jupyter nbconvert --to script config_template.ipynb')

