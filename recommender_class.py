class Recommender:

	def __init__(self, user_city, user_brand, user_type, user_year):
		import pandas as pd
		self.data = pd.read_csv('df_motos_raw_coord_brand_type.csv', sep=',', encoding='utf-8')		
		self.location_coords = pd.read_csv('auxiliary_data/locations_coords.csv', sep=',')
		self.brands_rank = pd.read_csv('scraped_data/rank_moto_brands.csv', sep=';')
		self.types_rank = pd.read_csv('auxiliary_data/rank_moto_types.csv.csv', sep=';')

		self.city = user_city
		self.brand = user_brand
		self.type = user_type
		self.year = user_year
		self.lat = self.user_location_coords()[0]
		self.lon = self.user_location_coords()[1]

		self.brand_score = int(self.brands_rank[self.brands_rank['brand'] == self.brand].brand_score)
		self.type_score = int(self.types_rank[self.types_rank['type'] == self.type].type_score)

		self.weight_brand = 0
		self.weight_type = 0
		self.weight_year = 0
		self.weight_city = 0
		self.total_weight = self.weight_brand + self.weight_type + self.weight_year + self.weight_city

	def user_location_coords(self):
		"""
		This function calculates the coordinates of the city entered by the user
		"""
		import geopy
		from geopy.geocoders import Nominatim
		geolocator = Nominatim()
		location = geolocator.geocode(self.city, timeout = 15)

		return (location.latitude, location.longitude)

	def cities_distance(self, city_lat, city_lon):
	    """    
	    :param city_lat: the value in the dataset's lat column to the corresponding city
	    :param city_lon: the value in the dataset's lon column to the corresponding city
	    :param user_lat: The corresponding lat value in the location dataset of the city selected by the user
	    :param user_lon: The corresponding lon value in the location dataset of the city selected by the user
	    
	    :return: The value in kilometers of the distance between the two cities.
	    
	    Usage of the Vicenty distance
	    """
	    
	    from geopy.distance import vincenty
	    
	    column_city = (city_lat, city_lon)
	    user_city = (self.user_lat, self.user_lon)
	    
	    return (vincenty(column_city, user_city).km)

	def distance_abs_value(self, a_value, b_value):
		return abs(a_value - b_value)

	def w_s(self, city_row, brand_row, type_row, year_row):
		import numpy as np
		params = np.array([city_row, brand_row, type_row, year_row])
		weights = np.array([self.weight_city, self.weight_brand, self.weight_type, self.weight_year])

		num = sum(params * weights) * 1.0
		return num/self.total_weight

		