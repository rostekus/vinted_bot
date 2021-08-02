from configparser import ConfigParser
import bot
import gmail
import argparse
from pathlib import Path
# TODO:
# save all possible brands from vinted site
# check regex for adress
# add ML 

class App:

    def __init__(self):
        self.url, self.brands, self.size, self.price, self.num_of_clothes= self.setup()
        #self.vinbot = bot.VintedBot(self.url, self.brands, self.size, self.price , self.num_of_clothes)
        #while(True):
            #self.vinbot.start()
        
    
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


    

    def check_url(self):
        pass

    def send_email(self):
        pass




if __name__ == '__main__':
    app = App()

        
