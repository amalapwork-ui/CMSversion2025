# Validation/MedicineValidation.py
from Exceptions.Errors import ValidationError

def validate_quantity(qty):
    try:
        val = int(qty)
    except Exception:
        raise ValidationError("Quantity must be an integer.")
    if val <= 0:
        raise ValidationError("Quantity must be positive.")
    return val
