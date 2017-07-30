from flask_wtf import Form
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField(label='openid', validators=[DataRequired()], description='used for user verification')
    remember_me = BooleanField(label='remeber me', default=False)