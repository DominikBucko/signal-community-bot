from .message import Message


def is_phone_number(phone_number: str) -> bool:
    if phone_number is None:
        return False
    return phone_number[0] == "+"


def is_group_id(group_id: str) -> bool:
    if group_id is None:
        return False
    prefix = "group."
    if group_id[: len(prefix)] != prefix:
        return False
    if group_id[-1] != "=":
        return False
    return True


def is_internal_id(internal_id: str) -> bool:
    if internal_id is None:
        return False
    return internal_id[-1] == "="


def should_react(user_chats: set, group_chats: dict, message: Message) -> bool:
    group = message.group
    if group in group_chats:
        return True

    source = message.source
    if source in user_chats:
        return True

    return False


def resolve_receiver(group_chats: dict, receiver: str) -> str:
    if is_phone_number(receiver):
        return receiver

    if receiver in group_chats:
        group_id = group_chats[receiver]
        return group_id

    raise SignalBotError(
        f"receiver {receiver} is not a phone number and not in self.group_chats. "
        "This should never happen."
    )


class SignalBotError(Exception):
    pass
