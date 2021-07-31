from bs4 import BeautifulSoup
from requests import get
import re
from datetime import date, datetime
import time;

BASE_URL = 'https://www.vinted.pl/ubrania?brand_id[]=9&catalog[]=1816&size_id[]=208&color_id[]=3'
ts = int(time.time())

USER_BRANDS = ['zara']


def check_user(brands, prices, sizes):
    number_of_right_element = 0
    for brand in USER_BRANDS:
        #print(sizes)
        num_of_elements = brands.count(brand)
        if num_of_elements >= 2:
            for clothe, size in  zip(brands, sizes):
                if clothe == brand and size == 'M':
                    number_of_right_element += 1
    return number_of_right_element


def get_links(URL):
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


def get_arr(URL):
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


if __name__ == '__main__':
    prices = []
    brands = []
    sizes = []
    links = get_links(BASE_URL)
    num_page = 1
    while len(links) != 0:

        URL = BASE_URL + '&time=' + str(ts) + '&page=' + str(num_page)

        print(num_page)
        links = get_links(URL)

        for i, link in enumerate(links):
            brands, prices, sizes = get_arr(link)

            if check_user(brands, prices, sizes) != 0:
                print(link)
        num_page += 1