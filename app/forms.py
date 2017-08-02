from flask_wtf import Form
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField(label='openid', validators=[DataRequired()], description='used for user verification')
    remember_me = BooleanField(label='remeber me', default=False)

class EditForm(Form):
    name = StringField('name', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])