""" Server for Operation Adventure."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "devLaRena"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/login', methods = ['POST'])
def login_user():
    """ Log in user."""

    email = request.form['email']
    password=request.form['password']
    user_object = crud.get_user_by_email(email)

    if user_object == None:
        flash('No account with this email exists. Please try again.')
        return redirect ('/')
    else:
        if password != user_object.password:
            flash('Incorrect Password. Please try again.')
            return redirect ('/')
        else:
            session['USERNAME'] = user_object.email
            # print(session['USERNAME'])
            print('session username set')
            return redirect (f'users/profile/{user_object.fname}')

@app.route('/users/profile/<fname>')
def show_user_profile(fname):
    """ Show logged in user profile."""

    email = session['USERNAME']
    user = crud.get_user_by_email(email)
    lname = user.lname
    itinerary_ids = crud.get_itinerary_ids_by_user(user)


        
    return render_template('user_profile.html', email=email, fname=fname, lname=lname)  


@app.route('/users/create-user')
def create_new_user():
    """Render new profile form."""

    return render_template('create_profile.html')

@app.route('/users/create-user', methods = ['POST'])
def new_user():
    """Create new profile."""

    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']

    user = crud.get_user_by_email(email)

    if user != None:
        flash('This email is already associated with an account. Please log in.')
        return redirect ('/')
    else:
        crud.create_user(email, password, fname, lname)
        flash('Your account has been created.  Please log in.')
        return redirect ('/')



@app.route('/users/itinerary')
def show_itinerary():
    """Show individual trip itinerary."""

    return render_template('my_trip.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)