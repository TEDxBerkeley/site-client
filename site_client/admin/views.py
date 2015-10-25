from flask import jsonify, Blueprint, url_for, render_template, request,\
    redirect
from site_client.libs.core import Conference, Engagement, Speaker, Nomination, \
    Staff, Membership
from .forms import AddSpeakerForm, EditSpeakerForm, AddStaffForm, EditStaffForm\
    , AddConferenceForm, EditConferenceForm

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

############
# SPEAKERS #
############

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

########
# TEAM #
########

@admin.route('/staff')
def staff():
    conf = get_conference()
    if conf:
        staff = conf.fetch_staff()
    return render_template('staff.html', **locals())


@admin.route('/staff/add', methods=['POST', 'GET'])
def staff_add():
    conf = get_conference()
    form = AddStaffForm(request.form)
    if request.method == 'POST':
        Staff(conference=conf.id, **request.form).post()
        return redirect(url_for('admin.staff'))
    return render_template('form.html', **locals())


@admin.route('/staff/<string:staffId>/edit', methods=['POST', 'GET'])
def staff_edit(staffId):
    conf = get_conference()
    staff = Staff(id=staffId).get()
    form = EditStaffForm(request.form, staff)
    if request.method == 'POST':
        staff.load(created_at=None, updated_at=None, **request.form).put()
        return redirect(url_for('admin.staff_info', staffId=staffId))
    return render_template('form.html', **locals())


@admin.route('/staff/<string:staffId>/delete', methods=['POST', 'GET'])
def staff_delete(staffId):
    conf = get_conference()
    if request.method == 'POST':
        Staff(id=staffId).delete()
        return redirect(url_for('admin.staff'))
    return render_template('delete.html', back=url_for('admin.staff'))


@admin.route('/staff/<string:staffId>', methods=['POST', 'GET'])
def staff_info(staffId):
    staff = Staff(id=staffId).get()
    return jsonify(staff._data)

##############
# CONFERENCE #
##############

@admin.route('/conference')
def conference():
    conf = get_conference()
    if conf:
        conferences = Conference().fetch()
    return render_template('conference.html', **locals())


@admin.route('/conference/add', methods=['POST', 'GET'])
def conference_add():
    form = AddConferenceForm(request.form)
    if request.method == 'POST':
        Conference(**request.form).post()
        return redirect(url_for('admin.conference'))
    return render_template('form.html', **locals())


@admin.route('/conference/<string:conferenceId>/edit', methods=['POST', 'GET'])
def conference_edit(conferenceId):
    conference = Conference(id=conferenceId).get()
    form = EditConferenceForm(request.form, conference)
    if request.method == 'POST':
        conference.load(created_at=None, updated_at=None, **request.form).put()
        return redirect(url_for('admin.conference_info', conferenceId=conferenceId))
    return render_template('form.html', **locals())


@admin.route('/conference/<string:conferenceId>', methods=['POST', 'GET'])
def conference_info(conferenceId):
    conference = Conference(id=conferenceId).get()
    return jsonify(conference._data)

###############
# NOMINATIONS #
###############

@admin.route('/nominations')
def nominations():
    conf = get_conference()
    if conf:
        nominations = Nomination(conference=conf.id).fetch()
    return render_template('nominations.html', **locals())
