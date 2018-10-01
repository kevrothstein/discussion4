from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True
API_KEY = "c2b338957f53a9500e8833e757ba6048"


class WeatherForm(FlaskForm):
	zipcode = IntegerField('whats your zipcode?', validators =[Required()]) 
	submit = SubmitField('Submit')

	def validate_zipcode(self, field):
		if len(str(field.data)) != 5:
			raise ValidationError('please eneter a 5 digit zipcode')

@app.route('/zipcode', methods = ['GET', 'POST'])
def zipcode_view():
	form = WeatherForm()
	if form.validate_on_submit():
		zipcode = str(form.zipcode.data)
		params = {}
		params['zip'] = zipcode + ',us'
		params['appid'] = 'c2b338957f53a9500e8833e757ba6048'
		baseurl = 'http://api.openweathermap.org/data/2.5/weather?'
		response = requests.get(baseurl, params = params)
		response_dict = json.loads(response.text)
		print(response_dict)

		description = response_dict['weather'][0]['description']
		city = response_dict['name']
		temperature_kelvin = response_dict['main']['temp']
		return render_template('results.html', city = city, description = description, temperature = temperature)

	flash(form.errors)
	return render_template('zipform.html', form = form)

if __name__ == '__main__':
	app.run()


