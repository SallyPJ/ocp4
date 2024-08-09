from datetime import datetime


def validate_date(date_str: str, format_str: str = '%d/%m/%Y') -> bool:
    """
    Valide si la chaîne de caractères correspond au format de date spécifié.

    Args:
        date_str (str): La chaîne de caractères représentant la date.
        format_str (str): Le format attendu pour la date (par défaut DD/MM/YYYY).

    Returns:
        bool: True si la date est valide, sinon False.
    """
    try:
        # Essaie de parser la chaîne de caractères en utilisant le format fourni
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False