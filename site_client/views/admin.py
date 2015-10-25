from flask import jsonify, Blueprint, url_for, render_template
from site_client.libs.core import Conference, Engagement, Speaker, Nomination


admin = Blueprint('admin', __name__, template_folder='templates/admin')


@admin.route('/')
def index():
    conf = Conference(year='2015', theme='Finding X').get_or_create()
    return render_template('dashboard.html')
