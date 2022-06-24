import os

config = {
    "signal_service": os.environ["SIGNAL_HOST"],
    "phone_number": os.environ["PHONE_NUMBER"],
    "object_storage_file": "object_storage/contacts_storage.pickle"
}

db_config = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "port": os.environ["DB_PORT"],
    "database": os.environ["DB_NAME"]
}
