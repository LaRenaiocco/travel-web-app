from model import (db, User, Itinerary, UserItinerary, Activity, Note, connect_to_db)
import json
from datetime import date, time, timedelta


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

    user_itin_ids = UserItinerary.query.filter(UserItinerary.user_id 
                                                == user.user_id).all()
    itinerary_ids = []
    for itin in user_itin_ids:
        itinerary_ids.append(itin.itinerary_id)
    itineraries = []
    for ids in itinerary_ids:
        item = Itinerary.query.get(ids)
        itineraries.append(item)
    return itineraries


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


def create_dates_list(start_date, end_date):
    """ Return list of days in range of start and end date for itinerary."""

    delta = end_date - start_date
    dates = []
    for d in range(delta.days + 1):
        dates.append(start_date + timedelta(days = d))
    return dates


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


class DateTimeEncoder(json.JSONEncoder):
    """Makes time and date objects jsonifiable."""

    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)