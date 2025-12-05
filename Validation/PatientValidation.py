# Validation/PatientValidation.py
from Exceptions.Errors import ValidationError
import re

def validate_mobile(mobile):
    if not mobile:
        raise ValidationError("Mobile number is required.")
    if not re.fullmatch(r"\d{7,15}", mobile):
        raise ValidationError("Mobile number must be digits only (7-15 digits).")
    return True

def validate_patient_name(name):
    if not name or name.strip() == '':
        raise ValidationError("Patient name is required.")
    if len(name) > 150:
        raise ValidationError("Patient name too long.")
    return True
