import re

def clean_value(value):

    if value is None:
        return ""

    value = str(value).strip()

    value = re.sub(r"\s+"," ",value)

    return value

