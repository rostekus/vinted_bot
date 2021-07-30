from bs4 import BeautifulSoup
from requests import get

URL = 'https://www.vinted.pl/mezczyzni/ubrania/plaszcze-i-kurtki/kurtki/kurtki-puchowe/147380719-brazowa-kurtka-zimowa-meska-zara'

page = get(URL)

bs = BeautifulSoup(page.content, 'html.parser')

bs = bs.find('div', class_ = 'row items-list')
for offer in bs.find_all('a', class_ = 'item-box__brand'):
    print
    offer = str(offer)
    for i in range(41,51):
        if offer[i] == '"':
            break
    print(offer[40:i])

    #for i in range(1,5):
