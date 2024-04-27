import re

def is_egyptian_phone_number(phone_number):
    pattern = r'^01[0125][0-9]{8}$'
    return bool(re.match(pattern, phone_number))