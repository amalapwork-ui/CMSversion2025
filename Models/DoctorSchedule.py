# Models/DoctorSchedule.py
class DoctorSchedule:
    def __init__(self, schedule_id=None, doctor_id=None, start_time=None, end_time=None, slot_duration=None):
        self.schedule_id = schedule_id
        self.doctor_id = doctor_id
        self.start_time = start_time
        self.end_time = end_time
        self.slot_duration = slot_duration
