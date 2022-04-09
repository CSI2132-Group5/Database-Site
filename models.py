from cgitb import text
from tokenize import String
from flask_login import UserMixin
from dataclasses import dataclass
from datetime import time

from enum import Enum

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
           # datetime.datetime.strptime(row[16], "%Y-%m-%d") if row[16] != None else None
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
        return Employee(
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
        return Patient(
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
        return Dentist(
            int(row[1]),         # specialty
            row[0],    # user ssn
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
        return BranchManager(
            int(row[1]),
            int(row[0])
        )

@dataclass
class Branch:
    name:String 
    address:String
    street_name:String
    street_number:int
    city: String # primary key
    province: String
    opening_time: datetime
    closing_time: datetime
    id: int
    def to_tuple(self):
       return (
           self.name,
           self.address,
           self.street_name,
           self.street_number,
           self.city,
           self.province,
           self.opening_time,
           self.closing_time,
           self.id
        )

    @staticmethod
    def from_postgres(row: list):
        return Branch(
            (row[0]),
            (row[1]),
            (row[2]),
            int(row[3]),
            (row[4]),
            (row[5]),
            time.strftime(row[6],'%H:%M:%S'),
            time.strftime(row[7],'%H:%M:%S'),
            int(row[8])
        ) 

@dataclass
class Appointment:
   id: int
   date:int
   start_time:int
   end_time:int
   status: int 
   assigned_room: int
   located_at: int
   appointment_patient: int
   appointment_dentist: int
   def to_tuple(self):
       return (
           self.id,
           self.date,
           self.start_time,
           self.end_time,
           self.status,
           self.assigned_room,
           self.located_at,
           self.appointment_patient,
           self.appointment_dentist
       )
    
   @staticmethod
   def from_postgres(row: list):
        return Appointment(
            int(row[0]),
            int(row[1]),
            int(row[2]),
            int(row[3]),
            int(row[4]),
            int(row[5]),
            int(row[6]),
            int(row[7]),
            int(row[8])
        ) 

@dataclass
class AppointmentProcedure: 
  procedure_code: int
  procedure_type: int
  tooth_number: int
  description: text
  appointment_id: int
  id: int
  procedure_category: text
  def to_tuple(self):
       return (
           self.procedure_code,
           self.procedure_type,
           self.tooth_number,
           self.description,
           self.appointment_id,
           self.id,
           self.procedure_category,
       )
  
  @staticmethod
  def from_postgres(row:list):
     return AppointmentProcedure( 
      int(row[0]),
      int(row[1]),
      int(row[2]),
      (row[3]),
      int(row[4]),
      int(row[5]),
      (row[6])
     )

@dataclass
class DentalAppliance:
  id: int
  type: text
  def to_tuple(self):
       return (
           self.id,
           self.type
       )
  
  @staticmethod
  def from_postgres(row:list):
     return DentalAppliance( 
      int(row[0]),
      (row[1])
     )

@dataclass
class ProcedureCategory:
    category_name: text
    description: text
    category_id: int
    def to_tuple(self):
       return (
           self.category_name,
           self.description,
           self.category_id
       )
    
    @staticmethod
    def from_postgres(row: list):
        return ProcedureCategory (
            (row[0]),
            (row[1]),
            int(row[2])
        )

@dataclass
class Invoice:
    issue_date:datetime
    total_charge: float
    discount:int
    penalty:int
    id:int
    receptionist_ssn:int
    def to_tuple(self):
       return (
       self.issue_date,
       self.total_charge,
       self.discount,
       self.penalty,
       self.id,
       self.receptionist_ssn
       )
    
    @staticmethod
    def from_postgres(row: list):
        return Invoice (
            datetime.strftime(row[0], "%Y-%m-%d") if row[0] != None else None,
            float(row[1]),
            int(row[2]),
            int(row[3]),
            int(row[4]),
            int(row[5])
        )

class ResponsibleParty:
    user_ssn: int
    responsible_for: int
    def to_tuple(self):
        return (
            self.user_ssn,
            self.responsible_for
        )
    
    @staticmethod
    def from_postgres(row: list):
        return ResponsibleParty (
            int(row[0]),
            int(row[1])
        )
@dataclass
class Review:
    employee_professionalism: int
    communication: int
    cleanliness: int
    value: int
    user_ssn: int
    def to_tuple(self):
        return (
            self.employee_professionalism,
            self.communication,
            self.cleanliness,
            self.value,
            self.user_ssn
        )
    
    @staticmethod
    def from_postgres(row: list):
        return Review (
            int(row[0]),
            int(row[1]),
            int(row[2]),
            int(row[3]),
            int(row[4])
        )

class PermissionLevel(Enum):
    DENTIST = 0
    DENTIST_PATIENT = 1
    ADMIN = 2
    ADMIN_PATIENT = 3
    PATIENT = 4,
    NONE = 5
