# # Utils/SlotUtils.py
# from datetime import datetime, timedelta

# def generate_slots_for_schedule(start_time_str, end_time_str, slot_minutes):
#     """
#     Given start_time_str and end_time_str like "09:00:00" and slot_minutes integer,
#     return list of slot time strings "HH:MM:SS" from start inclusive up to (but not including) end.
#     """
#     fmt = "%H:%M:%S"
#     start = datetime.strptime(start_time_str, fmt)
#     end = datetime.strptime(end_time_str, fmt)

#     if start >= end:
#         return []

#     slots = []
#     cur = start
#     while cur + timedelta(minutes=0) < end:
#         slots.append(cur.strftime(fmt))
#         cur += timedelta(minutes=slot_minutes)
#     return slots

# def slot_is_on_boundary(slot_time_str, start_time_str, slot_minutes):
#     """
#     Returns True if slot_time_str is on boundary relative to start_time_str and slot_minutes.
#     """
#     fmt = "%H:%M:%S"
#     s = datetime.strptime(start_time_str, fmt)
#     t = datetime.strptime(slot_time_str, fmt)
#     diff_minutes = int((t - s).total_seconds() // 60)
#     return diff_minutes >= 0 and (diff_minutes % slot_minutes) == 0


# Utils/SlotUtils.py
from datetime import datetime, timedelta

def generate_slots_for_schedule(start_time_str, end_time_str, slot_minutes):
    fmt = "%H:%M:%S"
    # accept either strings or time objects; convert to string if needed
    if not isinstance(start_time_str, str):
        start_time_str = start_time_str.strftime(fmt)
    if not isinstance(end_time_str, str):
        end_time_str = end_time_str.strftime(fmt)
    start = datetime.strptime(start_time_str, fmt)
    end = datetime.strptime(end_time_str, fmt)
    if start >= end:
        return []
    slots = []
    cur = start
    while cur < end:
        slots.append(cur.strftime(fmt))
        cur += timedelta(minutes=slot_minutes)
    return slots

def slot_is_on_boundary(slot_time_str, start_time_str, slot_minutes):
    fmt = "%H:%M:%S"
    if not isinstance(start_time_str, str):
        start_time_str = start_time_str.strftime(fmt)
    s = datetime.strptime(start_time_str, fmt)
    t = datetime.strptime(slot_time_str, fmt)
    diff_minutes = int((t - s).total_seconds() // 60)
    return diff_minutes >= 0 and (diff_minutes % slot_minutes) == 0
