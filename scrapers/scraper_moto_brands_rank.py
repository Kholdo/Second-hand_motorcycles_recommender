#!/usr/bin/python
# -*- coding: utf-8 -*-

#Scraper motorcycles rank

def scraper_moto_brands_rank():
	from datetime import datetime
	import pandas as pd
	from bs4 import BeautifulSoup
	import requests
	import re
	#BeautifulSoup object
	motorank_url_1 = "http://en.classora.com/reports/f87259/ranking-of-the-best-motorcycle-brands?id=872&groupCount=50&startIndex=1"
	motorank_url_2 = "http://en.classora.com/reports/f87259/ranking-of-the-best-motorcycle-brands?id=872&groupCount=50&startIndex=51"
	urls = [motorank_url_1, motorank_url_2]
	complete_brand_list = []
	for url in urls:
	    motorank_req = requests.get(url)
	    motos_soup = BeautifulSoup(motorank_req.text, "html.parser")

	    entrycells = motos_soup.find_all("td", {"class": "rankingEntryCell"})

	    datacells = motos_soup.find_all("td", {"class": "rankingDataCell"})

	    brand_list = [[entrycells[index].get_text().lower(), datacells[index].get_text()] for index, val in enumerate(entrycells)]
	    
	    complete_brand_list += brand_list
	    
	complete_brand_df = pd.DataFrame(complete_brand_list, columns = ['brand', 'brand_score'])
	complete_brand_df.to_csv('../scraped_data/rank_moto_brands.csv', sep = ';', index = False)
	#return complete_brand_df