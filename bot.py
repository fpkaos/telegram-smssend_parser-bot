from sys import argv
from bs4 import BeautifulSoup as bs
import requests
import telebot
from random import randint

class Soup:
    def __init__(self, url, param_name):
        self.url = url
        self.param_name = param_name
        self.page_count = self.calculate_pages()
    
    @staticmethod
    def make_soup(url, params):
        req = requests.get(url, params=params,
                          headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh;' \
            'Intel Mac OS X 10.9; rv:45.0) ' \
            'Gecko/20100101 Firefox/45.0'
        })
        return bs(req.text, 'html.parser')
    
    def calculate_pages(self):
        soup = Soup.make_soup(self.url, {self.param_name: 1})
        links = soup.find_all('a')
        end_n = int(links[6]['href'].split('=')[-1])
        return end_n
    
    def random_page(self) -> list:
        divs = Soup.make_soup(
            self.url,
            {self.param_name: randint(1, self.page_count)}
        ).find_all('div', class_='center-col__content-send_mess')
        #[(to, text),...]
        return [(d.contents[1].text, d.contents[3].text) for d in divs]
    
    def random_quote(self):
        rnd_page = self.random_page()
        return rnd_page[randint(0, len(rnd_page))]

soup = Soup(
    url='https://smsend.ru/sent-sms.php',
    param_name='PAGEN_1',
)

bot = telebot.TeleBot(argv[1])

@bot.message_handler(commands=["quote"])
def quote(msg):
    quote = soup.random_quote()
    bot.send_message(
        msg.chat.id,
        f'*{quote[0]}*\n{quote[1]}',
        parse_mode='markdown',
    )

bot.polling(none_stop=True)
