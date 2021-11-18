from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import os
import time
import threading

if not os.path.exists('./new_readmoo_user'):
    os.mkdir('./new_readmoo_user')

def readmoo():
    ISBN = []
    USER = []
    USERSTAR = []
    CONTENT = []
    BOOKNAME = []


    for page in range(281, 301):
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

        # 新url取isbn
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
        if page%5 == 0:
            readmoo = pd.DataFrame({'ISBN': ISBN, 'BOOKNAME': BOOKNAME, 'USER': USER, 'CONTENT': CONTENT, 'USERSTAR': USERSTAR})
            readmoo.to_csv("./new_readmoo_user/readmoo_user_{}.csv".format(page), encoding='utf-8-sig', index=False)
            ISBN = []
            USER = []
            USERSTAR = []
            CONTENT = []
            BOOKNAME = []

t=threading.Thread(target=readmoo)
t.start()

for i in range(12):
    time.sleep(1)

t.join()
