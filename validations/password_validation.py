import re

def validate_password(password):
    if len(password) < 8:
        return False
    if " " in password:
        return False
    if not any(letter.isupper() for letter in password):
        return False
    if not re.search(r"[^\w\s]", password):
        return False
    if not any(letter.isdigit() for letter in password):
        return False
    return True
