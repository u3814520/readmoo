from pymongo import MongoClient
import os
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import os
import time

if not os.path.exists('./new_readmoo_user'):
    os.mkdir('./new_readmoo_user')

client = MongoClient(host='10.2.14.10',port=27017)
db = client.userstar
coll = db.userstar

ISBN = []
USER = []
USERSTAR = []
CONTENT = []
BOOKNAME = []
NISBN = []
NUSER = []
NUSERSTAR = []
NCONTENT = []
NBOOKNAME = []

for page in range(1, 5):
    bookurl = f'https://share.readmoo.com/review/all/{page}'
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    res = requests.get(bookurl, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    list = soup.find_all('ul', class_='review-list')

    for l in list:
        li = l.find_all('li')
        for u in li:
            users = u.find_all('span', class_='from-user')
            star = u.find_all('div', class_='owner-rating')[0]['data-score']
            contents = u.find('div', class_='review-content').text.strip()
            USERSTAR.append(star)
            CONTENT.append(contents)

            for b in users:
                user = b.find_all('a')[0]['title']
                USER.append(user)
                print(user)

    for i in range(0, 100):
        urls = soup.select('h5[class="book-title"] a')[i]['href']
        bookname = soup.select('h5[class="book-title"] a')[i].text
        BOOKNAME.append(bookname)
        newres = requests.get(urls, headers=headers)
        newsoup = BeautifulSoup(newres.text, 'lxml')
        try:
            bookisbn = newsoup.select('span[itemprop="ISBN"]')[0].text
            ISBN.append(bookisbn)
            print(bookisbn)
        except:
            ISBN.append('0')
    print(f'第{page}頁')
    time.sleep(10)

for up in range(len(BOOKNAME)):
    updata = coll.find_one({'$and': [{'BOOKNAME': BOOKNAME[up]}, {'USER': USER[up]}]})
    if updata == None:
        coll.insert_one({'ISBN': ISBN[up],'BOOKNAME': BOOKNAME[up],'USER': USER[up],'CONTENT': CONTENT[up],'USERSTAR': USERSTAR[up]})
        NISBN.append(ISBN[up])
        NBOOKNAME.append(BOOKNAME[up])
        NUSER.append(USER[up])
        NCONTENT.append(CONTENT[up])
        NUSERSTAR.append(USERSTAR[up])
        readmoo = pd.DataFrame(
            {'ISBN': NISBN, 'BOOKNAME': NBOOKNAME, 'USER': NUSER, 'CONTENT': NCONTENT, 'USERSTAR': NUSERSTAR})
        readmoo.to_csv("./new_readmoo_user/readmoo_user_1116.csv", encoding='utf-8-sig', index=False)
    else:
        pass

