from flask_login import UserMixin
from dataclasses import dataclass

import datetime

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
            self.password
        )
    
    @staticmethod
    def from_postgres(row: list):
        # check to ensure the number of cells in the list matches the columns
        # in the postgres User table
        if len(row) != 16:
            return None
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
            row[15]
        )