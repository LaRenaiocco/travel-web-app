""" Server for Operation Adventure."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "devLaRena"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/users/<user_id>')
def show_user_profile(user_id):
    """Show user their profile."""

    return render_template('user_profile.html')


@app.route('/create-user')
def create_new_user():
    """Create new user profile."""

    return render_template('new_user.html')


@app.route('/users/itineraries/<itinerary_id>')
def show_itinerary():
    """Show individual trip itinerary."""

    return render_template('itinerary.html')

