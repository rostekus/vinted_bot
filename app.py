from configparser import ConfigParser
import bot
import gmail
import argparse
from pathlib import Path
import json
from string import ascii_uppercase
import sqlite3
from requests import get
from bs4 import BeautifulSoup
import re


# TODO:
# save all possible brands from vinted site
# check regex for adress
# add ML ?
#seaborn

class App:

    def __init__(self):
        # self.url, self.brands, self.size, self.price, self.num_of_clothes= self.setup()
        #self.vinbot = bot.VintedBot(self.url, self.brands, self.size, self.price , self.num_of_clothes)
        #while(True):
            #self.vinbot.start()
        pass
    
    def setup(self):
        setup_file = Path('config.ini')
        
        if not setup_file.is_file():

            parser = argparse.ArgumentParser(description='Bot for searching clothes on vinted.com')
            parser.add_argument('--url',required=True, type=str, nargs='?',
                        help='Url for searching')
            parser.add_argument('-b','--brands', type=str, nargs='?',
                        help='An optional integer positional argument')
            parser.add_argument('-s','--size', type=str, nargs='?',
                        help='An optional integer positional argument')
            parser.add_argument('-p','--price', type=int, nargs='?',
                        help='An optional integer positional argument')
            parser.add_argument('-n','--number', type=int, nargs='?',
                        help='An optional integer positional argument')
            args = parser.parse_args()
            #check if are correctly written
            brands = self.string_2_list(args.brands)
            
            print(args.url, brands , args.size, args.price, args.number)
            return args.url, brands , args.size, args.price, args.number 
        else:
            parser = ConfigParser()
            parser.read('config.ini')
            print(parser.get('set', 'url'))
            #check if are correctly written
            brands = self.string_2_list(parser.get('set', 'brands'))
            return parser.get('set', 'url'),brands,parser.get('set', 'size'),1,1

    def string_2_list(self,text):
        return list(text.lower().replace(' ','').split(','))


    # check if url is corrected
    def check_url(self):
        pass

    def send_email(self):
        pass


    def urls_generator(self):
        pattern = """<a class="follow__name" data-ch="br" href="\/brand\/(.+?)">
                  (.+?)
                 <\/a>
                 <div class="follow__details">
                  (.+?) p"""

        alphabet = ascii_uppercase
        base_url = 'https://www.vinted.pl/brands/by_letter/'
        for letter in alphabet:
            url = base_url + letter 
            yield url
    
    
    def all_brands_2_json(self):
        pattern = """<a class="follow__name" data-ch="br" href="\/brand\/(.+?)">
                  (.+?)
                 <\/a>
                 <div class="follow__details">
                  (.+?) p"""
        
        for url in self.urls_generator():
            page = get(url)
            bs = BeautifulSoup(page.content, 'html.parser')
            bs = bs.prettify()
            data  = {}
            data.update({letter :{text.group(2):text.group(3)for text in re.finditer(pattern, bs)}})
            print(data)
            with open('data.json', 'rw') as fp:
                json.dump(data, fp)
    
    
    def statistics_db(self):
        # check if file exists
        conn = sqlite3.connect('brands_statistics.db')
        curr = conn.cursor()
        
        curr.execute("""
        CREATE TABLE IF NOT EXISTS statistics (letter TEXT, brand TEXT, num INTEGER)""")
       
        pattern = """<a class="follow__name" data-ch="br" href="\/brand\/(.+?)">
                  (.+?)
                 <\/a>
                 <div class="follow__details">
                  (.+?) p"""
        
        
        alphabet = ascii_uppercase
        base_url = 'https://www.vinted.pl/brands/by_letter/'
        for letter in alphabet:
            url = base_url + letter 
            print(url)
            page = get(url)
            bs = BeautifulSoup(page.content, 'html.parser')
            bs = bs.prettify()
            for match in re.finditer(pattern, bs):
                curr.execute('INSERT INTO statistics VALUES (?, ?, ?)', (letter, match.group(2), match.group(3)))
                conn.commit()


if __name__ == '__main__':
    app = App()

        
