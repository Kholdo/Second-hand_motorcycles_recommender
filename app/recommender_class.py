class Recommender:

	def __init__(self, user_city, user_brand, user_type, user_year, k):
		"""
		:param user_city: the city selected by the user in his request
		:param user_brand: the motorcycle brand selected by the user in his request
		:param user_type: The motorcycle type selected by the user in his request
		:param user_year: The year selected by the user in his request
		:param k: The number of results you want to appear in the request
		"""

		import pandas as pd
		self.k = k
		self.data = pd.read_csv('app/static/data/df_motos_raw_coord_brand_type.csv', sep=',', encoding='utf-8')
		self.brands_rank = pd.read_csv('auxiliary_data/rank_moto_brands_plus.csv', sep=';')
		self.types_rank = pd.read_csv('auxiliary_data/rank_moto_types.csv', sep=';')

		self.city = user_city
		self.brand = user_brand
		self.type = user_type
		self.year = int(user_year)
		self.lat = self.user_location_coords()[0]
		self.lon = self.user_location_coords()[1]

		if self.brands_rank[self.brands_rank['brand'] == self.brand].brand_score.empty:
			self.brand_score = 0
		else:
			self.brand_score = int(self.brands_rank[self.brands_rank['brand'] == self.brand].brand_score)
		self.type_score = int(self.types_rank[self.types_rank['type'] == self.type].type_score)
		self.scores = [self.brand_score, self.type_score, self.year]

		#Weights of the characteristics that the user can choose
		self.weight_brand = 40
		self.weight_type = 40
		self.weight_year = 10
		self.weight_city = 10
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
	    
	    Usage of the Vincenty distance
	    """
	    
	    from geopy.distance import vincenty
	    
	    column_city = (city_lat, city_lon)
	    user_city = (self.lat, self.lon)
	    
	    return (vincenty(column_city, user_city).km)

	def distance_abs_value(self, a_value, b_value):
		return abs(a_value - b_value)

	def weighted_sum(self, city_row, brand_row, type_row, year_row):
		"""
		:param city_row: value of correcponding register in the the city_metric field
		:param brand_row: value of correcponding register in the the brand_metric field
		:param type_row: value of correcponding register in the the type_metric field
		:param year_row: value of correcponding register in the the year_metric field

		:return: the weighted sum of the input parameters

		"""
		import numpy as np
		params = np.array([city_row, brand_row, type_row, year_row])
		weights = np.array([self.weight_city, self.weight_brand, self.weight_type, self.weight_year])

		num = sum(params * weights) * 1.0
		return num/self.total_weight

	def recommender(self):
		"""
		This is our recommender function!!

		:return: the k registers closest to the user's selection

		"""

		score_columns = ['brand_score', 'type_score', 'year']

		self.data['city_metric'] = self.data.apply(lambda row: self.cities_distance(row['lat'], row['lon']), axis=1)

		for i, element in enumerate(['brand', 'type', 'year']):
			new_column = element + '_metric'
			print new_column
			try:
				self.data[new_column] = self.data.apply(lambda row: self.distance_abs_value(int(row[score_columns[i]]), self.scores[i]), axis=1)
			except TypeError:
				print new_column

		self.data['total_metric_pond'] = self.data.apply(lambda row: self.weighted_sum(row['city_metric'], row['brand_metric'], row['type_metric'], row['year_metric']), axis = 1)

		result_columns = ['city', 'brand', 'model', 'type', 'color', 'km', 'year', 'price', 'url', 'total_metric_pond']

		
		res = self.data[result_columns].sort_values(by = ['total_metric_pond'], ascending=True).head(self.k)

		return res
