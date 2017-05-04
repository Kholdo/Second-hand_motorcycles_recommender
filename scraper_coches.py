#!/usr/bin/python
# -*- coding: utf-8 -*-

#Scraper coches.net

def Scraper_coches():
	from datetime import datetime
	import pandas as pd
	from bs4 import BeautifulSoup		
	import requests
	import re
	from tools import remove_accents as ra
	#BeautifulSoup object
	coches_url = 'http://www.coches.net/segunda-mano/?pg=2'
	coches_req = requests.get(coches_url)
	coches_soup = BeautifulSoup(coches_req.text, "html.parser")
	pages_number_text = coches_soup.find_all("h1", {"class": "mt-SerpHeader-title u-ellipsis"})
	num_pages = int(re.findall(r'[.0-9]*\)', pages_number_text[0].contents[0])[0].replace('.','')[:-1])

	#Lets go to scrape the urls
	matrioska_tb = []
	matrioska_header = ['brand', 'model', 'province', 'price', 'year', 'km', 'doors',
							'seats', 'hp', 'gear', 'fuel', 'poll']

	print 'Start time: %ss' % datetime.now()
	print 'num_pages %d' %num_pages

	for i in range(1, num_pages):
		if i % 10 == 0:
			print "page %d" %i
		sub_url = 'http://www.coches.net/segunda-mano/?pg=%d' %i
		sub_req = requests.get(sub_url, allow_redirects = False)
		if sub_req.status_code == 200:
			sub_soup = BeautifulSoup(sub_req.text, "html.parser")
			links_list = sub_soup.find_all("a", {"class": "mt-CardAd-link"}, href = True)
			for link in links_list:
				link_req = requests.get("http://www.coches.net" + link['href'])
				#print "http://www.coches.net" + link['href']
				link_soup = BeautifulSoup(link_req.text, "html.parser")
				# price
				if len(link_soup.find_all("span", {"class": "t-h1 mt-AdDetailHeader-price u-c--red"})) != 0:
					car_price_text = link_soup.find_all("span", {"class": "t-h1 mt-AdDetailHeader-price u-c--red"})[0].contents[0]
					car_price = int(re.findall(r'[0-9]*\.[0-9]*|.*[0-9]', car_price_text)[0].replace('.', ''))
					# Brand
					try:
						car_brand = link_soup.find_all("a", {"data-tagging": "c_detail_bread_ad_brand"})[0].contents[0]
					except:
						car_brand = ''
					# Model
					try:
						car_model = link_soup.find_all("a", {"data-tagging": "c_detail_bread_ad_model"})[0].contents[0]
					except:
						car_model = ''
					# Province
					try:
						car_province = link_soup.find_all("a", {"data-tagging": "c_detail_bread_ad_province"})[0].contents[0]
					except:
						car_province = ''


					#Rest of features
					features_list = link_soup.find_all("li", {"class": "mt-DataGrid-item"})
					#car_year
					car_year = int(features_list[0].get_text().strip())

					car_km, car_doors, car_seats, car_hp, car_gear, car_fuel, car_poll = ['']*7
					for index, item in enumerate(features_list):
						#km
						if len(re.findall(r'[ ]km', item.get_text())) > 0:
							try:
								car_km = int(re.findall(r'[0-9]*\.[0-9]*|.*[0-9]', item.get_text().strip())[0].replace('.', ''))
							except:
								car_km = ''
						# Doors
						if len(re.findall(r'[ ]Puertas', item.get_text())) > 0:
							try:
								car_doors = int(re.findall(r'[0-9]', item.get_text().strip())[0].replace('.', ''))
							except:
								car_doors = ''
						# Seats
						if len(re.findall(r'[ ]Plazas', item.get_text())) > 0:
							try:
								car_seats = int(re.findall(r'[0-9]', item.get_text().strip())[0].replace('.', ''))
							except:
								car_seats = ''
						# hp
						if len(re.findall(r'[ ]cv', item.get_text())) > 0:
							try:
								car_hp = int(re.findall(r'[0-9]*', item.get_text().strip())[0].replace('.', ''))
							except:
								car_hp = ''
						# gear
						if len(re.findall(r'[ ]Cambio', item.get_text())) > 0:
							try:
								car_gear = unicode(re.findall(r'.*\s([^ ]*)', item.get_text().strip())[0])
							except:
								car_gear = ''
						# fuel
						if len(re.findall(r'Diesel|Gasolina', item.get_text())) > 0:
							try:
								car_fuel = unicode(re.findall(r'Diesel|Gasolina', item.get_text().strip())[0])
							except:
								car_fuel = ''
						# poll
						if len(re.findall(r'[ ]gr/km', item.get_text())) > 0:
							try:
								car_poll = re.findall(r'[0-9]*', item.get_text().strip())[0]
							except:
								car_poll = ''

					matrioska_tb.append([ra(car_brand), ra(car_model), 
										ra(car_province), car_price, 
										car_year, car_km, 
										car_doors, car_seats,
										car_hp, ra(car_gear),
										ra(car_fuel), car_poll
										])

	print 'End time: %s' % datetime.now()
	matrioska_df = pd.DataFrame(matrioska_tb, columns = matrioska_header)
	return matrioska_df