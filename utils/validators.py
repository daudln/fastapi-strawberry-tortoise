import re


def validate_email(email: str) -> bool:
    return re.match(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]{2,6}", email) is not None


def validate_password(password: str) -> bool:
    return (
        re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", password)
        is not None
    )
