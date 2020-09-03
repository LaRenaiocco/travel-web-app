"""Helper functions to assist in server flow."""

from model import (db, User, Itinerary, UserItinerary, Activity, Note, connect_to_db)
import json
import os
from datetime import date, time, timedelta
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE = os.environ['TWILIO_PHONE']


""" Database query functions"""

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_user_fname(email):
    """Return user's first name from email."""

    user = get_user_by_email(email)
    return user.fname


def get_user_id(email):
    """Return user id from email"""

    user = get_user_by_email(email)
    return user.user_id


def get_itineraries_by_user(user):
    """Look up itineraries associated with a specified user."""

    itins = db.session.query(UserItinerary.itinerary_id, Itinerary.trip_name).join(Itinerary).filter(UserItinerary.user_id == user.user_id).all()
    itins_list = []
    for itin in itins:
        itin_dict = {'itinerary_id': itin[0], 'trip_name': itin[1]}
        itins_list.append(itin_dict)

    return itins_list


def get_itinerary_by_id(itinerary_id):
    """Look up itinerary by id."""

    return Itinerary.query.get(itinerary_id)

def get_itinerary_name(itinerary_id):
    """Look up trip name by id."""

    itinerary = get_itinerary_by_id(itinerary_id)
    return itinerary.trip_name


def get_notes_by_itinerary_id(itin_id):
    """Look up notes associated with an itinerary."""

    return Note.query.filter_by(itinerary_id = itin_id).all()


def get_activities_by_itinerary_id(itin_id):
    """Look up Activities associated with an itinerary."""

    return Activity.query.filter_by(itinerary_id = itin_id).all()


""" Compile data in JSON ready format"""

def serialize_itinerary_by_id(itin_id):
    """serialize itinerary to jsonify"""

    itinerary = get_itinerary_by_id(itin_id)
    return {'itinerary_id': itinerary.itinerary_id,
                      'trip_name': itinerary.trip_name,
                      'start_date': itinerary.start_date,
                      'end_date': itinerary.end_date,
                      'num_days': itinerary.num_days,
                      'lat': itinerary.lat,
                      'lng': itinerary.lng
                      }

def list_activities_by_itinerary(itin_id):
    """serialize activities list to jsonify"""

    activities = get_activities_by_itinerary_id(itin_id)
    json_activities = []
    for a in activities:
        a_dict = {'activity_id': a.activity_id, 
            'itinerary_id': a.itinerary_id,
            'activity_name': a.activity_name, 
            'address': a.address, 
            'lat': a.lat,
            'lng': a.lng, 
            'activity_day': a.activity_day, 
            'activity_time': a.activity_time, 
            'activity_note': a.activity_note
            }
        json_activities.append(a_dict)
    return json_activities


def list_notes_by_itinerary(itin_id):
    """serialize notes list to jsonify"""

    notes_author = db.session.query(User.fname, Note.comment, Note.day).join(User)
    itin_notes = notes_author.filter(Note.itinerary_id == itin_id).all()
    json_notes = []
    for note in itin_notes: 
        n_dict = {} 
        n_dict['author'] = note[0] 
        n_dict['comment'] = note[1] 
        n_dict['day'] = note[2] 
        json_notes.append(n_dict)
    return json_notes

def json_itinerary_activities(itin_id):
    """ return itinerary and associated activities."""

    itinerary = serialize_itinerary_by_id(itin_id)
    activities = list_activities_by_itinerary(itin_id)
    return {'itinerary': itinerary, 'activities': activities}


def jsonify_all_itinerary_data(itin_id):
    """Return all data for an individual itinerary in jsonable format."""

    itinerary = serialize_itinerary_by_id(itin_id)
    activities = list_activities_by_itinerary(itin_id)
    start_date = itinerary['start_date']
    end_date = itinerary['end_date']
    dates = create_dates_list(start_date, end_date)
    notes = list_notes_by_itinerary(itin_id)
    return {'itinerary': itinerary, 
                 'activities': activities,
                 'dates': dates,
                 'notes': notes
                 }


""" Functions to work with date data""" 

def create_dates_list(start_date, end_date):
    """ Return list of days in range of start and end date for itinerary."""

    delta = end_date - start_date
    dates = []
    for d in range(delta.days + 1):
        dates.append(start_date + timedelta(days = d))
    return dates
 

class DateTimeEncoder(json.JSONEncoder):
    """Makes time and date objects jsonifiable."""

    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


""" Twilio notification functions"""

def add_phone_to_user(email, phone):
    """Add phone number to user object in database"""
    if phone == 'None':
        phone = None
    else:
        phone = '+1' + phone
    user = get_user_by_email(email)
    user.phone = phone
    db.session.commit()

    return user


def users_to_notify(itinerary_id, email):
    """ Gets users associated with an itinerary to notify of changes
    excluding user who made the change."""

    users = db.session.query(UserItinerary.user_id, User.phone, User.email).join(User).filter(UserItinerary.itinerary_id == itinerary_id).all()
    phone_list = []
    #user[1] = user phone, user[2]=user email
    for user in users:
        if user[1] != None and user[2] != email:
            phone_list.append(user[1])

    return phone_list


# def registration_text_update():


def send_itinerary_text_update(itinerary_id, email, trip_name, author):
    """Sends text updates to users via Twilio"""

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    phone_list = users_to_notify(itinerary_id, email)
    if phone_list != []:
        for phone_num in phone_list:
            message = client.messages.create(
                to=phone_num,
                from_=TWILIO_PHONE,
                body=f'Your trip to {trip_name} has been updated by {author}'
            )
        print(message.sid)







    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)