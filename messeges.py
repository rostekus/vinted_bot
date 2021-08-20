from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# stworzyć zestaw, zaproponować niższa cena % procent
# wysłąc ustaloną wiadomość



class Messeges:
	def __init__(self, PATH ='/vinted_bot/geckodriver'):
		self.driver = webdriver.Firefox(PATH)
		self.login()


	def login(self):
		print("please login in into vinted")
		login_page_url = 'https://www.vinted.pl/member/general/login'
		self.driver.get(login_page_url)


	def send_messege(self,message,link):
		self.driver.get(link)
		self.driver.find_element_by_id('composerInput').clear()
		driver.find_element_by_id('composerInput').send_keys(message)



if __name__ == '__main__':
	mes_bot = Messeges()
	sleep(60)
	print('over')
	mes_bot.send_messege('hellp','https://www.vinted.pl/inbox/393984578')
