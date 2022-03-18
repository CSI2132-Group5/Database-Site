from venv import create
from flask import (
    Flask, 
    request, 
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    LoginManager
)
from flask_login.utils import login_required
from flask_wtf import CSRFProtect

from db import authenticate_user, fetch_user, create_user

from datetime import datetime
import re

app = Flask(__name__)
app.config.from_pyfile('config.py')

# settup the login authentication
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def get_user(ssn):
    db_response = fetch_user(ssn)
    return db_response

# protect our page from CSRF attempts
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        seed_phrase = request.form.get("seedphrase")
        
        user = authenticate_user(username=username, password=seed_phrase)
        # if we see a None value, the username is wrong
        if user is None:
            print("User is None type")
            return render_template('login.html', wrong_password_or_user=True)
        else:
            # store the credentials and redirect to the dashboard
            login_user(user)
            return redirect(url_for('dashboard'))
    
    if current_user.is_authenticated:
        return redirect('dashboard')

    return render_template('login.html', wrong_password_or_user=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/admin/createuser', methods=["GET", "POST"])
@login_required
def create_user_page():
    if request.method == "POST":
        
        invalid_name = False  # will be marked as true if anything has been submitted empty
        first_name = request.form.get("first-name")
        middle_name = request.form.get("middle-name")
        last_name = request.form.get("last-name")
        # ensure none of the first/middle/last name entries are blank
        if (first_name == "") or (middle_name == "") or (last_name == ""):
            invalid_name = True
            
        invalid_age = False
        gender = int(request.form.get("gender"))
        # ensure that the geneder is a (0) male, (1) female, or (2) other
        if (gender < 0) or (gender > 2):
            invalid_age = True
        # the date of birth is sent via HTTP in the format YYYY-MM-DD, we need to convert to datetime
        date_of_birth = datetime.strptime(request.form.get("date-birth"), "%Y-%m-%d")
        # age can be sent as '', so if that is being sent to use attempting to convert this to an int
        # right away will create a str->int type conversion error (validate this first)
        if (request.form.get("age") != ""):
            age = int(request.form.get("age"))
            # we want to perform integer devision of the days elapsed (by 365) to determine whether the
            # number of elapsed years since present matches the age given/entered by/for the client
            years_difference = (datetime.now() - date_of_birth).days // 365
            # also ensure that the client is NOT under 13 years old
            if (age < 13) or (age != years_difference):
                invalid_age = True
        else:
            invalid_age = True
        
        invalid_address = False  # will be marked as true if anything has been submitted empty
        address = request.form.get("address")
        street_name = request.form.get("street-name")
        # verify that the address and street-name are not empty strings
        if (address != "") or (street_name == ""):
            invalid_address = True
        # house # can be sent as '', so if that is being sent to use attempting to convert this to an int
        # right away will create a str->int type conversion error (validate this first)
        if (request.form.get("house-number") != ""):
            house_number = int(request.form.get("house-number"))
            # ensure that we have not entered a negative house number (I don't think anyone has this)
            if house_number < 0:
                invalid_address = True
        else:
            invalid_address = True
            
        invalid_password = False
        password = request.form.get("password")
        # just check to make sure the password isn't empty and that it's at least 4 characters long
        # otherwise this can be considered a "weak" password choice
        if (password != "") or (len(password) < 4):
            invalid_password = True
        
        invalid_ssn = False
        # first check that the ssn is valid otherwise the int->str type conversion will fail
        if (request.form.get("ssn") != ""):
            ssn = int(request.form.get("ssn"))  # this will be used when we try and submit it to postgres
            # an SSN must be 9 characters long according to the Canadian government standard
            if len(request.form.get("ssn")) != 9:
                invalid_ssn = True
        else:
            invalid_ssn = True
            
        invalid_phone = False
        phone_number = request.form.get("phone-number")
        # regex found @ https://stackoverflow.com/questions/5294314/python-get-number-of-years-that-have-passed-from-date-string
        if not re.match("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", phone_number):
            invalid_phone = True
        
        # ensure that we have not generate a single error, if we have, update the HTML with the appropriate error hint
        if (not invalid_name) or (not invalid_address) or (not invalid_age) or (not invalid_password) or (not invalid_phone) or (not invalid_ssn):
            return render_template(
                "createuser.html",
                invalid_name=invalid_name,
                invalid_address=invalid_address,
                invalid_age=invalid_age,
                invalid_password=invalid_password,
                invalid_phone=invalid_phone,
                invalid_ssn=invalid_ssn
            )
        else:
            # give all the data in the form is valid, submit it to postgres
            
            # TODO - submit a user to the postgres db
            
            # no error has been generated, display that the user creation was successful
            return render_template(
                "createuser.html", 
                success=True
            )
    else:
        return render_template("createuser.html")

if __name__ == "__main__":
    app.run()