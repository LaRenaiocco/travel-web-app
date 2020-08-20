""" Script to seed our database with objects."""

import os
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb travel')
os.system('createdb travel')

model.connect_to_db(server.app)
model.db.create_all()

# Create users
crud.create_user('Alex@alex.com', 'test', 'Alex', 'Arbour')
crud.create_user('Bobby@bobby.com', 'test', 'Bobby', 'Bobbington')
crud.create_user('Claire@claire.com', 'test', 'Claire', 'Carson')
crud.create_user('Dawna@dawna.com', 'test', 'Dawna', 'Darcy')
crud.create_user('Eunice@eunice.com', 'test', 'Eunice', 'Ellis')
crud.create_user('Flo@flo.com', 'test', 'Flo', 'Florence')
crud.create_user('Grace@grace.com', 'test', 'Grace', 'Graceful')
crud.create_user('Hildy@hildy.com', 'test', 'Hildy', 'Hinter')
crud.create_user('Jamie@jamie.com', 'test', 'Jamie', 'Jameson')
crud.create_user('Kat@kat.com', 'test', 'Kat', 'King')


#create itineraries
crud.create_itinerary('London, UK', '2021-01-01', '2021-01-15', 15) # 51.4141076, -1.4000882
crud.create_itinerary('Bali, Indonesia', '2021-05-05', '2021-05-15', 11) #  -8.4556973, 114.510954
crud.create_itinerary('San Francisco, CA', '2020-12-01', '2020-12-05', 5) # 37.7576793, -122.5076413
crud.create_itinerary('Chicago, IL', '2020-11-25', '2020-11-28', 4) # 41.8333925, -88.0121674
crud.create_itinerary('Paris, France', '2021-03-03', '2021-03-09', 7) # 48.8588377, 2.2770192


#associate users with itineraries
crud.create_user_itinerary(1, 1)
crud.create_user_itinerary(2, 1)
crud.create_user_itinerary(3, 1)
crud.create_user_itinerary(4, 1)

crud.create_user_itinerary(10, 2)
crud.create_user_itinerary(9, 2)
crud.create_user_itinerary(8, 2)

crud.create_user_itinerary(1, 3)
crud.create_user_itinerary(4, 3)
crud.create_user_itinerary(7, 3)

crud.create_user_itinerary(7, 4)
crud.create_user_itinerary(6, 4)
crud.create_user_itinerary(5, 4)

crud.create_user_itinerary(1, 5)
crud.create_user_itinerary(2, 5)
crud.create_user_itinerary(3, 5)
crud.create_user_itinerary(5, 5)
crud.create_user_itinerary(8, 5)

#create activities for Itinerary

crud.create_activity(1, 'Lyceum Theatre', 'The Strand', 'London', 'SW1', '2021-01-02')
crud.create_activity(2, 'Traditional Dance Show', 'The beach', 'Bali', '11111')
crud.create_activity(3, 'Dinner with Friends', 'My house', 'Sebastopol', '95472', '2020-12-4', '17:00')
crud.create_activity(4, 'Fancy Restaurant', '1234 Any Street', 'Chicago', '12345')
crud.create_activity(5, 'Eiffel Tower', 'street', 'Paris', '234234', '2021-03-05', '09:00')

#create notes
crud.create_note(1, 1, 'Lets make sure we go to high tea!')
crud.create_note(5, 2, 'I wont eat escargot. Bleck!')
crud.create_note(3, 7, 'I want to go wine tasting!', '2020-12-02')
