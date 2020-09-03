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
    """ Users of the web app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    phone = db.Column(db.String, nullable=True)
    photo_path = db.Column(db.String, nullable=True)


    def __repr__(self):
        return f'< User Object user_id: {self.user_id} email: {self.email} >'


class Itinerary(db.Model):
    """ Itineraries - Data related to a specific trip created by a user."""

    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    trip_name = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    num_days = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


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

    user = db.relationship('User', backref='user_itinerary')
    itinerary = db.relationship('Itinerary', backref='user_itinerary')


    def __repr__(self):
        return f'User Itinerary Association: user_id: {self.user_id} itinerary_id: {self.itinerary_id} >'

class Activity(db.Model):
    """ Activities added to itineraries by users."""

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

    itinerary = db.relationship('Itinerary', backref='activity')


    def __repr__(self):
        return f'< Activity Object activity_id: {self.activity_id} activity_name: {self.activity_name} >'


class Note(db.Model):
    """ Notes added to itineraries by users."""

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

    itinerary = db.relationship('Itinerary', backref='note')
    author = db.relationship('User', backref='note')


    def __repr__(self):
        return f'< Note Object note_id: {self.note_id} user_id: {self.user_id} >'


def example_data():
    """Data for tests"""

    User.query.delete()
    Itinerary.query.delete()
    UserItinerary.query.delete()
    Activity.query.delete()
    Note.query.delete()

    user1 = User(email='Alex@alex.com', password='test', fname='Alex', 
                lname='Arbour', phone='7073182084')
    user2 = User(email='Bobby@bobby.com', password='test', fname='Bobby',
                lname='Bobbington', phone=None)
    london = Itinerary(trip_name='London, UK', start_date='2021-01-01',
                end_date='2021-01-08', num_days=8, lat=51.528308, lng=-0.3817846)
    ui = UserItinerary(user_id=1, itinerary_id=1)
    lyceum = Activity(itinerary_id=1, activity_name='Lyceum Theatre', 
                address='21 Wellington St, Covent Garden, London WC2E 7RQ, United Kingdom', 
                lat=51.511619, lng=-0.1223251, activity_day='2021-01-02', activity_time='20:00')
    museum = Activity(itinerary_id=1, activity_name='National Portrait Gallery', 
                address="St. Martin's Pl, Charing Cross, London WC2H 0HE, United Kingdom", 
                lat=51.5094269, lng=-0.1303103)
    note1 = Note(itinerary_id=1, user_id=1, comment='Lets make sure we go to high tea!',
                day=None)
    note2 = Note(itinerary_id=1, user_id=2, comment='Lets have a picnic in Hyde Park', 
                day='2021-01-05')

    db.session.add_all([user1, user2, london, ui, lyceum, museum, note1, note2])
    db.session.commit()



    
if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)