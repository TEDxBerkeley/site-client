from client.forms import Form, wtf


class LoginForm(Form):
    username = wtf.StringField('Username')
    password = wtf.StringField('Password')


class RegisterForm(Form):
    name = wtf.StringField('Full Name')
    username = wtf.StringField('Username')
    email = wtf.StringField('Email')
    password = wtf.StringField('Password')
    code = wtf.StringField('Invite Code')


class NominationForm(Form):
    nominator_name = wtf.StringField('Your Name')
    nominator_email = wtf.StringField('Your Email')
    nominee_name = wtf.StringField('Nominee Name')
    nominee_email = wtf.StringField('Nominee Email')
    speaker_pitch = wtf.TextAreaField('Why would this nominee be a good fit for TEDxBerkeley?')
