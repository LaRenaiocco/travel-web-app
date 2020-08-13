""" CRUD operations for travel web app."""

from model import (db, User, Itinerary, UserItinerary, Activity, Note, connect_to_db)

def create_user(email, password, fname, lname, photo_path=None):
    """Create and return a new user."""

    user = User(email=email, 
        password=password, 
        fname=fname, 
        lname=lname,
        photo_path=photo_path)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(user.email == email).first()


def create_itinerary(trip_name, start_date, end_date, num_days):
    """Create and return a new itinerary."""

    itinerary = Itinerary(trip_name=trip_name,
        start_date=start_date,
        end_date=end_date,
        num_days=num_days)

    db.session.add(itinerary)
    db.session.commit()

    return itinerary

def create_user_itinerary(user_id, itinerary_id):
    """ Create an association between a user and an itinerary."""

    user_itinerary = UserItinerary(user_id=user_id, itinerary_id=itinerary_id)

    db.session.add(user_itinerary)
    db.session.commit()

    return user_itinerary


def create_activity(itinerary_id, activity_name, street_address, city, postcode,  activity_day=None, activity_time=None, activity_note=None):
    """Create and return a new activity."""

    activity = Activity(itinerary_id=itinerary_id,
        activity_name=activity_name,
        street_address=street_address,
        city=city,
        postcode=postcode,
        activity_day=activity_day,
        activity_time=activity_time,
        activity_note=activity_note,)

    db.session.add(activity)
    db.session.commit()

    return activity

def create_note(itinerary_id, user_id, comment, day=None):
    """Create and return a new note."""

    note = Note(itinerary_id=itinerary_id,
        user_id=user_id,
        comment=comment,
        day=day)

    db.session.add(note)
    db.session.commit()

    return note 


if __name__ == '__main__':
    from server import app
    connect_to_db(app)