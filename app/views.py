from flask import render_template
from app import app

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
