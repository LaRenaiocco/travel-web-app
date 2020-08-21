from model import (db, User, Itinerary, UserItinerary, Activity, Note, connect_to_db)
import geocoder


def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_itineraries_by_user(user):
    """Look up itineraries associated with a specified user."""

    user_id = user.user_id
    user_itin_ids = UserItinerary.query.filter(UserItinerary.user_id == user_id).all()
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


def get_notes_by_itinerary_id(itin_id):
    """Look up notes associated with an itinerary."""

    return Note.query.filter_by(itinerary_id = itin_id).all()


def get_activities_by_itinerary_id(itin_id):
    """Look up Activities associated with an itinerary."""

    return Activity.query.filter_by(itinerary_id = itin_id).all()

def serialize_itinerary_by_id(itin_id):
    """serialize itinerary to jsonify"""

    itinerary = get_itinerary_by_id(itin_id)
    jsonifiable_itinerary = {'itinerary_id': itinerary.itinerary_id,
                      'trip_name': itinerary.trip_name,
                      'start_date': itinerary.start_date,
                      'end_date': itinerary.end_date,
                      'num_days': itinerary.num_days,
                      'lat': itinerary.lat,
                      'lng': itinerary.lng
                      }
    return jsonifiable_itinerary

def list_activities_by_itinerary(itin_id):
    """serialize activities to jsonify"""

    activities = get_activities_by_itinerary_id(itin_id)
    jsonifiable_activities = []
    for a in activities:
        a_dict = {'activity_id': a.activity_id, 'itinerary_id': a.itinerary_id, 'activity_name': a.activity_name, 'address': a.address, 'lat': a.lat, 'lng': a.lng, 'activity_day': a.activity_day, 'activity_time': a.activity_time, 'activity_note': a.activity_note}
        jsonifiable_activities.append(a_dict)

    return jsonifiable_activities

def json_itinerary_and_activities(itin_id):

    itinerary = serialize_itinerary_by_id(itin_id)
    activities = list_activities_by_itinerary(itin_id)

    json = {'itinerary': itinerary, 'activities': activities}


    
