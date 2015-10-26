from datetime import datetime
from random import random
from flask import jsonify, Blueprint, url_for, render_template, request
from site_client.libs.core import Conference, Engagement, Speaker, Nomination
from client.exceptions import LogicException
from flask_login import login_user, redirect as flask_redirect, current_user, \
    logout_user
from client.libs.core import User, Session
from .forms import LoginForm, RegisterForm, NominationForm
from client import hashing, login_manager
import functools


public = Blueprint('public', __name__, template_folder='../templates/public')

###################
# LOGIN UTILITIES #
###################

def redirect(location, **kwargs):
    """assembles kwargs as querystring"""
    kwargs = ['%s=%s' % pair for pair in kwargs.items()]
    location = location + '?' + '&'.join(kwargs)
    return flask_redirect(location)

def anonymous_required(f):
    """Require anonymous - otherwise, redirect to private sphere"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(
                request.args.get('next') or url_for('admin.home'), access_token=current_user.access_token)
        return f(*args, **kwargs)
    return wrapper

@login_manager.user_loader
def load_user(access_token):
    """Loading a user from saved userId"""
    session = Session(access_token=access_token).get()
    if session:
        user = User(id=session.user, access_token=access_token).get()
        session.user = user
        if user.is_active():
            return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Where unauthenticated users are sent"""
    return redirect(url_for('public.login'))


@public.route('/logout')
def logout():
    """Logout the user"""
    logout_user()
    return redirect(url_for('public.login'))

#########
# VIEWS #
#########

@public.route('/')
def home():
    conf = Conference(year='2015', theme='Finding X').get_or_create()
    return render_template('index.html')

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
        return jsonify({
            'results': [stf for stf in staff if stf['status'] == 'accepted']
        })
    return 'Conference staff announcement coming soon.'

@public.route('/nominate', methods=['GET', 'POST'])
def nominate(year=None):
    form = NominationForm(request.form)
    if request.method == 'POST':
        Nomination(**request.form).post()
        return "Thanks for submitting a nomination! <a href=\"%s\">back to tedxberkeley</a>" % url_for('public.home')
    return render_template('form.html', **locals())

@public.route('/<int:year>/')
@public.route('/conference')
def conference(year=None):
    """Conference main page"""
    conf = Conference(year=year).get()
    if conf:
        return jsonify(conf._data)
    return 'Conference information coming soon.'

@public.route('/login', methods=['POST', 'GET'])
@anonymous_required
def login():
    """Login page"""
    try:
        form = LoginForm(request.form)
        next = request.args.get('next', None)
        user = User(username=form.username.data)
        if request.method == 'POST' and form.validate():
            user.get()
            password = hashing.hash_value(form.password.data, salt=user.salt)
            user.authenticate(password=password, salt=None)
            if user.get_id() and user.is_authenticated() and user.is_active():
                if login_user(user):
                    return redirect(
                        request.form.get('next') or url_for('admin.home'), access_token=user.access_token)
            message = 'Login failed.'
    except LogicException as e:
        message = str(e)
    return render_template('login.html', **locals())


@public.route('/register', methods=['POST', 'GET'])
@anonymous_required
def register():
    """Register page"""
    try:
        form = RegisterForm(request.form)
        next = request.args.get('next', None)
        if request.method == 'POST' and form.validate():
            salt = hashing.hash_value(str(datetime.now()))
            password = hashing.hash_value(form.password.data, salt=salt)
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=password,
                salt=salt,
                username=form.username.data
            ).post().authenticate(password=password, salt=None)
            if login_user(user):
                return redirect(
                    request.form.get('next') or url_for('admin.home'),
                    access_token=user.access_token)
            else:
                return redirect(url_for('public.login'))
    except LogicException as e:
        message = str(e)
    return render_template('register.html', **locals())
