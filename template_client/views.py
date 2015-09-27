from client.public.views import public
from flask import jsonify
from .libs.sample import Sample


@public.route('/create')
def create():
	"""Creates a new Sample object and displays all objects"""
	Sample(option='c').post()
	Sample(option='d').post()
	sample = Sample(option='c').fetch()
	return jsonify(dict(results=sample))