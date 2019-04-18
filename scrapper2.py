from pprint import pprint
import sys
import json
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

# DB configurations
client = MongoClient()
db = client["TheHindu"]
col = None

# Scrapper configurations
base_url = "https://www.thehindu.com/"
collections = sys.argv[1:-1]
limit = int(sys.argv[-1])
print("Will scrape the articles in these sections:", collections)
print("Limit per section:", limit)

# Method for parsing the section
def parseCollections():
    for collection in collections:
        url = base_url + collection
        page = requests.get(url)
        if (page.status_code != 200):
            print("Error in fetching collection:", collection)
            continue
        print('Parsing collection:', collection)
        count = 0
        collected = []
        page_count = 0
        while(count <= limit):
            page_count += 1
            page_url = '{}/?page={}'.format(url, page_count)
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', class_="Other-StoryCard-heading")]
            for link in links:
                if(link in collected):
                    continue
                parseArticle(link)
                count += 1
                if (count > limit):
                    break
                collected.append(link)
        print('Number of articles parsed:', count-1)


# Method for parsing article page
def parseArticle(url):
    print("Parsing:", url)
    article = requests.get(url)
    soup = BeautifulSoup(article.content, 'html.parser')
    data = {}
    url_contents = url.split('/')
    data['tags'] = url_contents[3:-2]
    data['url'] = url
    title = soup.find_all('h1', class_='title')
    data['title'] = title[0].text.strip() if len(title) > 0 else ''
    intro = soup.find_all('h2', class_='intro')
    data['intro'] = intro[0].text.strip() if len(intro) > 0 else ''
    paras = [p.text.strip() for p in soup.find_all('div', class_='article')[0].find_all('p')]
    data['content'] = ' '.join(paras[:-3])
    data['time'] = paras[-2].split('|')[1].strip()
    author = soup.find_all('a', class_='auth-nm')
    data['author'] = author[0].text.strip() if len(author) > 0 else ''
    storeInDB(data)

def storeInDB(data):
    colname = data['tags'][0]
    col = db[colname]
    query = col.find({"url": data['url']})
    if (len(list(query)) > 0):
        return
    id = col.insert_one(data)
    print(id.inserted_id)


# Start crawler
parseCollections()

# python scrapper2.py education sport sci-tech elections entertainment life-and-style news children society 50