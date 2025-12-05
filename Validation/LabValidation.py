# Validation/LabValidation.py
from Exceptions.Errors import ValidationError

def validate_result_value(value):
    if value is None or str(value).strip() == '':
        raise ValidationError("Test result value cannot be empty.")
    return True
