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

from db import (
    authenticate_user,
    fetch_branch,
    fetch_dentist, 
    fetch_user, 
    create_user,
    fetch_users,
    create_admin,
    create_dentist,
    create_employee,
    create_patient,
    create_branch_manager,
    fetch_appointments,
    fetch_branch_id
)

from utils import user_permission_level

import models, hashlib, re
from datetime import datetime

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
        try:
            date_of_birth = datetime.strptime(request.form.get("date-birth"), "%Y-%m-%d")
        except ValueError as ve:
            date_of_birth = None
        # age can be sent as '', so if that is being sent to use attempting to convert this to an int
        # right away will create a str->int type conversion error (validate this first)
        if (date_of_birth != None) and (request.form.get("age") != ""):
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
        if (address == "") or (street_name == ""):
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

        if (request.form.get("street-number") != ""):
            street_number = int(request.form.get("street-number"))
            # ensure that we have not entered a negative house number (I don't think anyone has this)
            if street_number < 0:
                invalid_address = True
        else:
            invalid_address = True
        
        if (request.form.get("city") != ""):
            city = (request.form.get("city"))
        else:
            invalid_address= True
        
        if (request.form.get("province") != ""):
            province = (request.form.get("province"))
        else:
            invalid_address = True

        invalid_password = False
        password = request.form.get("password")
        # just check to make sure the password isn't empty and that it's at least 4 characters long
        # otherwise this can be considered a "weak" password choice
        if (password == "") or (len(password) < 4):
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
            
        invalid_email = False
        email = request.form.get("email")
        # regex found @ https://regexlib.com/Search.aspx?k=email&AspxAutoDetectCookieSupport=1
        if (email == "") or (not re.match("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", email)):
            invalid_email = True
        
        # if one of the user constraints fail (as defined below) let the user know this
        invalid_role = False
        
        is_patient = False
        if ("is-patient" in request.form) and ("insurance" in request.form):
            is_patient = True
            insurance = request.form.get("insurance")
         
        is_dentist = False
        is_admin = False
        is_manager = False   
        # an admin cannot be a dentist, and a dentist cannot be an admin
        if ("is-employee" in request.form):
            if ("is-dentist" in request.form) and ("works-at" in request.form) and ("specialty" in request.form):
                is_dentist = True
                works_at = request.form.get("works-at")
                role = request.form.get("role")
                type = request.form.get("type")
                salary = request.form.get("salary")
                shift_start = request.form.get("shift-start")
                shift_end = request.form.get("shift-end")
                specialty = request.form.get("specialty")
            
            if (not is_dentist) and ("is-admin" in request.form) and ("works-at" in request.form) and ("role" in request.form) and ("type" in request.form) and ("salary" in request.form) and ("shift-start" in request.form) and ("shift-end" in request.form):
                is_admin = True
                works_at = request.form.get("works-at")
                role = request.form.get("role")
                type = request.form.get("type")
                salary = request.form.get("salary")
                shift_start = request.form.get("shift-start")
                shift_end = request.form.get("shift-end")
            else:
                invalid_role = True
        
            # a branch manager must be either an admin or a dentist
            if ("is-manager" in request.form) and (is_admin or is_dentist):
                is_manager = True   
                manages = works_at
            else:
                invalid_role = True
        
        # ensure that we have not generate a single error, if we have, update the HTML with the appropriate error hint
        if invalid_name or invalid_address or invalid_age or invalid_password or invalid_phone or invalid_ssn or invalid_role:
            return render_template(
                "createuser.html",
                invalid_name=invalid_name,
                invalid_address=invalid_address,
                invalid_age=invalid_age,
                invalid_password=invalid_password,
                invalid_phone=invalid_phone,
                invalid_ssn=invalid_ssn,
                invalid_email=invalid_email,
                invalid_role=invalid_role,
                previous_form=request.form,
            )
        else:
            # give all the data in the form is valid, submit it to postgres
    
          create_user(models.User(
            ssn=ssn,
            address=address,
            house_number=house_number,
            street_name=street_name,
            street_number=street_number,
            city=city,
            province=province,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            email_address=email,
            date_of_birth=0,
            phone_number=phone_number,
            age=age,
            password=str(hashlib.sha256(password.encode('utf-8')).hexdigest()),
            dateofbirth=date_of_birth
        )
        )
        if is_admin or is_dentist or is_manager:
           create_employee(models.Employee(
               user_ssn=ssn,
               role=role,
               type=type,
               salary=salary,
               shift_start=shift_start,
               shift_end=shift_end
           ))
        if is_admin:
            create_admin(models.Admin(
               user_ssn=ssn,
               works_at=works_at 
            )
            )
        if is_dentist:
            create_dentist(models.Dentist (
               specialty=specialty,
               user_ssn=ssn,
               works_at=works_at
            )
            )
        if is_manager:
            create_branch_manager(models.BranchManager(
               manages=manages,
               user_ssn=ssn
            )
            )
        if is_patient:
            create_patient(models.Patient(
              user_ssn=ssn,
              insurance_company=insurance 
            ))
        
            # no error has been generated, display that the user creation was successful
        return render_template(
                "createuser.html", 
                success=True,
                previous_form=request.form
        )
    else:
        permission = user_permission_level(current_user.ssn)
        if not ((permission == models.PermissionLevel.ADMIN) or (permission == models.PermissionLevel.ADMIN_PATIENT)):
            return redirect(url_for('dashboard'))
            # TODO - TELL THE USER THEY DON'T HAVE PERMISSION
        
        return render_template("createuser.html")

@app.route('/dentist/createprocedure', methods=["GET", "POST"])
@login_required
def create_procedure_page():
    if request.method == "POST":
        
        invalid_category = False  # will be marked as true if category has been submitted empty
        category = request.form.get("category")

        # ensure the category is not blank
        if (category == ""):
            print(category)
            invalid_category = True


        invalid_description= False  # will be marked as true if description has been submitted empty
        description = request.form.get("description")

        # ensure the description is not blank
        if (description == ""):
            print(description)
            invalid_description = True
            
        invalid_procedure_id = False
        procedure_id=request.form.get("procedure_id") # will be marked as true if procedure id has been submitted empty

        # ensure the procedure id is not blank
        if (procedure_id == "") or (int(request.form.get("procedure_id")) <= 0):
            print(procedure_id)
            invalid_procedure_id = True

        invalid_appointment_id = False
        appointment_id=request.form.get("appointment_id") # will be marked as true if appointment id has been submitted empty

        # ensure the appointment id is not blank
        if (appointment_id == "") or (int(request.form.get("appointment_id")) <= 0):
            print(appointment_id)
            invalid_appointment_id = True

        invalid_procedure_code = False
        procedure_code=request.form.get("procedure_code") # will be marked as true if procedure code has been submitted empty

        # ensure the procedure code is not blank and equals 15 as required in our domain integrity constraints
        if (procedure_code == "") or (len(procedure_code) != 15):
            print(procedure_code)
            invalid_procedure_code = True

        invalid_procedure_type = False
        procedure_type=request.form.get("procedure_type") # will be marked as true if procedure type has been submitted empty

        # ensure the procedure type is not blank
        if (procedure_type == ""):
            print(procedure_type)
            invalid_procedure_type = True

        invalid_tooth_number = False
        tooth_number=request.form.get("tooth_number") # will be marked as true if tooth number has been submitted empty

        # ensure the tooth number is not blank and is between 1-32 inclusively
        if (tooth_number == "") or (int(request.form.get("tooth_number")) <= 0) or (int(request.form.get("tooth_number")) >= 33):
            print(tooth_number)
            invalid_tooth_number = True
        
        
        # ensure that we have not generate a single error, if we have, update the HTML with the appropriate error hint
        if invalid_category or invalid_description or invalid_procedure_id or invalid_appointment_id or invalid_procedure_code or invalid_procedure_type or invalid_tooth_number:
            return render_template(
                "createprocedure.html",
                invalid_category=invalid_category,
                invalid_description=invalid_description,
                invalid_procedure_id=invalid_procedure_id,
                invalid_appointment_id=invalid_appointment_id,
                invalid_procedure_code=invalid_procedure_code,
                invalid_procedure_type=invalid_procedure_type,
                invalid_tooth_number=invalid_tooth_number,
                previous_form=request.form,
            )
        else:
            # give all the data in the form is valid, submit it to postgres
            
            # TODO - submit a procedure to the postgres db
            
            # no error has been generated, display that the procedure creation was successful
            return render_template(
                "createprocedure.html", 
                success=True,
                previous_form=request.form
            )
    else:
        permission = user_permission_level(current_user.ssn)
        if not ((permission == models.PermissionLevel.DENTIST) or (permission == models.PermissionLevel.DENTIST_PATIENT)):
            return redirect(url_for('dashboard'))
            # TODO - TELL THE USER THEY DON'T HAVE PERMISSION
        
        return render_template("createprocedure.html")


@app.route('/admin/createappointment', methods=["GET", "POST"])
@login_required
def create_appointment_page():
    if request.method == "POST":
        

        invalid_appointment_id = False
        appointment_id=request.form.get("appointment_id") # will be marked as true if appointment id has been submitted empty

        # ensure the appointment id is not blank and is a value greater than 0
        if (appointment_id == "") or (int(request.form.get("appointment_id")) <= 0):
            print(appointment_id)
            invalid_appointment_id = True


        invalid_appointment_date = False
        appointment_date=request.form.get("appointment_date") # will be marked as true if appointment date has been submitted empty

        # ensure the appointment date is not blank
        if (appointment_date == ""):
            print(appointment_date)
            invalid_appointment_date = True

        invalid_start_time = False
        start_time=request.form.get("start_time") # will be marked as true if start time has been submitted empty

        # ensure the start time is not blank
        if (start_time == ""):
            print(start_time)
            invalid_start_time = True

        invalid_end_time = False
        end_time=request.form.get("end_time") # will be marked as true if end time has been submitted empty

        # ensure the end time is not blank
        if (end_time == ""):
            print(end_time)
            invalid_end_time = True

        invalid_assigned_room = False
        assigned_room=request.form.get("assigned_room") # will be marked as true if assigned room has been submitted empty

        # ensure the assigned room is not blank
        if (assigned_room == ""):
            print(assigned_room)
            invalid_assigned_room = True

        invalid_located_at  = False
        located_at=request.form.get("located_at") # will be marked as true if location has been submitted empty

        # ensure the location is not blank
        if (located_at == ""):
            print(located_at)
            invalid_located_at = True

        invalid_patient_id = False
        patient_id=request.form.get("patient_id") # will be marked as true if patient id has been submitted empty

        # ensure the patient id is not blank and is a value greater than 0
        if (patient_id == "") or (int(request.form.get("patient_id")) <= 0):
            print(patient_id)
            invalid_patient_id = True

        invalid_dentist_id = False
        dentist_id=request.form.get("dentist_id") # will be marked as true if dentist id has been submitted empty

        # ensure the dentist id is not blank and is a value greater than 0
        if (dentist_id == "") or (int(request.form.get("dentist_id")) <= 0):
            print(dentist_id)
            invalid_dentist_id = True

        invalid_status = False
        status = int(request.form.get("status"))
        # ensure that the appointment status is (0) no show, (1) cancelled, (2) completed, or unscheduled
        if (status < 0) or (status > 3):
            invalid_status = True


        invalid_appointment_type = False
        appointment_type = int(request.form.get("appointment_type"))
        # ensure that the appointment type is a (0) check up, or (1) surgery
        if (appointment_type < 0) or (appointment_type > 1):
            invalid_appointment_type = True
        
        # ensure that we have not generate a single error, if we have, update the HTML with the appropriate error hint
        if invalid_appointment_id or invalid_appointment_date or invalid_start_time or invalid_end_time or invalid_assigned_room or invalid_located_at or invalid_patient_id or invalid_dentist_id or invalid_status or invalid_appointment_type:
            return render_template(
                "createappointment.html",
                invalid_appointment_id=invalid_appointment_id,
                invalid_appointment_date=invalid_appointment_date,
                invalid_start_time=invalid_start_time,
                invalid_end_time=invalid_end_time,
                invalid_assigned_room=invalid_assigned_room,
                invalid_located_at=invalid_located_at,
                invalid_patient_id=invalid_patient_id,
                invalid_dentist_id=invalid_dentist_id,
                invalid_status=invalid_status,
                invalid_appointment_type=invalid_appointment_type,

            )
        else:
            # give all the data in the form is valid, submit it to postgres
            
            # TODO - submit an appointment to the postgres db
            
            # no error has been generated, display that the appointment creation was successful
            return render_template(
                "createappointment.html", 
                success=True,
                previous_form=request.form
            )
    else:
        permission = user_permission_level(current_user.ssn)
        if not ((permission == models.PermissionLevel.ADMIN) or (permission == models.PermissionLevel.ADMIN_PATIENT)):
            return redirect(url_for('dashboard'))
            # TODO - TELL THE USER THEY DON'T HAVE PERMISSION
            
        return render_template("createappointment.html")

@app.route('/admin/viewappointments', methods=["GET", "POST"])
@login_required
def view_appointments_page():
    appointments = fetch_appointments()
    
    appointments_prime = []
    # update IDs to show plaintext first/last names that will be easier for
    # the user to read on the HTML render
    for appointment in appointments:
        
        appointment_prime = appointment[0:6]
        # update the branch field, having branch id is ~ bad ui
        branch = fetch_branch_id(appointment[6])
        if branch != None:
            branch_name = branch.name
        else:
            branch_name = "ERROR" 
        
        # update the user field, we don't want to display their ID ~ bad ui
        client = fetch_user(appointment[7])
        if client != None:
            # we only want clients to be able to view their own records, therefore
            # if they are a client ~ block out all other client records
            if (user_permission_level(current_user.ssn) == models.PermissionLevel.PATIENT) and (client.ssn != current_user.ssn):
                continue
            client_name_c =  f"{client.first_name} {client.last_name}"  # concatenate the client's name
        else:
            client_name_c = "ERROR"
        
        # update the dentist field, we don't want to display their ID ~ bad ui
        dentist = fetch_user(fetch_dentist(appointment[8]).user_ssn)
        if dentist != None:
            dentist_name_c = f"{dentist.first_name} {dentist.last_name}"  # concatenate the dentist's name
        else:
            dentist_name_c = "ERROR"
        
        appointments_prime.append(appointment_prime + (branch_name, client_name_c, dentist_name_c))
        
    return render_template("viewappointments.html", appointments=appointments_prime, permission=user_permission_level(current_user.ssn))
    
@app.route('/admin/viewuser', methods=["GET", "POST"])
@login_required
def view_user_page():
    users = fetch_users()
    
    permission = user_permission_level(current_user.ssn)
    print(permission)
    if not ((permission == models.PermissionLevel.ADMIN) or (permission == models.PermissionLevel.ADMIN_PATIENT)):
        for user in users:
            if user.ssn != current_user.ssn:
                users.remove(user)
    
    return render_template(
        "users.html", 
         users=users
    )


if __name__ == "__main__":
    app.run()