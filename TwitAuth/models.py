'''SQLAlchemy models and utility functions for TwitAuth'''

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import numpy as np


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

DB = SQLAlchemy()

class User(DB.Model):
    '''Represents a twitter user'''
    # def __init__(self):
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'-User {self.name}'

class Tweet(DB.Model):
    '''represents a tweet'''
    # def __init__(self):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    embedding = DB.Column(DB.PickleType, nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    

    def __repr__(self):
        return f'-Tweet {self.text}'

def insert_fake_users():
    names = ['Oliver', 'Charlotte', 'Liam', 'Ava', 'Ethan', 'Amelia', 'Aiden',
            'Olivia', 'Gabriel', 'Aurora', 'Caleb', 'Violet',
            'Theodore', 'Luna', 'Declan', 'Hazel', 'Owen', 'Chloe', 'Elijah', 'Arya']
    users = [User(id=np.random.randint(1000), name = np.random.choice(names), newest_tweet_id=np.random.randint(20)),
    User(id=np.random.randint(1000), name = np.random.choice(names), newest_tweet_id=np.random.randint(20)),
    User(id=np.random.randint(1000), name=np.random.choice(names), newest_tweet_id=np.random.randint(20)),
    User(id=np.random.randint(1000), name=np.random.choice(names), newest_tweet_id=np.random.randint(20)),
    User(id=np.random.randint(1000), name=np.random.choice(names), newest_tweet_id=np.random.randint(20))]

    tweets = [Tweet(id=np.random.randint(1000), text=''.join(['hello ', np.random.choice(names)]), user_id=1, embedding=np.arange(5)), 
                Tweet(id=np.random.randint(1000), text=' world', user_id=2, embedding=np.arange(5))] 
    # Adds to database
    for user in users:
        DB.session.add(user)
    for tweet in tweets:
        DB.session.add(tweet)
    DB.session.commit()
    