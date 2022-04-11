from db import (
    fetch_user,
    fetch_dentist,
    fetch_admin,
    fetch_patient,
    fetch_branch_manager,
)
from models import PermissionLevel

def user_permission_level(ssn: int) -> PermissionLevel:
    # first ensure that the ssn exists within the database
    # as a root user type, otherwise checks for admin/dentist
    # will just waste system resources
    user = fetch_user(ssn)
    if user == None:
        return PermissionLevel.NONE
    
    # this will be used to verify whether a dentist, branch manager or admin
    # is also a patient ~ this is only needs to be done ONCE
    client = fetch_patient(ssn)

    #check to see if the user exists in the branch manager table
    # ~ if yes, the user is a branch manager
    manager=fetch_branch_manager(ssn)
    if manager!=None:
        permission_level=PermissionLevel.MANAGER
    
    # check to see if the user exists in the dentist table
    #    ~ if yes, the user is a dentist
    dentist = fetch_dentist(ssn)
    if dentist != None:
        permission_level = PermissionLevel.DENTIST
        
        # check to see if the user is both a dentist and patient
        if client != None:
            permission_level = PermissionLevel.DENTIST_PATIENT
    else:
        # a dentist cannot be an admin, so it is a condition that
        # the user cannot be a dentist to have admin permissions
        admin = fetch_admin(ssn)
        if admin != None:
            permission_level = PermissionLevel.ADMIN
            
            # check to see if the admin is a dentist and patient
            if client != None:
                permission_level = PermissionLevel.ADMIN_PATIENT
        else: 
            # if the user is not a dentist, not a branch manager, and not an admin, but
            # they exist within the system as a user, they MUST
            # be a patient ONLY
            permission_level = PermissionLevel.PATIENT
    
    return permission_level
