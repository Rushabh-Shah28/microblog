from flask import flash, redirect, render_template
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Rushabh'}
    posts = [
        {
            'author': 'J.K Rowling',
            'description': 'We do not need magic to transform our world. We carry all of the power we need '
                           'inside ourselves already.'
        },
        {
            'author': 'Barack Obama',
            'description': "The future rewards those who press on. I don't have time to feel sorry for myself. "
                           "I don't have time to complain. I'm going to press on"
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('ID required="%s", remember me= %s' % (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('login.html',
                           title='Login',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
