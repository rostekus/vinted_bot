from configparser import ConfigParser
from getpass import getpass
import re
import smtplib

def string_2_list(text):
        return list(text.lower().replace(" ", "").split(","))

def config():

    config = ConfigParser()
    
    setting  = {}

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    loggedin = False
    while not loggedin:
        try:
            mail = input('Gmail for sending csv files (click enter if you are not interested in this):')
            if mail:
                password = getpass('Password for email')
                server.login(mail,password)
            else:
                mail = 0
                password = 0
                break

        except:
            print("Wrong credentials")
    server.quit()


    url = input('URL (https://www.vinted.pl/...): ')
    correct = False
    while correct:
        if not 'https://www.vinted.pl/' in url:
            print('Wrong url')
            url = input('URL (https://www.vinted.pl/...): ')
        else:
            correct = True

    brands = string_2_list(input('Brands (separated by a comma):'))
    size = input('Size:')
    price = int(input('Maximum price: '))
    number  = int(input('Number of clothes per user:'))
    
    


    setting['url'] = url
    setting['brands'] = brands
    setting['size'] = size
    setting['price'] = price
    setting['number'] = number
    setting['mail'] = mail
    setting['password'] = password
    print('==========================')
    for x, y in setting.items():
        if x =='mail' and y == 0:
            print(f'{x} : Not provided')
        elif x =='password' and y == 0:
            print(f'{x} : Not provided')
        else:
            print(f'{x} : {y}')
    print('=========================')




    config['settings'] =setting





    with open('config.ini', 'w') as f:
        config.write(f)






def main():
    config()



if __name__ == '__main__':
    main()