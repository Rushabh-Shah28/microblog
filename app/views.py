from flask import flash, redirect, render_template, g, url_for, session, request
from app import app
from .forms import LoginForm
from .models import User
from app import oid, db, lm
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
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
@oid.loginhandler
def login():

    if g.user.is_authenticated and g.user:
        redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = str(form.remember_me.data)
        oid.try_login(form.openid.data, ask_for=['nickname' , 'email'])

        flash('ID required="%s", remember me= %s' % (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('login.html',
                           title='Login',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        redirect(url_for('login'))

    user = User.query.filter(User.email == resp.email)
    if user is None:
        user = User(name = resp.name, email = resp.email)
        db.session.add(user)
        db.session.commit()

    if 'remember_me' in session['remember_me']:
        remember_me = session['remember_me']
    else:
        remember_me = False

    login_user(user,remember_me)
    return redirect(url_for('index') or request.args.get('next'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




