"""Main app routing file for twitauth"""

from flask import Flask, render_template, request
from .models import DB, User, Tweet, insert_fake_users
from .twitter import insert_example_user, add_or_update_user
from .predict import predict_user

def create_app():
    #Initializes app
    app = Flask(__name__)

    # Saves data
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)
    
    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        insert_example_user()
        # insert_fake_users()
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/compare', methods = ['POST'])
    def compare():
        user0 , user1 = sorted([request.values['user0'], request.values['user1']])
        if user0 == user1:
            message = 'cannot compare a user to themself'
        else:
            print(user0, user1, request.values['tweet_text'])
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = f"{request.values['tweet_text']} is more likely to be said by {user1 if prediction else user0} than {user0 if prediction else user1}"
        return render_template('prediction.html', title = 'Prediction', message=message)


    @app.route('/update')
    def update():
        # insert_fake_users()
        insert_example_user()
        return render_template('base.html', title='Updated users', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Database reset', users=User.query.all())

    @app.route('/user', methods = ['POST'])
    @app.route('/user/<name>', methods = ['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error add{}: {}".format(name, e)
            tweets = []

        return render_template('user2.html', title=name, 
                                    tweets = tweets, message = message)
    return app