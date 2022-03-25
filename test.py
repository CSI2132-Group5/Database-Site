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
            cursor.execute("SELECT * FROM User")
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
            cursor.execute("SELECT * FROM \"User\" WHERE \"SSN\"=%s", (ssn, ))
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
    print("[LOG] Fetching Employee from DB.")
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
        print("[ERROR] Failed to fetch user account.")
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
        print("[ERROR] Failed to fetch user account.")
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

def create_patient(user: models.Patient) -> bool:
    print("[LOG] Adding new patient to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_user(user.user_ssn)
            if existence_check is None:
                return False
            
            query = """INSERT INTO "Patient" (user_ssn, insurance_company) VALUES (%s,%s);"""
            cursor.execute(query, user.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new user into the database.")
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
            emp_existence_check = fetch_dentist(dentist.user_ssn)
            if emp_existence_check is not None:
                return False
            
            query = """INSERT INTO "Dentist" (specialty,user_ssn,works_at) VALUES (%s,%s,%s);"""
            cursor.execute(query, dentist.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new dentist into the database.")
        print(traceback.format_exc())
        return False

def create_employee(user: models.Employee) -> bool:
    print("[LOG] Adding new employee to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_employee(user.user_ssn)
            if existence_check is not None:
                return False
            
            query = """INSERT INTO "Employee" (role,type,salary,shift_start,shift_end,user_ssn) VALUES (%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, user.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new user into the database.")
        print(traceback.format_exc())
        return False

def create_patient_chart():
    try:
      with db.cursor() as cursor:
          query = """INSERT INTO "PatientChart" (dosage,status,time) VALUES(55,"admitted","12:00:00");"""
          cursor.execute(query)
          db.commit()
    except Exception:
        print("[ERROR] Failed to insert patient chart into the database.")
        print(traceback.format_exc())
        return False    

def delete_user(user: models.User)-> bool:
    print("[LOG] Deleting user from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_user(user.ssn)
            if existence_check is None:
                return False
            cursor.execute("DELETE FROM \"User\" WHERE \"SSN\"=%s", (user.ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete user from the database.")
        print(traceback.format_exc())
        return False

def create_branch(user: models.Branch)->bool:
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
      last_name = "Donnell", 
      gender = 1, 
      email_address = "samantha.d@gmail.com",
      date_of_birth = 0, 
      phone_number = "6138977890", 
      age = 30, 
      password = "samantha123",
      dateofbirth="1992-06-06"
    )
    patient1 = models.Patient(
        user_ssn="1433",
        insurance_company="Green Shield"
    )
    user3 = models.User(
        ssn = 1999, 
        address = "Topper Road", 
        house_number = 77, 
        street_name = "Brave Drive", 
        street_number = 49,
        city = "Ottawa",
        province = "Ontario", 
        first_name = "Joanna", 
        middle_name = "May", 
        last_name = "Parker", 
        gender = 1, 
        email_address = "joanna.parker@gmail.com",
        date_of_birth = 0, 
        phone_number = "6134569823", 
        age = 21, 
        password = "joanna123",
        dateofbirth= "2001-01-01"
    )
    dentist1 = models.Dentist(
        user_ssn=9999,
        specialty="Surgeon",
        works_at=0
    )
    employee1 = models.Employee(
        role="dentist",
        type="full-time",
        salary=80000,
        shift_start=9,
        shift_end=18,
        user_ssn= 9999
    )
    branch = models.Branch (
        name="Montana",
        address="ro road",
        street_name="Mission Street",
        street_number="12",
        city="Oshawa",
        province="Ontario",
        opening_time="09:00:06",
        closing_time="18:00:00",
        id="40"
    )
    #create_user(user)
    #create_user(user2)
    #create_user(user3)
    #delete_user(1999)
    #create_patient(patient1)
    #create_employee(employee1)
    #create_dentist(dentist1)
    #delete_user(user3)
    create_branch(branch)
  #  fetch_employee(1294)

