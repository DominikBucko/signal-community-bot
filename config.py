import os


config = {
    "signal_service": os.environ["SIGNAL_HOST"],
    "phone_number": os.environ["PHONE_NUMBER"],
    "object_storage_file": "object_storage/contacts_storage.pickle"
}
