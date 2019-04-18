from pprint import pprint
import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import sys

queue = set()
crawled = set()

starturl = "https://www.thehindu.com/"
limit = 10000

def parseLinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    for a in soup.find_all('a'):
        link = a.get('href')
        if(link and 'www.thehindu.com' in link and link not in crawled):
            links.add(link)
    return links

def processArticle(url):
    # print(url)
    pass

# def crawl():
#     while(len(crawled) <= limit):
#         url = queue.pop()
#         if(url[-4:] == ".ece"):
#             processArticle(url)
#         else:
#             links = parseLinks(url)
#             queue = queue | links
# 
# def startCrawl():
#     queue.add(starturl)
#     crawl()
# 
# startCrawl()

queue.add(starturl)

while(len(crawled) <= limit):
    url = queue.pop()
    crawled.add(url)
    print(url)
    if(url[-4:] == ".ece"):
        processArticle(url)
    else:
        links = parseLinks(url)
        queue = queue | links


            
