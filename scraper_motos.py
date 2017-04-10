#Scraper motos.net

#libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import unicodedata

#BeautifulSoup object
motor_url = 'http://motos.coches.net/ocasion/?pg=2&Tops=1&or=-1&fi=SortDate'
motos_req = requests.get(motor_url)
motos_soup = BeautifulSoup(motos_req.text, "html.parser")

ads_number_text = motos_soup.find_all("h1", {"class": "floatleft"})
num_ads = int(re.findall(r'[^ ]*\.[^ ]*', ads_number_text[0].contents[0])[0].replace('.',''))

#There are usually thirty ads per page
ads_per_page = 30
first_page = 1
last_page = num_ads / ads_per_page

print last_page
