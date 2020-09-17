'''Prediction model of user based on tweet embeddings'''

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import b


def predict_user(user0_name, user1_name, tweet_text):
    '''determine and return which user is more likely to say a given tweet

    example run: predict_user('jackblack','elonmusk', 'Tesla woo')
    '''

    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    user_0_embeddings = np.array([tweet.embedding for tweet in user0.tweets])
    user_1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    embeddings = np.vstack([user_0_embeddings, user_1_embeddings])
    labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])
    print(f'0Embeds:\t{user_0_embeddings.shape}')
    print(f'1Embeds:\t{user_1_embeddings.shape}')
    print('Embeddings shape{}\t'.format(embeddings.shape))
    lr = LogisticRegression(solver = 'liblinear', max_iter = 200).fit(embeddings, labels)

    tweet_embedding = b.embed_sentence(tweet_text, model = 'twitter')
    return lr.predict(np.array(tweet_embedding).reshape(1, -1))