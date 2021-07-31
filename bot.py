from bs4 import BeautifulSoup
from requests import get
import re
from datetime import date, datetime
import time;
import sqlite3



# SAVE TO XML/ CSC send to email

BASE_URL = 'https://www.vinted.pl/ubrania?brand_id[]=9&catalog[]=1816&size_id[]=208&color_id[]=3'


USER_BRANDS = ['zara']

class VintedBot:

    def __init__(self, base_url, user_brand, user_size, user_price):
        self.base_url = base_url
        self.user_brand  = user_brand
        self.user_price = user_price
        self.ts  = ts = int(time.time())
        self.conn = sqlite3.connect('ubrania.db')
        self.curr = self.conn.cursor()
        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS clothes (link TEXT, num REAL)""")
        
    

    
    def check_user(self, brands, prices, sizes):
        number_of_right_element = 0
        for brand in self.user_brand:
            #print(sizes)
            num_of_elements = brands.count(brand)
            print(num_of_elements)
            if num_of_elements >= 2:
                for clothe, size in  zip(brands, sizes):
                    if clothe == brand and size == 'M':
                        number_of_right_element += 1
        return number_of_right_element

    def get_links(self, URL):
        page = get(URL)
        bs = BeautifulSoup(page.content, 'html.parser')
        soup = str(bs)
        string = '"is_favourite":false,"is_hated":false},"url":"'
        a = [m.start() for m in re.finditer(string, soup)]

        links = []
        for j in range(len(a)):
            start = a[j] + 46
            finish = 0
            for i in range(start + 1, start + 1000):

                # print(i)
                if soup[i] == '"':
                    finish = i
                    break

            links.append(soup[start:finish])
        return links  

    def get_arr(self, URL):
        page = get(URL)
        bs = BeautifulSoup(page.content, 'html.parser')
        soup = bs.find('div', class_='row items-list')

        prices = []
        brands = []
        sizes = []
        for price, brand, size in zip(soup.find_all('div', class_='item-box__title'),
                                    soup.find_all('a', class_='item-box__brand'),
                                    soup.find_all('div', class_='u-ui-margin-right-small')):
            size = size.get_text()

            price = price.get_text().strip().split(',')[0]
            brand = str(brand)
            for i in range(41, 51):
                if brand[i] == '"':
                    break

            brand = brand[40:i]
            prices.append(price)
            brands.append(brand)
            sizes.append(size)
        # print(prices)
        return brands, prices, sizes
    
    def start(self):
        prices = []
        brands = []
        sizes = []
        links = self.get_links(self.base_url)
        num_page = 1
        while len(links) != 0:

            URL = self.base_url + '&time=' + str(self.ts) + '&page=' + str(num_page)

            print(num_page)
            links = self.get_links(URL)

            for i, link in enumerate(links):
                brands, prices, sizes = self.get_arr(link)

                if self.check_user(brands, prices, sizes) > 3:
                    self.save_to_db(link,2)
                    print(link)
            num_page += 1

    def save_to_db(self,link, num):
        self.curr.execute('INSERT INTO clothes VALUES (?, ?)',(link, num))
        print('Dodano')
        print(self.curr.execute('SELECT * FROM clothes'))
        self.conn.commit()
        
    
    def close_conn(self):
        self.conn.close()











if __name__ == '__main__':
    bot = VintedBot(BASE_URL, ['zara'], 'M', 15)
    bot.start()
