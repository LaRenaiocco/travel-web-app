# You asked the question - does the table relationship make sense, 
# is it performant, etc.? For the data model you described to me 
# originally, this table structure makes sense.
"""Data Models for travel web app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///travel', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """ A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    email = db.Column(db.String, unique=True)
    # Have y'all talked about password security? For the MVP
    # this is clearly not a big deal, but take a look at
    # https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
    # This is one of many techniques you'll use in a production app
    # to secure user passwords.
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    photo_path = db.Column(db.String, nullable=True)

    user_itinerary = db.relationship('UserItinerary')
    note = db.relationship('Note')

    def __repr__(self):
        return f'< User Object user_id: {self.user_id} email: {self.email} >'


class Itinerary(db.Model):
    # Small nit: this docstring doesn't tell me much since it just 
    # duplicates the title of the class. Could you tell the reader 
    # more about what itineraries actually represent in your app?
    """ An Itinerary."""

    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    trip_name = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    # I remember we talked about this briefly, but did you
    # try calculating this automatically (end_date - start_date)?
    num_days = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    user_itinerary = db.relationship('UserItinerary')
    activity = db.relationship('Activity')
    note = db.relationship('Note')

    def __repr__(self):
        return f'< Itinerary Object itinerary_id: {self.itinerary_id} trip_name: {self.trip_name} >'


class UserItinerary(db.Model):
    """ Association table for User and Itinerary."""

    __tablename__ = "user_itineraries"

    ui_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.user_id'))
    itinerary_id = db.Column(db.Integer,
                    db.ForeignKey('itineraries.itinerary_id'))

    user = db.relationship('User')
    itinerary = db.relationship('Itinerary')

    def __repr__(self):
        return f'User Itinerary Association: user_id: {self.user_id} itinerary_id: {self.itinerary_id} >'

class Activity(db.Model):
    """ An Activity."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    itinerary_id = db.Column(db.Integer,
                    db.ForeignKey('itineraries.itinerary_id'))
    activity_name = db.Column(db.String)
    address = db.Column(db.String)
    # place_id = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    activity_day = db.Column(db.Date, nullable=True)
    activity_time = db.Column(db.Time, nullable=True)
    activity_note = db.Column(db.Text, nullable=True)


    # Do you need to define the relationship here, as well as in the Itinerary
    # class? There you've already added `activity = db.relationship('Activity')`,
    # and you declare the foreign key relationship here (itinerary_id). 
    # The docs seem to indicate this duplicate relationship is unnecessary
    # (https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-many)
    # but I'm not a SQLAlchemy expert. There are a few other places in your model
    # where you duplicate the relationship (e.g in the Note class).
    itinerary = db.relationship('Itinerary')

    def __repr__(self):
        return f'< Activity Object activity_id: {self.activity_id} activity_name: {self.activity_name} >'


class Note(db.Model):
    """ A note."""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    itinerary_id = db.Column(db.Integer,
                    db.ForeignKey('itineraries.itinerary_id'))
    user_id = db.Column(db.Integer, 
                    db.ForeignKey('users.user_id'))
    comment = db.Column(db.Text)
    day = db.Column(db.Date, nullable=True)

    itinerary = db.relationship('Itinerary')
    author = db.relationship('User')

    def __repr__(self):
        return f'< Note Object note_id: {self.note_id} user_id: {self.user_id} >'
    
if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)