from bs4 import BeautifulSoup
from requests import get
import re
import time
import sqlite3
import csv

# SAVE TO XML/ CSC 
# send to email
#brak rzeczy
#multitreading
# obserwacja osób ktore mają przedmitoy
BASE_URL = 'https://www.vinted.pl/ubrania?search_text=house&search_id=471276307&catalog[]=2050&brand_id[]=11'

USER_BRANDS = ['zara']


class VintedBot:

    def __init__(self, base_url, user_brand, user_size, user_price,user_number_of_clothes):
        self.base_url = base_url
        self.user_brand = user_brand
        self.user_price = user_price
        self.user_size = user_size
        self.user_number_of_clothes = user_number_of_clothes
        self.ts = ts = int(time.time())
        self.curr, self.conn  = self.connect_db()
        
    def connect_db(self):
        conn = sqlite3.connect('ubrania.db')
        curr = conn.cursor()
        curr.execute("""
        CREATE TABLE IF NOT EXISTS clothes (user TEXT, num INTEGER, link TEXT)""")
        return curr, conn


    def check_user(self, brands, prices, sizes,link):
        number_of_right_element = 0
        for brand in self.user_brand:
            num_of_elements = brands.count(brand)
            if num_of_elements >= self.user_number_of_clothes:
                for clothe, size, price in zip(brands, sizes, prices):
                    if clothe == brand and size == self.user_size and price <= self.user_price:
                        number_of_right_element += 1
        if number_of_right_element >= self.user_number_of_clothes:
            username  = self.get_username(link)
            return username, number_of_right_element
        return False, False


    def get_links(self, URL):
        
        page = get(URL)
        bs = BeautifulSoup(page.content, 'html.parser')
        soup = str(bs)
        with open('hello.html', 'w') as f:
            f.write(soup)
        # change to regex
        pattern = '"is_hated":false},"url":"(.*?)","a'
        links = [x.group(1) for x in re.finditer(pattern, soup)]
        print(links)
        time.sleep(10)
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

            price = int(price.get_text().rstrip("'").split(',')[0])
            brand = str(brand)
            i =41
            for i in range(41, 51):
                if brand[i] == '"':
                    break

            brand = brand[40:i]
            prices.append(price)
            brands.append(brand)
            sizes.append(size)
        return brands, prices, sizes

    def start(self):
        prices = []
        brands = []
        sizes = []
        links = self.get_links(self.base_url)
        num_page = 1
        while len(links) != 0:
            print(num_page)
            URL = self.base_url + '&time=' + str(self.ts) + '&page=' + str(num_page)

            links = self.get_links(URL)

            for i, link in enumerate(links):
                brands, prices, sizes = self.get_arr(link)
                username, number_of_right_element = self.check_user(brands, prices, sizes, link)
                if(username != False):
                    self.save_to_db(link, number_of_right_element,username)

                
            num_page += 1
        self.close_conn()


    def save_to_db(self, link, num, username):
        
        self.curr.execute('SELECT user FROM clothes WHERE user = ?', (username,))
        row = self.curr.fetchone()
        if row is None:
            self.curr.execute('INSERT INTO clothes VALUES (?, ?, ?)', (username, num,link,))
            self.conn.commit()
    
    def save_to_csv(self):
        data = self.conn.execute('SELECT * FROM clothes')
        with open('data.csv', 'w' ) as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'num', 'link'])
            writer.writerows(data)


    def get_username(self,link):
        page = get(link)
        bs = BeautifulSoup(page.content, 'html.parser')
        page_string  = bs.prettify()
        user = re.search('path":"/member/\d{6,7}\-(.*?)","i', page_string).group(1)
        return user



    def close_conn(self):
        self.conn.close()


if __name__ == '__main__':
    bot = VintedBot(BASE_URL, ['house'], 'M', 100, 1)
    bot.start()
