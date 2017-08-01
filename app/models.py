from app import db

class User(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))