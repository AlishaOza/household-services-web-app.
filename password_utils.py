from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash
import re

# Define password policy
policy = PasswordPolicy.from_names(
    length=12,  # min length
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter chars
)


def validate_password(password, username=None):
    """Validate password against complexity rules"""
    errors = []

    if not password:
        errors.append("Password cannot be empty")
        return errors

    # Check against basic policy
    for requirement in policy.test(password):
        if "Length" in str(requirement):
            errors.append("Password must be at least 12 characters long")
        elif "Uppercase" in str(requirement):
            errors.append("Password must contain at least 1 uppercase letter (A-Z)")
        elif "Numbers" in str(requirement):
            errors.append("Password must contain at least 1 number (0-9)")
        elif "Special" in str(requirement):
            errors.append("Password must contain at least 1 special character (!@#$%^&*)")

    # Additional checks
    if username and username.lower() in password.lower():
        errors.append("Password cannot contain your username")

    if password.isnumeric():
        errors.append("Password cannot be entirely numeric")

    return errors


def hash_password(password):
    """Generate secure password hash"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)