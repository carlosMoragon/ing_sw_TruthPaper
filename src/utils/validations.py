import re


def validate_date(date: str) -> bool:
    # yyyy-mm-dd
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date))


def validate_password(password: str) -> bool:
    # Busca que tenga al menos 4 números, 1 mayúscula, 1 carácter especial y 8 dígitos
    return bool(re.match(r'^(?=.*\d{4,})(?=.*[A-Z])(?=.*[\W_]).{8,}$', password))


def validate_email(email: str) -> bool:
    # Busca una expresión del tipo (string1)@(string2).(2+characters)
    return bool(re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))
