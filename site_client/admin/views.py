from flask import jsonify, Blueprint, url_for, render_template, request,\
    redirect
from site_client.libs.core import Conference, Engagement, Speaker, Nomination
from .forms import AddSpeakerForm, EditSpeakerForm

admin = Blueprint('admin', __name__,
    template_folder='../templates/admin',
    url_prefix='/admin')


def get_conference():
    """Retrieves current conference"""
    return Conference(year='2015', theme='Finding X').get_or_create()


@admin.route('/')
def home():
    conf = get_conference()
    return render_template('dashboard.html')


@admin.route('/speakers')
def speakers():
    conf = get_conference()
    if conf:
        speakers = conf.fetch_speakers()
    return render_template('speakers.html', **locals())


@admin.route('/speakers/add', methods=['GET', 'POST'])
def speaker_add():
    conf = get_conference()
    form = AddSpeakerForm(request.form)
    if request.method == 'POST':
        Speaker(conference=conf.id, **request.form).post()
        return redirect(url_for('admin.speakers'))
    return render_template('form.html', **locals())


@admin.route('/speakers/<string:speakerId>/edit', methods=['POST', 'GET'])
def speaker_edit(speakerId):
    conf = get_conference()
    speaker = Speaker(id=speakerId).get()
    form = EditSpeakerForm(request.form, speaker)
    if request.method == 'POST':
        speaker.load(created_at=None, updated_at=None, **request.form).put()
        return redirect(url_for('admin.speaker_info', speakerId=speakerId))
    return render_template('form.html', **locals())


@admin.route('/speakers/<string:speakerId>/delete', methods=['POST', 'GET'])
def speaker_delete(speakerId):
    conf = get_conference()
    if request.method == 'POST':
        Speaker(id=speakerId).delete()
        return redirect(url_for('admin.speakers'))
    return render_template('delete.html', back=url_for('admin.speakers'))


@admin.route('/speakers/<string:speakerId>', methods=['POST', 'GET'])
def speaker_info(speakerId):
    speaker = Speaker(id=speakerId).get()
    return jsonify(speaker._data)


@admin.route('/team')
def team():
    conf = get_conference()
    if conf:
        speakers = conf.fetch_staff()
    return render_template('header.html', **locals())


@admin.route('/conference')
def conference():
    conf = get_conference()
    return render_template('header.html', **locals())
