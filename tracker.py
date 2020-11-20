import webbrowser
import requests
import time
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

URL = input(f"\n{bcolors.BOLD}Insert ebay product's url:{bcolors.ENDC} ")
while (not URL) or ('ebay.com' not in URL):
    URL = input("Insert only ebay product's url: ")

USER_AGENT = input(f"\n{bcolors.BOLD}Insert your user agent (Google \"what is my user agent\"):{bcolors.ENDC} ")

MIN_PRICE = input(f"\n{bcolors.BOLD}Insert the minimum price you want to pay($):{bcolors.ENDC} ")
while not MIN_PRICE.isdigit():
    MIN_PRICE = input("insert only float type price: ")


MIN_PRICE = float(MIN_PRICE)    
headers = {"User-Agent": USER_AGENT}
notifier = ToastNotifier()

print(f'\n{bcolors.OKGREEN}*** Tracking Started ***{bcolors.ENDC}')

try:
    while True:
        page = requests.get(URL, headers=headers)
        parsed_page = BeautifulSoup(page.content, 'html.parser')

        # find price on ebay page
        if parsed_page.find(id='prcIsum'):
            price = parsed_page.find(id='prcIsum').get_text()
        else: 
            price = parsed_page.find(id='mm-saleDscPrc').get_text() # in case item on sale

        product_title = parsed_page.find(id='itemTitle').get_text()[16:]
        numeric_price = float(price.split()[1][1:])

        if numeric_price < MIN_PRICE:
            notifier.show_toast(title="Item's Price Has Been Dropped!", msg=product_title, duration=7, threaded=True)
            webbrowser.open(url=URL, new=2)
            break

        time.sleep(3600) # checks for price change every hour
except:
    print(f'\n{bcolors.FAIL}Something went wrong, check your inputs')
    
print(f'\n*** Tracking Stopped ***{bcolors.ENDC}')     