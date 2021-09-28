from configparser import ConfigParser
import bot
import mail
import argparse
from pathlib import Path
import json
from string import ascii_uppercase
import sqlite3
from requests import get
from bs4 import BeautifulSoup
import re
import sys


class App:
    def __init__(self):
        self.url, self.brands, self.size, self.price, self.num_of_clothes = self.setup()

        self.vinbot = bot.VintedBot(
            self.url, self.brands, self.size, self.price, self.num_of_clothes
        )
        self.mail = 0
        self.password = 0
        while True:
            self.setup()
            self.vinbot.start()


    def setup(self):

        setup_file = Path("config.ini")
        if setup_file.is_file():

            parser = ConfigParser()
            

            args = self.get_arguments(required= False)
            
            if any(vars(args).values()):
                config = ConfigParser()
                config.read("config.ini")

                if  args.url:
                    config.set('settings', 'url',args.url)

                if  args.brands:
                    brands = self.string_2_list(args.brands)

                    config.set('settings', 'brands',str(brands))

                if  args.price:
                    config.set('settings', 'price', str(args.price))
                
                if  args.size:
                    config.set('settings', 'size',args.size)

                if  args.number:
                    config.set('settings', 'number',str(args.number))


                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

            parser = ConfigParser()  
            parser.read("config.ini")
            brands = self.string_2_list(parser.get("settings", "brands"))
            
            try:
                self.mail = parser.get("settings", "mail")
                self.password = parser.get("settings", "password")
            except NoOptionError as e:
                print('Mail and password were not given')



            return (
                parser.get("settings", "url"),
                brands,
                parser.get("settings", "size"),
                int(parser.get("settings", "price")),
                int(parser.get("settings", "number")),
            )
        else:
            print('Please run setup.py first')
            sys.exit()

    def get_arguments(self, required=True):

        parser = argparse.ArgumentParser(
            description="Bot for searching clothes on vinted.com"
        )
        parser.add_argument(
            "--url", required=required, type=str, nargs="?", help="Url for searching"
        )
        parser.add_argument(
            "-b",
            "--brands",
            type=str,
            nargs="?",
            help="Brands (separated by a comma)",
            required=required,
        )
        parser.add_argument(
            "-s",
            "--size",
            type=str,
            nargs="?",
            help="Clothes size",
            required=required,
        )
        parser.add_argument(
            "-p",
            "--price",
            type=int,
            nargs="?",
            help="Maximum price",
            required=required,
        )
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            nargs="?",
            help="Number of clothes per user",
            required=required,
        )
        return parser.parse_args()



    def string_2_list(self, text):
        return list(text.lower().replace(" ", "").split(","))

    # send csv file to email
    def send_email(self):
        mail.send_email(self.mail, self.password)


    def urls_generator(self):
        pattern = """<a class="follow__name" data-ch="br" href="\/brand\/(.+?)">
                  (.+?)
                 <\/a>
                 <div class="follow__details">
                  (.+?) p"""

        alphabet = ascii_uppercase
        base_url = "https://www.vinted.pl/brands/by_letter/"
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
            bs = BeautifulSoup(page.content, "html.parser")
            bs = bs.prettify()
            data = {}
            data.update(
                {
                    letter: {
                        text.group(2): text.group(3)
                        for text in re.finditer(pattern, bs)
                    }
                }
            )
            print(data)
            with open("data.json", "rw") as fp:
                json.dump(data, fp)

    # scrap info from https://www.vinted.pl/brands/by_letter/ into sqlite3 datebase sqlite3
    def statistics_db(self):
        conn = sqlite3.connect("brands_statistics.db")
        curr = conn.cursor()

        curr.execute(
            """
        CREATE TABLE IF NOT EXISTS statistics (letter TEXT, brand TEXT, num INTEGER)"""
        )

        pattern = """<a class="follow__name" data-ch="br" href="\/brand\/(.+?)">
                  (.+?)
                 <\/a>
                 <div class="follow__details">
                  (.+?) p"""

        alphabet = ascii_uppercase
        base_url = "https://www.vinted.pl/brands/by_letter/"
        for letter in alphabet:
            url = base_url + letter
            print(url)
            page = get(url)
            bs = BeautifulSoup(page.content, "html.parser")
            bs = bs.prettify()
            for match in re.finditer(pattern, bs):
                curr.execute(
                    "INSERT INTO statistics VALUES (?, ?, ?)",
                    (letter, match.group(2), match.group(3)),
                )
                conn.commit()


if __name__ == "__main__":
    app = App()
