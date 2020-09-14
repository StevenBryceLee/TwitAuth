'''SQLAlchemy models and utility functions for TwitAuth'''

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

class User(DB.Model):
    '''Represents a twitter user'''
    # def __init__(self):
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f'-User {self.name}'

class Tweet(DB.Model):
    '''represents a tweet'''
    # def __init__(self):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'-Tweet {self.text}'

def insert_example_users():
    users = [User(id=1, name = 'nick'),
    User(id=2, name = 'steven'),
    User(id=3, name='joe'),
    User(id=4, name='bob'),
    User(id=5, name='bill')]
    tweets = [Tweet(id=1, text='hello'), Tweet(id=2, text=' world')] 
    # Adds to database
    for user in users:
        DB.session.add(user)
    for tweet in tweets:
        DB.session.add(tweet)
    DB.session.commit()
    