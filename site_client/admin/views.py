from flask import jsonify, Blueprint, url_for, render_template
from site_client.libs.core import Conference, Engagement, Speaker, Nomination


admin = Blueprint('admin', __name__,
    template_folder='../templates/admin',
    url_prefix='/admin')


@admin.route('/')
def home():
    conf = Conference(year='2015', theme='Finding X').get_or_create()
    return render_template('dashboard.html')


@admin.route('/speakers')
def speakers():
    return render_template('header.html')


@admin.route('/team')
def team():
    return render_template('header.html')


@admin.route('/conference')
def conference():
    return render_template('header.html')
