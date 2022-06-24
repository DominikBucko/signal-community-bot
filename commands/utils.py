import db.database_functions as db


def is_super_admin(phone_number):
    return db.get_user(phone_number).is_super_user
