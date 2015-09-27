from flask import jsonify, Blueprint
from .libs.sample import Sample


public = Blueprint('public', __name__)

@public.route('/create')
def create():
    """Creates a new Sample object and displays all objects"""
    Sample(option='c').post()
    Sample(option='d').post()
    sample = Sample(option='c').fetch()
    return jsonify(dict(results=sample))
