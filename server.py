""" Server for Operation Adventure."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud
import helper
import os

app = Flask(__name__)
app.secret_key = "devLaRena"
app.jinja_env.undefined = StrictUndefined
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/login', methods = ['POST'])
def login_user():
    """ Log in user."""

    email = request.form['email']
    password = request.form['password']
    user = helper.get_user_by_email(email)

    if user == None:
        flash('No account with this email exists. Please try again.')
        return redirect ('/')
    else:
        if password != user.password:
            flash('Incorrect Password. Please try again.')
            return redirect ('/')
        else:
            session['USERNAME'] = user.email
            # print(session['USERNAME'])
            print('session username set')
            return redirect (f'users/profile/{user.fname}')


@app.route ('/logout')
def logut_user():
    """Log out user."""

    session.pop('USERNAME', None)
    session.pop('TRIP', None)

    return redirect('/')


@app.route('/users/profile/<fname>')
def show_user_profile(fname):
    """ Show logged in user profile."""

    email = session['USERNAME']
    user = helper.get_user_by_email(email)
    user_itins = helper.get_itineraries_by_user(user)

    return render_template('user_profile.html', user=user, user_itins=user_itins)  


@app.route('/users/create-user')
def create_new_user():
    """Render new profile form."""

    return render_template('create_profile.html')


@app.route('/users/create-user', methods = ['POST'])
def new_user():
    """Create new profile."""

    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']

    user = helper.get_user_by_email(email)

    if user != None:
        flash('This email is already associated with an account. Please log in.')
        return redirect ('/')
    else:
        crud.create_user(email, password, fname, lname)
        flash('Your account has been created.  Please log in.')
        return redirect ('/')


@app.route('/users/trips/new-trip.json', methods=['POST'])
def new_itinerary():
    """Creates a new itinerary for a user."""

    email = session["USERNAME"]
    user = helper.get_user_by_email(email)
    trip_name = request.form.get('trip_name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    num_days = crud.calculate_itinerary_days(start_date, end_date)
    new_itinerary = crud.create_itinerary(trip_name, start_date, end_date, num_days)
    new_ui = crud.create_user_itinerary(user.user_id, new_itinerary.itinerary_id)
    json_info = {'itinerary_id': new_itinerary.itinerary_id, 'trip_name': new_itinerary.trip_name}

    return jsonify(json_info)





@app.route('/users/trips/<itinerary_id>')
def show_itinerary(itinerary_id):
    """Show individual trip itinerary."""

    return render_template('my_trip.html')

@app.route('/map')
def show_map():

    return render_template('my_trip.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)