from client.forms import Form, wtf

class AddSpeakerForm(Form):
    statuses = ['pending review', 'under review', 'accepted', 'declined']
    name = wtf.StringField()
    tagline = wtf.StringField()
    description = wtf.StringField()
    status = wtf.SelectField(default="pending review", choices=[(s, s) for s in statuses])


class EditSpeakerForm(AddSpeakerForm):
    pass


class AddStaffForm(Form):
    name = wtf.StringField()
    tagline = wtf.StringField()
    description = wtf.StringField()
    avatar = wtf.StringField() # path to image


class EditStaffForm(AddStaffForm):
    pass
