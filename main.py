from typing import Union

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import cloudscraper
import dateutil.parser

app = FastAPI()


@app.get("/")
def read_root():
    return {"Go to api docs (eg. my-url/docs) and input rss feed url as query parameter"}


@app.get("/check")
def check_rssfeed_url(q: Union[str, None] = None):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    URL = q
    info = scraper.get(URL).text

    soup = BeautifulSoup(info, "xml")
    feeds = soup.find_all('item')
    feed_list = []
    for feed in feeds:
        feed_details = {}
        if feed.title.string:
            feed_details['title'] = feed.title.string
        else:
            feed_details['title'] = 'title not found'
        
        if feed.pubDate.string:
            feed_details['date'] =  dateutil.parser.parse(feed.pubDate.string)
        else:
            feed_details['date'] = 'date not found'
        
        if feed.link.string:
            feed_details['link'] = feed.link.string
            img_link = getimage(feed_details['link'], scraper)
            if img_link != 'image link not found':
                feed_details['image link'] = img_link
            else:
                feed_details['image link'] = 'image link not found'

        else:
            feed_details['link'] = 'link not found'
            
        feed_list.append(feed_details)
        print(feed_details)
    print(feed_list)
    return feed_list
        

def getimage(news_url, scraper):
    info = scraper.get(news_url).text
    soup = BeautifulSoup(info, "html.parser")
    try:
        image_prop = soup.head.find(property="og:image")
        image_link = image_prop.get('content')
        print("image retrieval successfull")
    except:
        image_link = 'image link not found'
        print("image retrieval not successfull")
    return image_link
