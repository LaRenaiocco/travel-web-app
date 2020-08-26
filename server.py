""" Server for Operation Adventure."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud
import helper
import os
import json
from datetime import date, time

app = Flask(__name__)
app.secret_key = os.environ['FLASK_KEY']
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
            return redirect (f'users/profile/{user.fname}')


@app.route ('/logout')
def logout_user():
    """Log out user."""

    session.clear()
    return redirect('/')


@app.route('/users/create-user.json', methods = ['POST'])
def new_user():
    """Create new profile."""

    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    user = helper.get_user_by_email(email)
    if user != None:
        return jsonify('This email is already associated with an account. Please log in.')
    else:
        crud.create_user(email, password, fname, lname)
        return jsonify('Your account has been created.  Please log in.')


@app.route('/users/profile/<fname>')
def show_user_profile(fname):
    """ Show logged in user profile."""

    user = helper.get_user_by_email(session['USERNAME'])
    user_itins = helper.get_itineraries_by_user(user)
    return render_template('user_profile.html', user=user, user_itins=user_itins)  


@app.route('/users/trips/new-trip.json', methods=['POST'])
def new_itinerary():
    """Creates a new itinerary for a user and returns data as JSON."""

    user = helper.get_user_by_email(session["USERNAME"])
    trip_name = request.form['trip_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    num_days = crud.calculate_itinerary_days(start_date, end_date)
    lat, lng = crud.get_latitude_longitude_for_itinerary(trip_name)
    new_itinerary = crud.create_itinerary(trip_name, start_date, end_date, num_days, lat, lng)
    crud.create_user_itinerary(user.user_id, new_itinerary.itinerary_id)
    return jsonify({'itinerary_id': new_itinerary.itinerary_id, 'trip_name': new_itinerary.trip_name})


@app.route('/users/trips/add-trip.json', methods=['POST'])
def link_itinerary():
    """Links a user to an existing itienrary and returns data as JSON"""

    user = helper.get_user_by_email(session["USERNAME"])
    itinerary_id = request.form['id']
    itinerary = helper.get_itinerary_by_id(itinerary_id)
    crud.create_user_itinerary(user.user_id, itinerary_id)
    return jsonify({'itinerary_id': itinerary_id, 'trip_name': itinerary.trip_name})


@app.route('/users/trips/<itinerary_id>')
def show_itinerary(itinerary_id):
    """Show individual trip itinerary."""

    session['TRIP'] = itinerary_id
    return render_template('my_trip.html')


@app.route('/users/trips/api')
def return_json_for_maps():
    """Return json to JS for my_trip google map."""

    json_data = helper.json_itinerary_activities(session['TRIP'])
    return json.dumps(json_data, cls=helper.DateTimeEncoder)


@app.route('/users/itinerary/api')
def return_json_for_itinerary():
    """Return json to JS for my_trip page."""

    json_data = helper.jsonify_all_itinerary_data(session['TRIP'])
    return json.dumps(json_data, cls=helper.DateTimeEncoder)


@app.route('/users/trips/new-note.json', methods=['POST'])
def return_new_note():
    """Saves new note to DB and returns to page in JSON."""

    itinerary_id = session['TRIP']
    email = session["USERNAME"]
    user_id = helper.get_user_id(email)
    author = helper.get_user_fname(email)
    comment = request.form['comment']
    date = request.form['date']
    if date == '':
        date = None
    crud.create_note(itinerary_id, user_id, comment, date)
    json_data = {'author': author, 'comment': comment, 'day': date}
    return json.dumps(json_data, cls=helper.DateTimeEncoder)
    

@app.route('/users/trips/activities')
def activity_search():
    """return itinerary information for activity search page."""

    trip_name = helper.get_itinerary_name(session['TRIP'])
    return render_template('activity_search.html', trip_name=trip_name)

@app.route('/users/trips/activities.json')
def return_map_render_json():
    """returns itinerary information for activity search map."""

    json_data = helper.serialize_itinerary_by_id(session['TRIP'])
    return json.dumps(json_data, cls=helper.DateTimeEncoder)


@app.route('/users/trips/new-activity/api', methods=['POST'])
def add_new_activity():
    """adds new activity to database."""

    itinerary_id = session['TRIP']
    activity_name = request.form['name']
    address = request.form['address']
    lat_lng = request.form['latlng']
    lat_lng = lat_lng.strip('()')
    lat_lng_list = lat_lng.split(', ')
    lat = float(lat_lng_list[0])
    lng = float(lat_lng_list[1])
    # lat, lng = float(lat_lng_list) - error.  reassess later
    activity_day = request.form['day']
    if activity_day == '':
        activity_day = None
    activity_time = request.form['time']
    if activity_time == '':
        activity_time = None
    activity_note = request.form['note']
    if activity_note == '':
        activity_note = None
    crud.create_activity(itinerary_id, activity_name, address, 
                        lat, lng, activity_day, activity_time, 
                        activity_note)
    return jsonify('This activity has been added to your trip')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)