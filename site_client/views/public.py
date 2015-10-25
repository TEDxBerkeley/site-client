from flask import jsonify, Blueprint, url_for, render_template, request
from site_client.libs.core import Conference, Engagement, Speaker, Nomination


public = Blueprint('public', __name__, template_folder='../templates/public')

@public.route('/')
def index():
    conf = Conference(year='2015', theme='Finding X').get_or_create()
    return render_template('index.html')


@public.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')

@public.route('/speakers')
@public.route('/<int:year>/speakers')
def speakers(year=None):
    """List of speakers for a conference"""
    conf = Conference(year=year).get()
    if conf:
        speakers = conf.fetch_speakers()
        return jsonify(dict(results=speakers))
    return 'Conference speaker announcements coming soon.'


@public.route('/<int:year>/team')
@public.route('/team')
def team(year=None):
    """List of team members for a conference"""
    conf = Conference(year=year).get()
    if conf:
        staff = conf.fetch_staff()
        return jsonify(dict(results=staff))
    return 'Conference staff announcement coming soon.'

@public.route('/nominate', methods=['GET', 'POST'])
def nominate(year=None):
    if request.method == 'GET':
        return render_template('nomination_form.html')
    else:
        return "Thanks for submitting a nomination!"

@public.route('/<int:year>/')
@public.route('/conference')
def conference(year=None):
    """Conference main page"""
    conf = Conference(year=year).get()
    if conf:
        return jsonify(conf._data)
    return 'Conference information coming soon.'
