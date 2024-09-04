import re


def validate_national_id(national_id: str) -> bool:
    """
    Validates the national ID to ensure it consists of 2 letters followed by 5 digits.

    Args:
        national_id (str): The national ID to validate.

    Returns:
        bool: True if the national ID is valid, False otherwise.
    """
    pattern = r'^[A-Za-z]{2}\d{5}$'

    if re.match(pattern, national_id):
        return True
    return False
