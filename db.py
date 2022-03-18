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

def authenticate_user(username:str, password:str) -> models.User:
    print("[LOG] Authenticating User with db.")
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM \"User\" WHERE email_address like %s AND password LIKE %s", (username, password))
            db_response = cursor.fetchall()
            
            print(db_response[0])
            # this would imply either the ssn does not exist in the postgres or the unique
            # key constaints in the database has broken causing duplicate columns
            if (not db_response) or (len(db_response) != 1):
                print("[ERROR] Invalid Authentication Request to Postgres")
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
            
            query = """INSERT INTO "User" ("SSN", address, house_number, street_name, street_number, city, province, first_name, middle_name, last_name, gender, email_address, date_of_birth, phone_number, age, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, user.to_tuple())
            db.commit()
            
            return True
            
    except Exception:
        print("[ERROR] Failed to insert new user into the database.")
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
        password = "b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3"
    )
    create_user(user)