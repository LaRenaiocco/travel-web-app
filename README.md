# <img src="https://github.com/LaRenaiocco/travel-web-app/blob/master/static/adventure_awaits.png" alt="Adventure Awaits">
Adventure Awaits was inspired by my love of travel, and in particular traveling with friends.  Also the fact that I am always the one keeping everyone and everything organized leading up to a trip and finding all the best activities and deals.  Adventure Awaits allows users to create an account, set up unlimited itineraries for future trips, and link those itineraries with their travel mates so that a user and friends can collaboratively plan the perfect adventure!

## About the Developer
Before attending Hackbright Academy, LaRena spent most of her adult life clowning around in the circus (yes, you read that right).  She studied Theatre in college and then honed her circus and clowning skills at the San Francisco Clown Conservatory.  LaRena spent 8 years touring full time in the US, Mexico and Japan with Ringling Bros. and Barnum & Bailey as well as Kinoshita Circus. Despite her passion for travel, being on the road 52 weeks a year can wear out even the most seasoned traveller.  Looking to live in one place and ready for the next step in her career, coupled with massive amounts of time in the current pandemic, LaRena discovered a love for software development and has enjoyed putting her previously unused math and logic skills to good use and learning to code.


## Deployment
 http://adventure-awaits.fun/

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future Features](#future)
* [Installation](#installation)
* [License](#license)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* Jinja2
* PostgresQL
* SQLAlchemy ORM
* JavaScript
* jQuery
* HTML
* CSS
* Bootstrap
* Google Maps for JavaScript
* Google Geocoder
* Google Places
* Twilio

## <a name="features"></a>Features

#### Landing Page
Users  can register or login on the Jinja2 and Javascript rendered landing page. Passwords are encrypted using argon2 hashing for user security.

![alt text](https://media.giphy.com/media/TJV64Sf5avhAVQXchr/giphy.gif "Adventure Awaits landing page")

#### User Profile Page
After a user has created an account and logged in they will be redirected to their profile page.  Here the user can see all of their existing trips, plan a new trip by entering a place and dates, join an existing trip that friends are planning, and activate or deactivate text updates about their trips. The text update feature uses the Twilio API.

![alt text](https://media.giphy.com/media/YMXyE98g8UaJ3roZfy/giphy.gif "Adventure Awaits profile page")

#### Itinerary Pages
Users are linked to their fellow travellers through the itinerary page.  All users with the access code can join a trip together and this is the space to collaborate on the perfect adventure.  Users can see their itinerary with all activities broken down by day and time for a trip.  Undated activities will appear at the bottom of the itinerary.  All activities will also appear on the trip map, and clicking a marker will quickly show the user what day their activity is planned for.  This space also allows users to leave notes and ideas for each other regarding the trip, see which friends are linked to this trip as well as print their itinerary.

![alt text](https://media.giphy.com/media/UokE1YPakB14XCYO0z/giphy.gif "Adventure Awaits itinerary page")

#### Activity Search
The activity search page is linked to the itinerary and features an autocomplete map. Both maps are rendered using the Google Maps JavaScript API with the help of Google Places and Google Geocoder.  Users can search for museums, restaurants and activities and will be offered autocomplete suggestions based on the latitude and longitude of their trip.  Once an activity is selected, the user can add a date, time and additional notes if desired before adding the item to their trip.

![alt text](https://media.giphy.com/media/L0GkAEonzBmvlswL4L/giphy.gif "Adventure Awaits activity search")

## <a name="future"></a>The Future of Adventure Awaits
There are lots of new features planned for additional sprints:
* Archiving of past trips
* Functionality to edit or delete activities and notes from itineraries
* Adding a currency converter and IOU system so users can keep track of who paid for what on a trip.
* Integrating a flight search and hotel API

The goal is to make this a one stop travel planning app that includes everything a user needs to plan the perfect trip all in one place.

## <a name="installation"></a>Installation
To run Adventure Awaits on your own machine:

Install PostgresQL (Mac OSX)

Clone or fork this repo:
```
https://github.com/LaRenaiocco/travel-web-app
```

Create and activate a virtual environment inside your Adventure Awaits directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Twilio API](https://www.twilio.com/try-twilio/)

Sign up to use the [Google Maps Javascript, Google Places and Geocoder APIs](https://cloud.google.com/maps-platform/)

You will need to register for 2 API keys.  One will be used in the JavaScript front-end and one for the Python back-end.  Your front-end API key will need to be locked to your personal IP address and included in your script tags, the back-end key will need to be saved as below:


Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export TWILIO_API_KEY="YOUR_KEY_HERE"
export TWILIO_AUTH_TOKEN="YOUR_TOKEN_HERE"
export TWILIO_PHONE="YOUR_TWILIO_PHONE_NUMBER"
export GOOGLE_API_KEY="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_ID_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb travel
python3.6 model.py
```

Run the app:

```
python3.6 server.py
```

You can now navigate to 'localhost:5000/' to access Adventure Awaits.

## <a name="license"></a>License
The MIT License (MIT) Copyright (c) 2016 Agne Klimaite

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.