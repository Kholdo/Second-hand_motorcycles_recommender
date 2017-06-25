__author__ = 'kholdo'

import pandas as pd
from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from recommender_class_test import Recommender

data = pd.read_csv('../df_motos_raw_coord_brand_type.csv', sep=',', encoding='utf-8')
brands_list = sorted(data['brand'].unique())
types_list = sorted(data['type'].unique())
years_list = sorted(data['year'].unique())
cities_list = sorted(data['city'].unique())

app = Flask(__name__)
Bootstrap(app)

@app.route("/", methods=['GET', 'POST'])
def message():
	title= "Motorcycle Recommender"
	subtitle = "The best and simplest one in the whole world wide web"
	query_city = request.form.get("cities")
	query_brand = request.form.get("brands")
	query_type = request.form.get("types")
	query_year = request.form.get("years")
	
	if query_city != None and query_brand != None and query_type != None and query_year != None:
		r = Recommender(query_city, query_brand, query_type, query_year, 20)
		res = r.recommender().values.tolist()
	else:
		res = []

	return render_template("main.html", res = res, title = title, subtitle=subtitle, 
							brands_list = brands_list, types_list=types_list, 
							years_list = years_list, cities_list=cities_list,
							query_city=query_city, query_brand=query_brand, 
							query_type=query_type, query_year=query_year)

if __name__ == '__main__':
	app.run(port=5000, debug=True)