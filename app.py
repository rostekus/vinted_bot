import bot
import gmail
from sys import argv


# check regex for adress
class App:

    def __init__(self):
        pass
    
    def setup(self):
        
        is_corrct = self.check_url(url)
        if is_corrct:
            return 

    def check_url(self):
        pass

    def send_email(self):
        pass


BASE_URL = 'https://www.vinted.pl/ubrania?currency=PLN&search_id=471687498&status[]=6&status[]=1&status[]=2&size_id[]=208&order=price_low_to_high&brand_id[]=20682&brand_id[]=9&brand_id[]=123&brand_id[]=91&price_to=15'
if __name__ == '__main__':

    if(argv[1] == 'setup'):
        BASE_URL = argv[2]
    print(BASE_URL)
    else:
        vinbot = bot.VintedBot(BASE_URL, ['house'], 'M', 100, 1)
        vinbot.start()
