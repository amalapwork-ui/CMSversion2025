# Validation/StaffValidation.py
from Exceptions.Errors import ValidationError

def validate_username(username):
    if not username or username.strip() == '':
        raise ValidationError("Username is required.")
    if len(username) < 3:
        raise ValidationError("Username too short (min 3).")
    return True

def validate_password(password):
    if not password or password.strip() == '':
        raise ValidationError("Password required.")
    if len(password) < 4:
        raise ValidationError("Password too short (min 4).")
    return True
