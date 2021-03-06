from bs4 import BeautifulSoup
from requests import get
import re
import time
import sqlite3
import csv






class VintedBot:
    def __init__(
        self, base_url, user_brand, user_size, user_price, user_number_of_clothes
    ):
        self.base_url = base_url  # URL for searching
        self.user_brand = user_brand  # brands for searching
        self.user_price = user_price  # max price
        self.user_size = user_size  # size for searching
        self.user_number_of_clothes = user_number_of_clothes
        self.ts = ts = int(time.time())
        self.curr, self.conn = self.connect_db()

    # connecting to database
    def connect_db(self):
        conn = sqlite3.connect("clothes.db")
        curr = conn.cursor()
        curr.execute(
            """
        CREATE TABLE IF NOT EXISTS clothes (user TEXT, num INTEGER, link TEXT)"""
        )
        return curr, conn

    # check if user has more mathing searching clothes
    def check_user(self, brands, prices, sizes, link):
        number_of_right_element = 0
        for brand in self.user_brand:
            num_of_elements = brands.count(brand)
            if num_of_elements >= self.user_number_of_clothes:
                for clothe, size, price in zip(brands, sizes, prices):
                    if (
                        clothe == brand
                        and size == self.user_size
                        and price <= self.user_price
                    ):
                        number_of_right_element += 1
        if number_of_right_element >= self.user_number_of_clothes:
            username = self.get_username(link)
            return username, number_of_right_element
        return False, False

    # getting offers link from vinted page
    def get_links(self, URL):

        page = get(URL)
        bs = BeautifulSoup(page.content, "html.parser")
        soup = str(bs)
        with open("hello.html", "w") as f:
            f.write(soup)
        # change to regex
        pattern = '"is_hated":false},"url":"(.*?)","a'
        links = [x.group(1) for x in re.finditer(pattern, soup)]
        return links

    # getting array with prices, brands, and clothes sizes
    def get_arr(self, URL):
        page = get(URL)
        bs = BeautifulSoup(page.content, "html.parser")
        soup = bs.find("div", class_="row items-list")

        prices = []
        brands = []
        sizes = []
        for price, brand, size in zip(
            soup.find_all("div", class_="item-box__title"),
            soup.find_all("a", class_="item-box__brand"),
            soup.find_all("div", class_="u-ui-margin-right-small"),
        ):
            size = size.get_text()
            
            price = int(price.get_text().rstrip("'").replace(" ", "").split(",")[0])
            brand = str(brand)
            i = 41
            for i in range(41, 51):
                if brand[i] == '"':
                    break

            brand = brand[40:i]
            prices.append(price)
            brands.append(brand)
            sizes.append(size)
        return brands, prices, sizes

    # start bot 
    def start(self):
        print("brand", type(self.user_brand))
        print("num", type(self.user_number_of_clothes))
        print("price", type(self.user_price))
        print("size: ", type(self.user_size))
        prices = []
        brands = []
        sizes = []
        links = self.get_links(self.base_url)
        num_page = 1
        while len(links) != 0:
            print(num_page)
            URL = self.base_url + "&time=" + str(self.ts) + "&page=" + str(num_page)

            links = self.get_links(URL)

            for i, link in enumerate(links):
                brands, prices, sizes = self.get_arr(link)
                username, number_of_right_element = self.check_user(
                    brands, prices, sizes, link
                )
                if username != False:
                    self.save_to_db(link, number_of_right_element, username)

            num_page += 1
        self.close_conn()

    # save found user to database
    def save_to_db(self, link, num, username):
        # print(username)
        self.curr.execute("SELECT user FROM clothes WHERE user = ?", (username,))
        row = self.curr.fetchone()

        if row is None:
            self.curr.execute(
                "INSERT INTO clothes VALUES (?, ?, ?)",
                (
                    username,
                    num,
                    link,
                ),
            )
            self.conn.commit()
            print(f"Dodano {username}")

    # save database to csv file
    def save_to_csv(self):
        data = self.conn.execute("SELECT * FROM clothes")
        with open("data.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["user", "num", "link"])
            writer.writerows(data)

    # getting username from vintedpage
    def get_username(self, link):
        page = get(link)
        bs = BeautifulSoup(page.content, "html.parser")
        # print(link)
        page_string = bs.prettify()
        user = re.search('path":"\/member\/\d{5,7}\-(.*?)","i', page_string).group(1)

        return user


    # close connection
    def close_conn(self):
        self.conn.close()


if __name__ == "__main__":
    bot = VintedBot(BASE_URL, ["zara", "medicine", "mango"], "M", 15, 2)
    bot.save_to_csv()
