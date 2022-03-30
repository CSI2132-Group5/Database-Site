import config
import psycopg2

import traceback
import models

db = psycopg2.connect(
    host=config.POSTGRESQL_HOST,
    user=config.POSTGRESQL_USER,
    password=config.POSTGRESQL_PASSWORD,
    database=config.POSTGRESQL_DATABASE,
    port=config.POSTGRESQL_PORT
)

def fetch_users() -> models.User:
    print("[LOG] Fetching all users from the DB.")
    try: 
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"User\"")
            db_response = cursor.fetchall()
            
            return db_response
            
    except Exception:
        print("[ERROR] Failed to fetch all user accounts.")
        print(traceback.format_exc())
        return None
        
def fetch_user(ssn:int) -> models.User:
    print("[LOG] Fetching User from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"User\" WHERE \"SSN\"=%s", (ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.User.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch user account.")
        print(traceback.format_exc())
def fetch_dentist(user_ssn:int) -> models.Dentist:
    print("[LOG] Fetching Dentist from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Dentist\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Dentist.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch demtist account.")
        print(traceback.format_exc())

def fetch_admin(user_ssn:int) -> models.Admin:
    print("[LOG] Fetching Admin from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Receptionist\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Admin.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch admin account.")
        print(traceback.format_exc())

def fetch_employee(user_ssn:int) -> models.Employee:
    print("[LOG] Fetching Employee from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Employee\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Employee.from_postgres(db_response[0])
    except Exception:
        print("[ERROR] Failed to fetch employee account.")
        print(traceback.format_exc())

def fetch_patient(user_ssn:int) -> models.Patient:
    print("[LOG] Fetching Patient from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Patient\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Patient.from_postgres(db_response[0])
    except Exception:
        print("[ERROR] Failed to fetch patient account.")
        print(traceback.format_exc())

def fetch_branch_manager(user_ssn:int) -> models.BranchManager:
    print("[LOG] Fetching Branch Manager from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"BranchManager\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.BranchManager.from_postgres(db_response[0])
    except Exception:
        print("[ERROR] Failed to fetch branch manager account.")
        print(traceback.format_exc())

def fetch_patient_records():
    print("[LOG] Fetching all Patient Charts from DB")
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM PatientChart")
            db_response =cursor.fetchall()

        if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
        print(db_response)
        return models.PatientChart.from_postgres(db_response[0])
    except Exception:
        print("[ERROR] Failed to fetch patient charts.")
        print(traceback.format_exc())

def authenticate_user(username:str, password:str) -> models.User:
    print("[LOG] Authenticating User with db.")
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"User\" WHERE email_address like %s AND password LIKE %s", (username, password))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            # we only care about the first index (and should be the only)
            return models.User.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to authenticate a User's username and password.")
        print(traceback.format_exc())

def create_user(user: models.User) -> bool:
    print("[LOG] Adding new user to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_user(user.ssn)
            if existence_check is not None:
                return False
            
            query = """INSERT INTO "User" ("SSN", address, house_number, street_name, street_number, city, province, first_name, middle_name, last_name, gender, email_address, date_of_birth, phone_number, age, password,dateofbirth) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, user.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new user into the database.")
        print(traceback.format_exc())
        return False

def create_patient(patient: models.Patient) -> bool:
    print("[LOG] Adding new patient to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_user(patient.user_ssn)
            patient_existence_check = fetch_patient(patient.user_ssn)
            if existence_check is None or patient_existence_check is not None:
                return False
            
            query = """INSERT INTO "Patient" (user_ssn, insurance_company) VALUES (%s,%s);"""
            cursor.execute(query, patient.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new patient into the database.")
        print(traceback.format_exc())
        return False
def create_dentist(dentist: models.Dentist) -> bool:
    print("[LOG] Adding new dentist to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            emp_existence_check = fetch_employee(dentist.user_ssn)
            dentist_existence_check = fetch_dentist(dentist.user_ssn)
            if dentist_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "Dentist" (specialty,user_ssn,works_at) VALUES (%s,%s,%s);"""
            cursor.execute(query, dentist.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new dentist into the database.")
        print(traceback.format_exc())
        return False
def create_admin(admin: models.Admin) -> bool:
    print("[LOG] Adding new admin to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            emp_existence_check = fetch_employee(admin.user_ssn)
            admin_existence_check = fetch_admin(admin.user_ssn)
            if admin_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "Receptionist" (user_ssn,works_at) VALUES (%s,%s);"""
            cursor.execute(query, admin.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new admin into the database.")
        print(traceback.format_exc())
        return False

def create_branch_manager(branch_manager: models.BranchManager) -> bool:
    print("[LOG] Adding new branch manager to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            emp_existence_check = fetch_employee(branch_manager.user_ssn)
            branch_manager_existence_check = fetch_branch_manager(branch_manager.user_ssn)
            if branch_manager_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "BranchManager" (manages,user_ssn) VALUES (%s,%s);"""
            cursor.execute(query, branch_manager.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new branch manager into the database.")
        print(traceback.format_exc())
        return False

def create_employee(employee: models.Employee) -> bool:
    print("[LOG] Adding new employee to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_user(employee.user_ssn)
            emp_existence_check = fetch_employee(employee.user_ssn)
            if emp_existence_check is not None or existence_check is None:
                return False
            
            query = """INSERT INTO "Employee" (role,type,salary,shift_start,shift_end,user_ssn) VALUES (%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, employee.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new employee into the database.")
        print(traceback.format_exc())
        return False

def delete_employee(employee: models.Employee)->bool:
    print("[LOG] Deleting employee from the db.")
    try:
        with db.cursor() as cursor:
           existence_check = fetch_employee(employee.user_ssn)
           if existence_check is None:
                return False 
           cursor.execute("DELETE FROM \"Employee\" WHERE \"user_ssn\"=%s", (employee.user_ssn, ))
           db.commit()
            
           return True
    except Exception:
        print("[ERROR] Failed to delete employee from the database.")
        print(traceback.format_exc())
        return False

def delete_patient(patient: models.Patient)->bool:
    print("[LOG] Deleting patient from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_patient(patient.ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"Patient\" WHERE \"user_ssn\"=%s", (patient.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete patient from the database.")
        print(traceback.format_exc())
        return False

def delete_dentist(dentist: models.Dentist)->bool:
    print("[LOG] Deleting dentist from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_dentist(dentist.ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"Dentist\" WHERE \"user_ssn\"=%s", (dentist.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete dentist from the database.")
        print(traceback.format_exc())
        return False

def delete_admin(admin: models.Admin)->bool:
    print("[LOG] Deleting admin from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_admin(admin.user_ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"Receptionist\" WHERE \"user_ssn\"=%s", (admin.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete admin from the database.")
        print(traceback.format_exc())
        return False

def delete_branch_manager(branch_manager: models.BranchManager)->bool:
    print("[LOG] Deleting branch manager from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_branch_manager(branch_manager.user_ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"BranchManager\" WHERE \"user_ssn\"=%s", (branch_manager.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete branch manager from the database.")
        print(traceback.format_exc())
        return False

def create_patient_chart():
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "PatientChart" (dosage,status,time) VALUES();"""
          cursor.execute(query)
          db.commit()
    except Exception:
        print("[ERROR] Failed to insert patient chart into the database.")
        print(traceback.format_exc())
        return False    

def delete_user(ssn)-> bool:
    print("[LOG] Deleting user from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_user(ssn)
            if existence_check is None:
                return False
            cursor.execute("DELETE FROM \"User\" WHERE \"SSN\"=%s", (ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete user from the database.")
        print(traceback.format_exc())
        return False

def delete_branch(branch: models.Branch)->bool:
     print("[LOG] Deleting branch from the db")
     try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM \"Branch\" WHERE \"city\"=%s", (branch.city, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete branch from the database.")
        print(traceback.format_exc())
        return False

def create_branch(branch: models.Branch)->bool:
    print("[LOG] Creating branch in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "Branch" (name,address,street_name,street_number,city,province,opening_time,closing_time,id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
          cursor.execute(query, branch.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert branch into the database.")
        print(traceback.format_exc())
        return False    

def create_appointment(appointment: models.Appointment)->bool:
    print("[LOG] Creating appointment in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "Appointment" (id,date,start_time,end_time,status,assigned_room,located_at,appointment_patient,appointment_dentist) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
          cursor.execute(query, appointment.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert appointment into the database.")
        print(traceback.format_exc())
        return False   

def delete_appointment(appointment: models.Appointment)->bool:
     print("[LOG] Deleting appointment from the db")
     try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM \"Appointment\" WHERE \"id\"=%s", (appointment.id, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete appointment from the database.")
        print(traceback.format_exc())
        return False

def create_appointment(appointment: models.Appointment)->bool:
    print("[LOG] Creating appointment in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "Appointment" (id,date,start_time,end_time,status,assigned_room,located_at,appointment_patient,appointment_dentist) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
          cursor.execute(query, appointment.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert appointment into the database.")
        print(traceback.format_exc())
        return False  

def create_appointment_procedure(appointment_procedure: models.AppointmentProcedure)->bool:
    print("[LOG] Creating appointment procedure in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "AppointmentProcedure" (procedure_code,procedure_type,tooth_number,description,appointment_id,id,procedure_category) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
          cursor.execute(query, appointment_procedure.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert appointment procedure into the database.")
        print(traceback.format_exc())
        return False  

def delete_appointment_procedure(appointment_procedure: models.AppointmentProcedure)->bool:
     print("[LOG] Deleting appointment procedure from the db")
     try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM \"AppointmentProcedure\" WHERE \"id\"=%s", (appointment_procedure.id, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete appointment from the database.")
        print(traceback.format_exc())
        return False

def create_procedure_category(procedure_category: models.ProcedureCategory)->bool:
    print("[LOG] Creating procedure category in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "ProcedureCategory" (category_name,description,category_id) VALUES(%s,%s,%s);"""
          cursor.execute(query, procedure_category.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert appointment procedure into the database.")
        print(traceback.format_exc())
        return False  
def create_invoice(invoice: models.Invoice)->bool:
    print("[LOG] Creating invoice in the db.")
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "Invoice" (issue_date,total_charge,discount,penalty,id,receptionist_ssn) VALUES(%s,%s,%s,%s,%s,%s);"""
          cursor.execute(query, invoice.to_tuple())
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to insert invoice into the database.")
        print(traceback.format_exc())
        return False  
def update_user(user: models.User)->bool:
    print("[LOG] Updating user in the db.")
    try:
      with db.cursor() as cursor:
          query = """Update "User" SET "SSN"=%s,address=%s,house_number=%s,street_name=%s,street_number=%s,
          city=%s,province=%s,first_name=%s,middle_name=%s,last_name=%s,gender=%s,email_address=%s,date_of_birth=%s,
          phone_number=%,age=%s,password=%s,dateofbirth=%s WHERE "SSN"=%s;"""
          cursor.execute(query,[user.ssn,user.address,user.house_number,
          user.street_name,user.street_number,user.city,user.province,user.first_name,
          user.middle_name,user.last_name,user.gender,user.email_address,user.email_address,
          user.date_of_birth,user.phone_number,user.age,user.password,user.dateofbirth])
          db.commit()

          return True
    except Exception:
        print("[ERROR] Failed to update user into the database.")
        print(traceback.format_exc())
        return False  

if __name__ == "__main__":
    user = models.User(
        ssn = 1234, 
        address = "random road", 
        house_number = 52, 
        street_name = "clown drive", 
        street_number = 42,
        city = "Ottawa",
        province = "Ontario", 
        first_name = "Joe", 
        middle_name = "Robert", 
        last_name = "Smith", 
        gender = 0, 
        email_address = "joe.smith@gmail.com",
        date_of_birth = 0, 
        phone_number = "2345324455", 
        age = 25, 
        password = "b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3",
        dateofbirth="1970-03-03"
    )
    user2 = models.User(
      ssn = 9999,
      address = "nonono",
      house_number = 12,
      street_name = "Queen Street",
      street_number = 42,
      city = "Ottawa",
      province = "Ontario",
      first_name = "Samantha", 
      middle_name = "J", 
      last_name = "Donald", 
      gender = 1, 
      email_address = "samantha.d@gmail.com",
      date_of_birth = 0, 
      phone_number = "6138977890", 
      age = 30, 
      password = "samantha123",
      dateofbirth="1992-06-06"
    )
    patient1 = models.Patient(
        user_ssn="1430",
        insurance_company="Green Shield"
    )
    user3 = models.User(
        ssn = 1430, 
        address = "Lala Road", 
        house_number = 77, 
        street_name = "Lala Drive", 
        street_number = 49,
        city = "Ottawa",
        province = "Ontario", 
        first_name = "Mary", 
        middle_name = "Jane", 
        last_name = "Parker", 
        gender = 1, 
        email_address = "mary.parker@gmail.com",
        date_of_birth = 0, 
        phone_number = "6134569823", 
        age = 21, 
        password = "mary123",
        dateofbirth= "2001-01-01"
    )
    dentist1 = models.Dentist(
        user_ssn=1990,
        specialty="Surgeon",
        works_at=0
    )
    employee1 = models.Employee(
        role="dentist",
        type="full-time",
        salary=80000,
        shift_start=9,
        shift_end=18,
        user_ssn= 7547
    )
    branch = models.Branch (
        name="Res",
        address="nono road",
        street_name="Main Street",
        street_number="12",
        city="Hamilton",
        province="Ontario",
        opening_time="09:00:06",
        closing_time="18:00:00",
        id=37
    )
    appointment = models.Appointment (
        id = "12",
        date="20220202",
        start_time=9,
        end_time=10,
        status=0,
        assigned_room=934,
        located_at=0,
        appointment_patient=1433,
        appointment_dentist=1233
    )
    branchManager = models.BranchManager (
        user_ssn=7547,
        manages=0,
    )
    appointmentProcedure = models.AppointmentProcedure(
        procedure_code=22,
        procedure_type=2,
        tooth_number=20,
        description="n/a",
        appointment_id="12",
        id=56,
        procedure_category="wisdom teeth"
    ) 
    procedure_category1 = models.ProcedureCategory(
        category_name="wisdom teeth",
        description="n/a",
        category_id="0"
    )
    admin1 = models.Admin (
        user_ssn=1294,
        works_at=0
    )
    invoice1 = models.Invoice(
        issue_date="2022-03-04",
        total_charge=34.00,
        discount=23,
        penalty=0,
        id=1,
        receptionist_ssn=1294
    )
    #create_user(user)
    #create_user(user2)
    create_user(user3)
    #delete_user(1999)
    #create_admin(admin1)
    create_employee(employee1)
    create_branch_manager(branchManager)
    create_patient(patient1)
    #delete_patient(patient1)
    #create_invoice(invoice1)
    #delete_employee(employee1)
    
    #create_employee(employee1)
    #create_dentist(dentist1)
    #delete_user(user3)
    #create_branch(branch)
    #create_appointment(appointment)
    #delete_appointment(appointment)
    #delete_branch(branch)
    #fetch_employee(1294)
    #fetch_dentist(1233)
    #create_procedure_category(procedure_category1)
    #create_appointment_procedure(appointmentProcedure)
    update_user(user2)