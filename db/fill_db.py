import db.database_functions as db
import db.images as img
from peewee import IntegrityError


def fill_db():
    users = {
        "Dominik": "+421949186020",
        "Janik": "+421950764723",
        "Petrik": "+421903306221"
    }
    for username, phone_number in users.items():
        try:
            db.add_user(name=username, phone_number=phone_number, is_super_user=True)
        except IntegrityError as e:
            print(f"failed to create user: {username}", e)

    chats = {'Dominik': {'required_id': '+421949186020'},
             'Petrik': {'required_id': '+421903306221'},
             'Janik': {'required_id': '+421950764723'},
             'Vilo': {'required_id': '+421944373693'},
             'bot test group': {
                 'optional_id': 'group.VHBSZVBSdytDaDNZZkRsQ2N6bVluQnR3Yld1QUpDVkxyVXB2bDdGajNnYz0=',
                 'required_id': 'TpRePRw+Ch3YfDlCczmYnBtwbWuAJCVLrUpvl7Fj3gc='},
             'left4ded': {
                 'optional_id': 'group.dGMxREp4di80U3l2c0ZiQUIraitTTUordmljWk9QL3luc2N2OGZ2UW1Zbz0=',
                 'required_id': 'tc1DJxv/4SyvsFbAB+j+SMJ+vicZOP/ynscv8fvQmYo='},
             }

    for name, identifiers in chats.items():
        try:
            db.add_chat(name=name, **identifiers)
        except IntegrityError as e:
            print(f"failed to created group: {name}", e)


    commands = [
        {'name': 'vypicuj vila', 'command': 'VILO DRZ PICU', 'description': 'sends abusive content', 'attachment': None, 'is_functional': False},
        {'name': 'list commands', 'description': 'shows list of commands', 'attachment': None, 'is_functional': True},
        {'name': '!addcontact ', 'description': 'adds listeners', 'attachment': None, 'is_functional': True},
        {'name': 'todo', 'description': 'shows todo list', 'attachment': None, 'is_functional': True},
        {'name': '!todo ', 'description': 'adds todo item', 'attachment': None, 'is_functional': True},
        {'name': 'no so', 'command': "NO CO KOKOCI, DAVAJTE REACTY TAKOJ!!!!\n❤ - Yes\n👎 - No\n👍 - Yes, ked ostatni pojdu\n😥 - Mozem jebac\n😮 - Neskor sa napojim", 'description': 'launches gaming poll', 'attachment': None, 'is_functional': False},
        {'name': 'scare me', 'description': 'scares user', 'attachment': img.scare_me, 'is_functional': False},
        {'name': 'smh', 'description': 'smh gif', 'attachment': img.smh, 'is_functional': False},
    ]

    for command in commands:
        try:
            db.add_command(**command)
        except IntegrityError as e:
            print(f"failed to create command: {command['name']}", e)
