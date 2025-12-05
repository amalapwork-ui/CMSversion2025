# Validation/ConsultationValidation.py
from Exceptions.Errors import ValidationError

def validate_symptoms(symptoms):
    if not symptoms or symptoms.strip() == '':
        raise ValidationError("Symptoms cannot be empty.")
    if len(symptoms) > 1000:
        raise ValidationError("Symptoms text is too long.")
    return True

def validate_diagnosis(diagnosis):
    if not diagnosis or diagnosis.strip() == '':
        raise ValidationError("Diagnosis cannot be empty.")
    if len(diagnosis) > 1000:
        raise ValidationError("Diagnosis text is too long.")
    return True
