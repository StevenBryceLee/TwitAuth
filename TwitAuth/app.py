"""Main app routing file for twitauth"""

from flask import Flask, render_template
from .models import DB, User, insert_example_users

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
        insert_example_users()

        # users = User.query.all()
        #Rendering template that we created passing home to template
        return render_template('base.html', title='Home', users=User.query.all())
    
    return app