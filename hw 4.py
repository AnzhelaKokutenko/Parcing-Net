import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30/r4sT761g-47'}
url ='https://lenta.ru/'
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
news = dom.xpath("//div[@class = 'span4']/div[@class = 'item' or @class = 'first-item']")

news_list = []
for new in news:
    one_new = {}
    name = str(new.xpath(".//a[contains (@href, '/news/')]/text()")).replace(u"\\xa0", u" ")
    link = new.xpath(".//a/@href")
    date = new.xpath(".//time[@class='g-time']/@title")


    one_new['name'] = name
    one_new['link'] = f'{url}{link[0]}'
    one_new['date'] = date
    one_new['source'] = url

    news_list.append(one_new)

pprint(news_list)

db = client['lenta']
news = db['news']

def database2(data):
    for i in data:
        test = news.find_one({'link': one_new['link']})
        if test is None:
           news.insert_one(i)

database2(news_list)
