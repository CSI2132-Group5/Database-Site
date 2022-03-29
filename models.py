from flask_login import UserMixin
from dataclasses import dataclass

from datetime import datetime

@dataclass
class User(UserMixin):
    ssn:int  # primary key
    address:str
    house_number:int
    street_name:str
    street_number:int
    city:str
    province:str
    first_name:str
    middle_name:str
    last_name:str
    gender:int
    email_address:str
    date_of_birth:int
    phone_number:str
    age:int
    password:str
    dateofbirth:datetime
    
    def get_id(self) -> int:
        return self.ssn
    
    def dob(self) -> datetime:
        return datetime.fromtimestamp(self.date_of_birth)
    
    def to_tuple(self):
        return (
            self.ssn,
            self.address,
            self.house_number,
            self.street_name,
            self.street_number,
            self.city,
            self.province,
            self.first_name,
            self.middle_name,
            self.last_name,
            self.gender,
            self.email_address,
            self.date_of_birth,
            self.phone_number,
            self.age,
            self.password,
            self.dateofbirth
        )
    
    @staticmethod
    def from_postgres(row: list):
        # there is an optional dateofbirth column, hence, we need to check if it has been passed to the
        # function from postgres and handle it accordingly
        #       ELSE -> pass a None value type to the class in place
        return User(
            int(row[0]),
            row[1],
            int(row[2]),
            row[3],
            int(row[4]),
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            int(row[10]),
            row[11],
            int(row[12]),
            row[13],
            int(row[14]),
            row[15],
            datetime.strftime(row[16], "%Y-%m-%d") if row[16] != None else None
        )
        
@dataclass
class Employee:
    user_ssn:int  # primary key
    role:str
    type:str
    salary:int
    shift_start:int
    shift_end:int
    
    def to_tuple(self):
        return (
            self.role,
            self.type,
            self.salary,
            self.shift_start,
            self.shift_end,
            self.user_ssn
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Admin(
            int(row[5]),    # user_ssn
            row[0],         # role
            row[1],         # type 
            int(row[2]),    # salary
            int(row[3]),    # shift_start      
            int(row[4])     # shift_end
        )

@dataclass
class Patient:
    user_ssn:int  # primary key
    insurance_company:str
    
    def to_tuple(self):
        return (
            self.user_ssn,
            self.insurance_company
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Admin(
            int(row[0]),    # user_ssn
            row[1]          # insurance_company
        )

@dataclass
class Admin:
    user_ssn:int  # primary key
    works_at:int
    
    def to_tuple(self):
        return (
            self.user_ssn,
            self.works_at
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Admin(
            int(row[0]),
            int(row[1])
        )
        
@dataclass
class Dentist:
    user_ssn:int  # primary key
    specialty:str
    works_at:int
    
    def to_tuple(self):
        return (
            self.specialty,
            self.user_ssn,
            self.works_at
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Admin(
            row[1],         # specialty
            int(row[0]),    # user ssn
            int(row[2])     # works at
        )
        
@dataclass
class BranchManager:
    user_ssn:int  # primary key
    manages:int
    
    def to_tuple(self):
        return (
            self.manages,
            self.user_ssn
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Admin(
            int(row[1]),
            int(row[0])
        )