#run code in terminal: 
# python3 -m unittest tests.py 


from unittest import TestCase
from flask import session
from model import connect_to_db, db, example_data
from server import app
import helper
import crud



class FlaskTestsBasic(TestCase):
    """Flask tests"""

    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertIn(b"Need an account?", result.data)


class CrudAndHelperTests(TestCase):
    """Tests for crud.py and helper.py"""

    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///apptestdb")
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_create_user(self):
        """Tests creation of user in database."""

        u = crud.create_user('Claire@claire.com', 'test', 'Claire', 'Cramer')
        self.assertIsNotNone(u.user_id)


    def test_create_itinerary(self):
        """Tests creation of an itinerary in database."""

        it = crud.create_itinerary('San Francisco, CA', '2020-12-01', '2020-12-05',
                                    5, 37.7576793, -122.5076413)
        self.assertIsNotNone(it.itinerary_id)


    def test_create_user_itinerary(self):
        """Tests creation of a user and itinerary association in database."""

        ui = crud.create_user_itinerary(2, 1)
        self.assertIsNotNone(ui.ui_id)


    def test_create_activity(self):
        """Tests creation of an activity in the database."""

        a = crud.create_activity(1, 'Highclere Castle', 
            'Highclere Park, Highclere, Newbury RG20 9RN, United Kingdom', 
            51.3265934, -1.3628547, '2021-01-04', '13:00')
        self.assertIsNotNone(a.activity_id)


    def test_create_note(self):
        """Tests creation of a note in the databse"""

        n = crud.create_note(1, 1, 'test note')
        self.assertIsNotNone(n.note_id)


    def test_get_user_by_email(self):
        """Test get_user_by_email function"""

        u = helper.get_user_by_email('Alex@alex.com')
        self.assertIsNotNone(u.user_id)


    def test_get_user_fname(self):
        """Test get_user_fname function"""
        
        self.assertEqual(helper.get_user_fname('Alex@alex.com'), 'Alex')


    def test_get_user_id(self):
        """Test get_user_id function"""

        self.assertEqual(helper.get_user_id('Alex@alex.com'), 1)


    def test_get_itineraries_by_user(self):
        """Test get_itineraries_by_user function"""
        
        user = helper.get_user_by_email('Alex@alex.com')
        test = helper.get_itineraries_by_user(user)
        self.assertIs(type(test), list)


    def test_get_itinerary_by_id(self):
        """Test get_itinerary_by_id function"""

        it = helper.get_itinerary_by_id(1)
        self.assertIsNotNone(it.trip_name)


    def test_get_itinerary_name(self):
        """Test get_itinerary_name function"""

        self.assertEqual(helper.get_itinerary_name(1), 'London, UK')


    def test_get_notes_by_itinerary_id(self):
        """Test get_notes_by_itinerary_id function"""

        test = helper.get_notes_by_itinerary_id(1)
        self.assertIs(type(test), list)

    
    def test_get_activities_by_itinerary_id(self):
        """Test get_activities_by_itinerary_id function"""

        test = helper.get_activities_by_itinerary_id(1)
        self.assertIs(type(test), list)


    def test_serialize_itinerary_by_id(self):
        """Test serialize_itinerary_by_id function"""

        test = helper.serialize_itinerary_by_id(1)
        self.assertIs(type(test), dict)


    def test_list_activities_by_itinerary(self):
        """Test list_activities_by_itinerary function"""

        test = helper.list_activities_by_itinerary(1)
        self.assertIs(type(test), list)


    def test_list_notes_by_itinerary(self):
        """Test list_notes_by_itinerary function"""

        test = helper.list_notes_by_itinerary(1)
        self.assertIs(type(test), list)


    def test_json_itinerary_activities(self):
        """Test json_itinerary_activities function"""

        test = helper.json_itinerary_activities(1)
        self.assertIs(type(test), dict)


    def test_jsonify_all_itinerary_data(self):
        """Test jsonify_all_itinerary_data function"""

        test = helper.jsonify_all_itinerary_data(1)
        self.assertIs(type(test), dict)


    def test_create_dates_list(self):
        """Test create_dates_list function"""
        it = helper.get_itinerary_by_id(1)
        start, end = it.start_date, it.end_date
        test = helper.create_dates_list(start, end)
        self.assertIs(type(test), list)


    def test_users_to_notify(self):
        """Test users_to_notify function"""

        test = helper.users_to_notify(1, 'Bobby@bobby.com')
        self.assertIs(type(test), list)

    

if __name__ == '__main__':
    unittest.main()


# Currently no tests for: 
# crud.calculate_itinerary_days - considering removing this data from db anyway
# crud.get_latitude_longitude_for_itinerary - google api call
# helper.DateTimeEncoder - don't know how to write test for?
# helper.add_phone_to_user - don't know how to write test for?
# helper.send_itinerary_text_update - Twilio api call
