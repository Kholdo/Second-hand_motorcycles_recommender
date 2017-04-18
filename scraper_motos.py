#!/usr/bin/python
# -*- coding: utf-8 -*-

#Scraper motos.net

def scraper_motos():
	from datetime import datetime
	import pandas as pd
	from bs4 import BeautifulSoup
	import requests
	import re
	from tools import remove_accents as ra
	#BeautifulSoup object
	motor_url = 'http://motos.coches.net/ocasion/?pg=1&or=-1&fi=SortDate'
	motos_req = requests.get(motor_url)
	motos_soup = BeautifulSoup(motos_req.text, "html.parser")

	ads_number_text = motos_soup.find_all("h1", {"class": "floatleft"})
	num_ads = int(re.findall(r'[^ ]*\.[^ ]*', ads_number_text[0].contents[0])[0].replace('.',''))

	#There are usually thirty ads per page
	ads_per_page = 30
	first_page = 1
	last_page = num_ads / ads_per_page
	#Lets go to scrape the urls
	matrioska_tb = []
	matrioska_header = ['city', 'brand', 'model', 'type', 'cc', 'color', 'km', 'year', 'price']

	print 'Start time: %s' % datetime.now()
	print 'num_ads %d' %num_ads

	for i in range(first_page, last_page):
		sub_url = 'http://motos.coches.net/ocasion/?pg=%d&or=-1&fi=SortDate' %i
		sub_req = requests.get(sub_url, allow_redirects = False)
		if sub_req.status_code == 200:
			sub_soup = BeautifulSoup(sub_req.text, "html.parser")
			links_list = sub_soup.find_all("a", {"class": "lnkad"}, href = True)
			for link in links_list:
				link_req = requests.get("http://motos.net" + link['href'])
				link_soup = BeautifulSoup(link_req.text, "html.parser")			
				#If the ad exists, there is a h1 tag with class 'mgbottom10 floatleft'
				if len(link_soup.find_all("h1", class_= 'mgbottom10 floatleft')) != 0:				
					title = link_soup.find_all("span", itemprop = "title")
					try:
						bike_price = int(''.join(re.findall(r'\b\d+\b', link_soup.find(class_='pvp').contents[0])))
					except:
						bike_price = ''
						print "price error in http://motos.coches.net" + link['href']
					if len(title) == 4 and bike_price != '':						
						#city, brand, model
						bike_city, bike_brand, bike_model = ra(title[1].get_text()), ra(title[2].get_text()),ra(title[3].get_text())

						#type
						try:
							bike_type = link_soup.find(id = 'litTipo').contents[1].strip()
						except:
							bike_type = ''
							print "type error in http://motos.coches.net" + link['href']
						#cc
						try:
							bike_cc = int(''.join(re.findall(r'\b\d+\b', link_soup.find(id='litCC').contents[1].strip())))
						except:
							bike_cc = ''
							print "cc error in http://motos.coches.net" + link['href']
						#color
						try:
							bike_color = re.findall(r'<b>Color:</b>([^<]*)', link_req.text)[0].strip()
							bike_color = '' if bike_color == '-' else bike_color
						except:
							bike_color = ''
							print "color error in http://motos.coches.net" + link['href']
						#km
						try: 
							bike_km = re.findall(r'<b>Km:</b>([^<]*)', link_req.text)[0].strip().replace('.', '')
							bike_km = '' if bike_km == '-' else bike_km
						except:
							bike_km = ''
							print "km error in http://motos.coches.net" + link['href']
						#year
						try:
							bike_year = re.findall(r'Año:</b>([^<]*)', link_req.text.encode('utf8'))[0].strip().replace('.','')
						except:
							bike_year = ''
							print "year error in http://motos.coches.net" + link['href']
						
						matrioska_tb.append([bike_city, bike_brand, bike_model, bike_type, bike_cc, bike_color, bike_km, bike_year, bike_price])

	print 'End time: %s' % datetime.now()
	matrioska_df = pd.DataFrame(matrioska_tb, columns = matrioska_header)
	return matrioska_df