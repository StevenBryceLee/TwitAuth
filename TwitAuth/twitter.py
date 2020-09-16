
'''Collects tweets, embeddings and save to DB'''

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import tweepy
import basilica
from .models import DB, Tweet, User

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']
                 
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
BASILICA_KEY = os.getenv("BASILICA_KEY")

b = basilica.Connection(BASILICA_KEY)
user = 'jackblack'

# Grants authorization
TWITTER_AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
TWITTER = tweepy.API(TWITTER_AUTH)
DB = SQLAlchemy()
user = 'jackblack'
twitter_user = TWITTER.get_user(user)

tweets = twitter_user.timeline(count = 5, exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode = 'extended',)
tweet_text = tweets[0].full_text
# print(tweet_text)
embedding = b.embed_sentence(tweet_text, model = 'twitter')

# print(embedding[0])
# exit()

def add_or_update_user(username):
    twitter_user = TWITTER.get_user(username)
    db_user = (User.query.get(twitter_user.id) or 
                User(id = twitter_user.id, name = username))
    DB.session.add(db_user)
    tweets = twitter_user.timeline(count = 3, exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode = 'extended',)
    # Get latest tweet ID
    if tweets:
        db_user.newest_tweet_id = tweets[0].id

    for tweet in tweets:
        embedding = b.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id = tweet.id, text=tweet.full_text[:300], embedding=embedding)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)

    DB.session.commit()

    for name in TWITTER_USERS:
        try:
            twitter_user = TWITTER.get_user(name)
            db_user = (User.query.get(twitter_user.id))
            # print(twitter_user.id)
            tweets = twitter_user.timeline(count = 3, exclude_replies=True,
                                            include_rts=False, tweet_mode='Extended',
                                            )
            # for tweet in tweets:
                # print(tweet.text)
        except Exception as e:
            print(f'Error: {e},\n{username} not found')
        
        else:
            DB.session.commit()


def insert_example_user():
    for user in TWITTER_USERS[:5]:
        add_or_update_user(user)