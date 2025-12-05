# Utils/InputUtils.py
from datetime import datetime
from Exceptions.Errors import ValidationError

def input_str(prompt, required=True, max_len=None):
    while True:
        v = input(prompt).strip()
        if not v and required:
            print("This field is required.")
            continue
        if max_len and v and len(v) > max_len:
            print(f"Value is too long (max {max_len} chars).")
            continue
        return v or None

def input_int(prompt, required=True, min_value=None, max_value=None):
    while True:
        v = input(prompt).strip()
        if not v:
            if required:
                print("This field is required.")
                continue
            return None
        try:
            n = int(v)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if min_value is not None and n < min_value:
            print(f"Value must be >= {min_value}.")
            continue
        if max_value is not None and n > max_value:
            print(f"Value must be <= {max_value}.")
            continue
        return n

def input_date(prompt, required=True, date_fmt="%Y-%m-%d"):
    while True:
        v = input(prompt).strip()
        if not v:
            if required:
                print("This field is required.")
                continue
            return None
        try:
            d = datetime.strptime(v, date_fmt).date()
            return d.strftime(date_fmt)  # return string compatible with DB queries
        except ValueError:
            print(f"Please enter date in {date_fmt} format (e.g. 2025-12-05).")

def input_time(prompt, required=True, time_fmt="%H:%M:%S"):
    while True:
        v = input(prompt).strip()
        if not v:
            if required:
                print("This field is required.")
                continue
            return None
        try:
            t = datetime.strptime(v, time_fmt).time()
            return t.strftime(time_fmt)
        except ValueError:
            print(f"Please enter time in {time_fmt} format (e.g. 09:30:00).")

def confirm(prompt="Confirm (y/n): "):
    while True:
        v = input(prompt).strip().lower()
        if v in ('y','yes'):
            return True
        if v in ('n','no'):
            return False
        print("Please type 'y' or 'n'.")
