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
crud.create_itinerary('London, UK', '2021-01-01', '2021-01-08', 15, 51.4141076, -1.4000882)
crud.create_itinerary('Bali, Indonesia', '2021-05-05', '2021-05-15', 11, -8.4556973, 114.510954)
crud.create_itinerary('San Francisco, CA', '2020-12-01', '2020-12-05', 5, 37.7576793, -122.5076413)
crud.create_itinerary('Chicago, IL', '2020-11-25', '2020-11-28', 4, 41.8333925, -88.0121674)
crud.create_itinerary('Paris, France', '2021-03-03', '2021-03-09', 7, 48.8588377, 2.2770192)


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

crud.create_activity(1, 'Lyceum Theatre', '21 Wellington St, Covent Garden, London WC2E 7RQ, United Kingdom', 51.511619, -0.1223251, '2021-01-02', '20:00')
crud.create_activity(1, 'Wagamama', '17 Bedford St, Covent Garden, London WC2E 9HP, United Kingdom', 51.5107958, -0.12691, '2021-01-02', '17:00')
crud.create_activity(1, 'National Portrait Gallery', "St. Martin's Pl, Charing Cross, London WC2H 0HE, United Kingdom", 51.5094269, -0.1303103)
crud.create_activity(1, 'Warner Bros. Studio Tour London', 'Studio Tour Dr, Leavesden, Watford WD25 7LR, United Kingdom', 51.6903501, -0.4202619, '2021-01-06', '09:00')
crud.create_activity(1, 'Highclere Castle', 'Highclere Park, Highclere, Newbury RG20 9RN, United Kingdom', 51.3265934, -1.3628547, '2021-01-04', '13:00')
crud.create_activity(1, 'Victoria and Albert Museum', 'Cromwell Rd, Knightsbridge, London SW7 2RL, United Kingdom', 51.4966425, -0.1743687, activity_note="I don't know what day we should do this, but they have a cool fashion exhibit")
crud.create_activity(2, 'Aling-Aling Waterfall', 'Jl. Raya Desa Sambangan, Sambangan, Kec. Sukasada, Kabupaten Buleleng, Bali 81161, Indonesia', -8.2525684, 114.9480604)
crud.create_activity(3, 'Dinner with Friends', '5231 Wendell Lane, Sebastopol, CA, 95472', 38.348009, -122.7702767, '2020-12-4', '17:00')
crud.create_activity(4, 'The Girl and the Goat', '809 W Randolph St, Chicago, IL 60607', 41.884113, -87.6501642)
crud.create_activity(5, 'Eiffel Tower', 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France', 48.8583736, 2.2922926, '2021-03-05', '09:00')

#create notes
crud.create_note(1, 1, 'Lets make sure we go to high tea!')
crud.create_note(5, 2, 'I wont eat escargot. Bleck!')
crud.create_note(3, 7, 'I want to go wine tasting!', '2020-12-02')
