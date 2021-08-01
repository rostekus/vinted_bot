import bot
import gmail
from sys import argv


# check regex for adress


BASE_URL = 'https://www.vinted.pl/ubrania?search_text=house&brand_id[]=11&catalog[]=2050&currency=PLN&search_id=471276307'
if __name__ == '__main__':

    if(argv[1] == 'setup'):
        BASE_URL = argv[2]
    print(BASE_URL)

    #vinbot = bot.VintedBot(BASE_URL, ['house'], 'M', 100, 1)
    #vinbot.start()
