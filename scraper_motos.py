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

print num_ads
