# Validation/AppointmentValidation.py
from Exceptions.Errors import ValidationError
from datetime import datetime

def validate_date_str(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except Exception:
        raise ValidationError("Invalid date. Use YYYY-MM-DD.")

def validate_time_str(time_str):
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        return True
    except Exception:
        raise ValidationError("Invalid time. Use HH:MM:SS.")
