"""Main app routing file for twitauth"""

from flask import Flask, render_template
from .models import DB, User, Tweet, insert_fake_users
from .twitter import insert_example_user
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
        # insert_example_user()
        insert_fake_users()
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/update')
    def update():
        insert_fake_users()
        return render_template('base.html', title='Updated users', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Database reset', users=User.query.all())

    @app.route('/user/<username>')
    def show_user_data(username):
        DB.drop_all()
        DB.create_all()
        user_id = User.query.filter_by(name=username).all()
        print("User ID", user_id)
        print("type: ",type(user_id))
        return render_template('user.html', title='User', users=User.query.filter_by(name=username).all(), 
                                    tweets=Tweet.query.filter_by(user_id=user_id).all())
    return app