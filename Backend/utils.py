# utils.py
# Utility functions for fitness app

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash a plain password using Werkzeug."""
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hashed version."""
    return check_password_hash(hashed, password)
