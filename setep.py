from configparser import ConfigParser

config = ConfigParser()


config['settings'] ={
    'url' :'https://www.vinted.pl/ubrania?search_text=&brand_id[]=20682&brand_id[]=9&brand_id[]=123&brand_id[]=91&size_id[]=208&status[]=6&status[]=1&status[]=2&price_to=15.0&currency=PLN&search_id=471687498',
    'brands' : 'zara',
    'size' : 'M',
    'price' : 15,
    'number': 2
}

with open('config.ini', 'w') as f:
    config.write(f)