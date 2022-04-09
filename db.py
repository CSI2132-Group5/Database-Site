import string
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
        return False

###################################

# User queries
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
        return False

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

###################################

# Employee queries
def create_employee(employee: models.Employee) -> bool:
    print("[LOG] Adding new employee to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            existence_check = fetch_user(user.ssn)
            emp_existence_check = fetch_employee(employee.user_ssn)
            if emp_existence_check is not None or existence_check is not None:
                return False
            
            query = """INSERT INTO "Employee" (role,type,salary,shift_start,shift_end,user_ssn) VALUES (%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, employee.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new employee into the database.")
        print(traceback.format_exc())
        return False

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
        return False

def delete_employee(employee: models.Employee)->bool:
    print("[LOG] Deleting employee from the db.")
    try:
        with db.cursor() as cursor:
            employee_existence_check = fetch_employee(employee.user_ssn)
            if employee_existence_check is None:
                    return False 
            cursor.execute("DELETE FROM \"Employee\" WHERE \"user_ssn\"=%s", (employee.user_ssn, ))
            db.commit()
                
            return True
    except Exception:
        print("[ERROR] Failed to delete employee from the database.")
        print(traceback.format_exc())
        return False

###################################

# Patient queries
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
        return False

def delete_patient(patient: models.Patient)->bool:
    print("[LOG] Deleting patient from the db.")
    try:
        with db.cursor() as cursor:
            patient_existence_check = fetch_patient(patient.user_ssn)
            if patient_existence_check is None:
               return False
            cursor.execute("DELETE FROM \"Patient\" WHERE \"user_ssn\"=%s", (patient.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete patient from the database.")
        print(traceback.format_exc())
        return False

def fetch_patients():
    print("[LOG] Fetching all patients from the DB.")
    try: 
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"User\" as u JOIN \"Patient\" as p ON u.\"SSN\"=p.user_ssn") 
            db_response = cursor.fetchall()
            
            return db_response
            
    except Exception:
        print("[ERROR] Failed to fetch all patient accounts.")
        print(traceback.format_exc())
        return None

###################################

# Dentist queries
def create_dentist(dentist: models.Dentist) -> bool:
    print("[LOG] Adding new dentist to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            branch_id_existence_check = fetch_branch_id(dentist.works_at)
            emp_existence_check = fetch_employee(dentist.user_ssn)
            dentist_existence_check = fetch_dentist(dentist.user_ssn)
            if branch_id_existence_check is not None or dentist_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "Dentist" (specialty,user_ssn,works_at) VALUES (%s,%s,%s);"""
            cursor.execute(query, dentist.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new dentist into the database.")
        print(traceback.format_exc())
        return False

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

###################################

# Admin queries
def create_admin(admin: models.Admin) -> bool:
    print("[LOG] Adding new admin to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            branch_id_existence_check = fetch_branch_id(admin.works_at)
            emp_existence_check = fetch_employee(admin.user_ssn)
            admin_existence_check = fetch_admin(admin.user_ssn)
            if branch_id_existence_check is not None or admin_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "Receptionist" (user_ssn,works_at) VALUES (%s,%s);"""
            cursor.execute(query, admin.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new admin into the database.")
        print(traceback.format_exc())
        return False

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

###################################

# Branch manager queries
def create_branch_manager(branchManager: models.BranchManager) -> bool:
    print("[LOG] Adding new branch manager to the db.")
    try:
        with db.cursor() as cursor:
            # verify whether the ssn already exists in the database, if it does, don't attempt
            # to perform an SQL insertion
            #     -> as insert is expensive because of the class to tuple conversion
            #existence_check = fetch_user(u.user_ssn)
            branch_manager_manages_existence_check = fetch_branch_id(branchManager.manages)
            emp_existence_check = fetch_employee(branchManager.user_ssn)
            branch_manager_existence_check = fetch_branch_manager(branchManager.user_ssn)
            if branch_manager_manages_existence_check is not None or branch_manager_existence_check is not None or emp_existence_check is None:
                return False
            
            query = """INSERT INTO "BranchManager" (manages,user_ssn) VALUES (%s,%s);"""
            cursor.execute(query, branchManager.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new branch manager into the database.")
        print(traceback.format_exc())
        return False

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
        return False

def delete_branch_manager(branchManager: models.BranchManager)->bool:
    print("[LOG] Deleting branch manager from the db.")
    try:
        with db.cursor() as cursor:
            existence_check = fetch_branch_manager(branchManager.user_ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"BranchManager\" WHERE \"user_ssn\"=%s", (branchManager.user_ssn, ))
            db.commit()
            
            return True
    except Exception:
        print("[ERROR] Failed to delete branch manager from the database.")
        print(traceback.format_exc())
        return False

###################################

# Branch queries
def fetch_branch_id(id:string) -> models.Branch:
    print("[LOG] Fetching Branch id from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Branch\" WHERE \"id\"=%s", (id, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Branch.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch Branch id.")
        print(traceback.format_exc())
        return False
        
def fetch_branches() -> models.Branch:
    print("[LOG] Fetching all branches from the DB.")
    try: 
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Branch\"")
            db_response = cursor.fetchall()
            return db_response

    except Exception:
        print("[ERROR] Failed to fetch all branches.")
        print(traceback.format_exc())
        return None

def fetch_branch(city:string) -> models.Branch:
    print("[LOG] Fetching Branch city from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Branch\" WHERE \"city\"=%s", (city, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Branch.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch Branch.")
        print(traceback.format_exc())
        return False

def delete_branch(branch: models.Branch)->bool:
     print("[LOG] Deleting branch from the db")
     try:
        with db.cursor() as cursor:
            branch_existence_check = fetch_branch(branch.city)
            if branch_existence_check is None:
                return False
            
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
            branch_id_existence_check = fetch_branch_id(branch.id)
            branch_existence_check = fetch_branch(branch.city)
            if branch_id_existence_check is not None or branch_existence_check is not None:
                return False
            
            query = """INSERT INTO "Branch" (name,address,street_name,street_number,city,province,opening_time,closing_time,id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, branch.to_tuple())
            db.commit()

            return True
    except Exception:
        print("[ERROR] Failed to insert branch into the database.")
        print(traceback.format_exc())
        return False    

###################################

# Appointment queries
def create_appointment(appointment: models.Appointment)->bool:
    print("[LOG] Creating appointment in the db.")
    try:
      with db.cursor() as cursor:
            appointment_dentist_existence_check = fetch_dentist(appointment.appointment_dentist)
            appointment_patient_existence_check = fetch_patient(appointment.appointment_patient)
            appointment_located_at_existence_check = fetch_branch_id(appointment.located_at)
            appointment_id_existence_check = fetch_appointment_id(appointment.id)
            if appointment_dentist_existence_check is None or appointment_patient_existence_check is None or appointment_located_at_existence_check is None or appointment_id_existence_check is None:
                return False
            
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
            appointment_id_existence_check = fetch_appointment_id(appointment.id)
            if appointment_id_existence_check is None:
                return False
            
            cursor.execute("DELETE FROM \"Appointment\" WHERE \"id\"=%s", (appointment.id, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete appointment from the database.")
        print(traceback.format_exc())
        return False

def fetch_appointment_id(id:int) -> models.Appointment:
    print("[LOG] Fetching prcedure category from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"AppointmentProcedure\" WHERE \"id\"=%s", (id, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.Appointment.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch procedur category.")
        print(traceback.format_exc())
        return False

###################################

# Appointment procedure queries
def create_appointment_procedure(appointmentProcedure: models.AppointmentProcedure)->bool:
    print("[LOG] Creating appointment procedure in the db.")
    try:
      with db.cursor() as cursor:
            appointment_id_category_existence_check = fetch_appointment_id(appointmentProcedure.appointment_id)
            appointment_procedure_category_existence_check = fetch_procedure_category(appointmentProcedure.procedure_category)
            appointment_procedure_existence_check = fetch_appointment_procedure_id(appointmentProcedure.id)
            if appointment_procedure_category_existence_check is not None or appointment_procedure_existence_check is not None or appointment_id_category_existence_check is not None:
                return False
            
            query = """INSERT INTO "AppointmentProcedure" (procedure_code,procedure_type,tooth_number,description,appointment_id,id,procedure_category) VALUES(%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, appointmentProcedure.to_tuple())
            db.commit()

            return True
    except Exception:
        print("[ERROR] Failed to insert appointment procedure into the database.")
        print(traceback.format_exc())
        return False  

def fetch_appointment_procedure_id(id:int) -> models.AppointmentProcedure:
    print("[LOG] Fetching prcedure category from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"AppointmentProcedure\" WHERE \"id\"=%s", (id, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.AppointmentProcedure.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch procedure category.")
        print(traceback.format_exc())
        return False

def delete_appointment_procedure(appointmentProcedure: models.AppointmentProcedure)->bool:
     print("[LOG] Deleting appointment procedure from the db")
     try:
        with db.cursor() as cursor:
            appointment_procedure_id_existence_check = fetch_appointment_procedure_id(appointmentProcedure.id)
            if appointment_procedure_id_existence_check is None:
                return False
            
            cursor.execute("DELETE FROM \"AppointmentProcedure\" WHERE \"id\"=%s", (appointmentProcedure.id, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete appointment from the database.")
        print(traceback.format_exc())
        return False

###################################

# Procedure category queries
def create_procedure_category(procedureCategory: models.ProcedureCategory)->bool:
    print("[LOG] Creating procedure category in the db.")
    try:
      with db.cursor() as cursor:
            procedure_category_existence_check = fetch_branch_id(procedureCategory.category_id)
            category_name_existence_check = fetch_procedure_category(procedureCategory.category_name)
            if procedure_category_existence_check is not None or category_name_existence_check is not None:
                return False
            
            query = """INSERT INTO "ProcedureCategory" (category_name,description,parent_category,category_id) VALUES(%s,%s,%s,%s);"""
            cursor.execute(query, procedureCategory.to_tuple())
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
def update_user(user: models.User,patient:models.Patient)->bool:
    print("[LOG] Updating patient in the db.")
    try:
      with db.cursor() as cursor:
          query = """UPDATE "User" SET "SSN"=%s,address=%s,house_number=%s,street_name=%s,street_number=%s,
          city=%s,province=%s,first_name=%s,middle_name=%s,last_name=%s,gender=%s,email_address=%s,date_of_birth=%s,
          phone_number=%s,age=%s,password=%s,dateofbirth=%s WHERE \"SSN\"=%s;"""
          cursor.execute(query,(user.ssn,user.address,user.house_number,
          user.street_name,user.street_number,user.city,user.province,user.first_name,
          user.middle_name,user.last_name,user.gender,user.email_address,user.date_of_birth,user.phone_number,user.age,user.password,user.dateofbirth,user.ssn,))
          db.commit()
          query_two = """UPDATE "Patient" SET user_ssn=%s,insurance_company=%s WHERE \"user_ssn\"=%s;"""
          cursor.execute(query_two,(patient.user_ssn,patient.insurance_company,patient.user_ssn,))
          db.commit()
          return True
    except Exception:
        print("[ERROR] Failed to update patient in the database.")
        print(traceback.format_exc())
        return False  


def fetch_appointment_procedures()->models.AppointmentProcedure:
    print("[LOG] Fetching all appointment procedures from the DB.")
    try: 
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"AppointmentProcedure\"")
            db_response = cursor.fetchall()
            
            return db_response
    except Exception:
        print("[ERROR] Failed to fetch all appointment procedures.")
        print(traceback.format_exc())
        return None

def fetch_appointments()->models.Appointment:
    print("[LOG] Fetching all appointments from the DB.")
    try: 
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Appointment\"")
            db_response = cursor.fetchall()
            
            return db_response
    except Exception:
        print("[ERROR] Failed to fetch all appointments.")
        print(traceback.format_exc())
        return None
def fetch_procedure_category(category_name:int) -> models.ProcedureCategory:
    print("[LOG] Fetching prcedure category from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ProcedureCategory\" WHERE \"category_name\"=%s", (category_name, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.ProcedureCategory.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch procedur category.")
        print(traceback.format_exc())
        return False

def delete_procedure_category(procedureCategory: models.ProcedureCategory)->bool:
     print("[LOG] Deleting procedure category from the db")
     try:
        with db.cursor() as cursor:
            category_name_existence_check = fetch_procedure_category(procedureCategory.category_name)
            if category_name_existence_check is None:
               return False
            
            cursor.execute("DELETE FROM \"ProcedureCategory\" WHERE \"category_name\"=%s", (procedureCategory.category_name, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete procedure category from the database.")
        print(traceback.format_exc())
        return False

###################################

# Responsible party queries
def create_responsible_party(responsibleParty: models.ResponsibleParty)->bool:
    print("[LOG] Creating responsible party in the db.")
    try:
      with db.cursor() as cursor:
            responsible_for_existence_check = fetch_patient(responsibleParty.responsible_for)
            user_existence_check = fetch_user(user.ssn)
            responsible_party_existence_check = fetch_responsible_party(responsibleParty.user_ssn)
            if responsible_for_existence_check is not None or user_existence_check is not None or responsible_party_existence_check is not None:
                return False
            
            query = """INSERT INTO "ResponsibleParty" (user_ssn,reponsible_for) VALUES(,%s,%s);"""
            cursor.execute(query, responsibleParty.to_tuple())
            db.commit()

            return True
    except Exception:
        print("[ERROR] Failed to insert responsible party into the database.")
        print(traceback.format_exc())
        return False  

def fetch_responsible_party(user_ssn:int) -> models.ResponsibleParty:
    print("[LOG] Fetching responsible party from DB.")
    try:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ResponsibleParty\" WHERE \"user_ssn\"=%s", (user_ssn, ))
            db_response = cursor.fetchall()
            
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                return  # user does not exist
            
            return models.ResponsibleParty.from_postgres(db_response[0])
            
    except Exception:
        print("[ERROR] Failed to fetch responsible party.")
        print(traceback.format_exc())
        return False

def delete_responsible_party(responsibleParty: models.ResponsibleParty)->bool:
     print("[LOG] Deleting responsible party from the db")
     try:
        with db.cursor() as cursor:
            existence_check = fetch_responsible_party(responsibleParty.user_ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"ResponsibleParty\" WHERE \"user_ssn\"=%s", (responsibleParty.user_ssn, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete responsible party from the database.")
        print(traceback.format_exc())
        return False

###################################

# Review queries
def create_review(review: models.Review)->bool:
    print("[LOG] Creating Review in the db.")
    try:
      with db.cursor() as cursor:
            patient_existence_check = fetch_patient(review.user_ssn)
            if patient_existence_check is None:
                return False
            
            query = """INSERT INTO "Review" (employee_professionalism,communication,cleanliness,value,user_ssn) VALUES(%s,%s,%s,%s,%s);"""
            cursor.execute(query, review.to_tuple())
            db.commit()

            return True
    except Exception:
        print("[ERROR] Failed to insert Review into the database.")
        print(traceback.format_exc())
        return False  

def delete_review(review: models.Review)->bool:
     print("[LOG] Deleting Review from the db")
     try:
        with db.cursor() as cursor:
            existence_check = fetch_patient(review.user_ssn)
            if existence_check is None:
               return False
            cursor.execute("DELETE FROM \"Review\" WHERE \"user_ssn\"=%s", (review.user_ssn, ))
            db.commit()
            
            return True
     except Exception:
        print("[ERROR] Failed to delete Review from the database.")
        print(traceback.format_exc())
        return False

###################################

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
      last_name = "Dennis", 
      gender = 1, 
      email_address = "samantha.d@gmail.com",
      date_of_birth = 0, 
      phone_number = "6138977890", 
      age = 30, 
      password = "f6ea0f717a4641deddaf2060f0ea63ad9aca7fc580fcf5535b9443913ee4e9d6",
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
        id=37,
        opening_time="09:00:06",
        closing_time="18:00:00"
       
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
    admin1 = models.Admin(
        user_ssn=1234,
        works_at=0
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
    review1 = models.Review (
        employee_professionalism=5,
        communication=5,
        cleanliness=5,
        value=5,
        user_ssn=999999999
    )
    #create_user(user)
    #create_user(user2)
   # create_user(user3)
    #delete_user(1999)
    #create_admin(admin1)
    #create_employee(employee1)
   # create_branch_manager(branchManager)
    #create_patient(patient1)
    #delete_patient(patient1)
    #create_invoice(invoice1)
    #delete_employee(employee1)
    create_admin(admin1)
    #create_employee(employee1)
    #create_dentist(dentist1)
    #delete_user(user3)
    create_branch(branch)
    print(fetch_branch_id(0))
    create_review(review1)
    #create_appointment(appointment)
    #delete_appointment(appointment)
    #delete_branch(branch)
    #fetch_employee(1294)
    #fetch_dentist(1233)
    #create_procedure_category(procedure_category1)
    #create_appointment_procedure(appointmentProcedure)
    #update_user(user2,patient1)
   # print(fetch_appointment_procedures())
    #print(fetch_appointments())
   # print(fetch_branches())
   # print(fetch_users())