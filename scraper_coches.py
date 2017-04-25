#!/usr/bin/python
# -*- coding: utf-8 -*-

#Scraper coches.net

def scraper_coches():
	from datetime import datetime
	import pandas as pd
	from bs4 import BeautifulSoup
	import requests
	import re
	#BeautifulSoup object
	coches_url = 'http://www.coches.net/segunda-mano/?pg=2'
	coches_req = requests.get(coches_url)
	coches_soup = BeautifulSoup(coches_req.text, "html.parser")
	pages_number_text = coches_soup.find_all("h1", {"class": "mt-SerpHeader-title u-ellipsis"})
	num_pages = int(re.findall(r'[.0-9]*\)', pages_number_text[0].contents[0])[0].replace('.','')[:-1])

	return num_pages