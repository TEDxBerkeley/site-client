from flask import jsonify, Blueprint, url_for, render_template
from .libs.core import Conference, Engagement, Speaker, Nomination


admin = Blueprint('admin', __name__, template_folder='templates/admin')
