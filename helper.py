from model import (db, User, Itinerary, UserItinerary, Activity, Note, connect_to_db)


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


