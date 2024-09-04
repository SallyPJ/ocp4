from datetime import datetime


def validate_date(date_str: str, format_str: str = '%d/%m/%Y') -> bool:
    """
    Validates whether a given string matches the specified date format.

    Args:
        date_str (str): The string representing the date to validate.
        format_str (str): The expected date format (default is DD/MM/YYYY).

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        # Essaie de parser la chaîne de caractères en utilisant le format fourni
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False


def get_current_datetime():
    """
    Retrieves the current date and time formatted as DD/MM/YYYY HH:MM:SS.

    Returns:
        str: The current date and time as a string.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def parse_date(date_str):
    """
    Parses a string into a datetime object, expecting the format DD/MM/YYYY.

    Args:
        date_str (str): The string representing a date.

    Returns:
        datetime: A datetime object parsed from the provided string.
    """
    return datetime.strptime(date_str, "%d/%m/%Y")
