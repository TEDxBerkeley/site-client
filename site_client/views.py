from flask import jsonify, Blueprint, url_for
from .libs.sample import Sample


public = Blueprint('public', __name__)

@public.route('/')
def index():
    return '<a href="%s">test logic connection</a>' % url_for('public.test')

@public.route('/test')
def test():
    """Creates a new Sample object and displays all objects"""
    Sample(option='c').post()
    Sample(option='d').post()
    sample = Sample(option='c').fetch()
    return jsonify(dict(results=sample))
