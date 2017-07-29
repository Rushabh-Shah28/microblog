from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
    user = {'name': 'Rushabh'}
    posts = [
        {
            'author': "J.K Rowling",
            'description': 'Beautiful day in Portland!'
        },
        {
            'author': 'Barack Obama',
            'description': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)
