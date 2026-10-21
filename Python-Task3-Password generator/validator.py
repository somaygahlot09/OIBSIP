#This module contains functions for validating website URLs and email addresses.

import re

def validate_website(value):
    value = value.strip()

    # Website pattern
    website_pattern = (
        r"^(https?://|www\.)"
        r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
        r"(/.*)?$"
    )

    # Email pattern
    email_pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    if re.fullmatch(website_pattern, value):
        return True

    if re.fullmatch(email_pattern, value):
        return True

    return False