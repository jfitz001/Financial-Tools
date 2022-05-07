from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def scrape_multicoin():
    # location of multicoin portfolio
    url = 'https://multicoin.capital/portfolio/'

    # gets html from url
    html = urllib.request.urlopen(url)

    # initialize beautiful soup
    x = BeautifulSoup(html, 'html.parser')

    # returns the coins and initialize list to store them
    tickers = []
    for para in x.find_all("p", class_="short-description"):
        tickers.append(para.get_text().split()[0])

    return tickers


def scrape_icodrops():
    # url for ico coins, looking for high interest rated coins
    url = 'https://icodrops.com/category/upcoming-ico/'

    # using selenium since webpage is javascript oriented
    ## Jamie's PC
    # driver = webdriver.Chrome(r'C:\Users\jamie\Downloads\chromedriver.exe')
    ## Mikes PC
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    # looking for coin names
    x = driver.find_elements_by_tag_name('h3')
    y = driver.find_elements_by_class_name('interest')
    z = driver.find_elements_by_class_name('date')

    # initialize beautiful soup
    a_list = []
    b_list = []
    c_list = []
    for i in x:
        if i.text != '':
            a_list.append(i.text)
    for i in y:
        if i.text != '':
            b_list.append(i.text)
    for i in z:
        if i.text != '':
            c_list.append(i.text)

    # Create list to store coin dictionaries
    dict_list = []
    if len(a_list) == len(b_list) and len(b_list) == len(c_list):
        # for loop to join a,b, and c list data
        for i in range(len(a_list)):
            hash = {'name': a_list[i],
                    'rating': b_list[i],
                    'release': c_list[i]
                    }
            dict_list.append(hash)

    # for i in dict_list:
    #     for k, v in i.items():
    #         print(f'{k}: {v}')
    #     print('\n')

    return dict_list


def scrape_topicolist():
    # scraping the top picks from this website
    url = 'https://topicolist.com/'
    # gets html from url
    html = urllib.request.urlopen(url)

    # initialize beautiful soup
    x = BeautifulSoup(html, 'html.parser')
    # returns the coins and initialize list to store them
    tickers = []
    for i in (x.find_all('h4', class_='heading-34')):
        tickers.append(i.text)

    return tickers
