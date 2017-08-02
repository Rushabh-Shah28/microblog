from flask import flash, redirect, render_template, g, url_for, session, request
from app import app
from .forms import LoginForm, EditForm
from .models import User
from app import oid, db, lm
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

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
        name = resp.name
        if name is None or name == "":
            name = resp.email.split('@')[0]
        user = User(name = name, email = resp.email)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user,remember_me)
    return redirect(url_for('index') or request.args.get('next'))

@app.before_request
def before_request():
    g.user = current_user
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<name>')
def user(name):
    u = User.query.filter_by(name=name).first()
    if not u:
        return redirect(url_for('index'))

    posts = [
        {'author': u, 'description': 'Test post #1'},
        {'author': u, 'description': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=u,
                           posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)






