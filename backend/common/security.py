import hashlib
import hmac
import secrets

_ALGORITHM = "sha256"
_DEFAULT_ITERATIONS = 200_000
_SALT_BYTES = 16


def hash_password(plain_password: str, iterations: int = _DEFAULT_ITERATIONS) -> str:
    """Hash a plaintext password as 'iterations$salt_hex$hash_hex'.

    The iteration count travels with the hash so it can be raised later
    without invalidating passwords hashed under an older count.
    """
    salt = secrets.token_hex(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(_ALGORITHM, plain_password.encode("utf-8"), bytes.fromhex(salt), iterations)
    return f"{iterations}${salt}${digest.hex()}"


def verify_password(plain_password: str, stored_value: str) -> bool:
    """Verify a plaintext password against a stored 'iterations$salt$hash' value."""
    if not stored_value or stored_value.count("$") != 2:
        return False

    iterations_str, salt, expected_hex = stored_value.split("$")
    try:
        iterations = int(iterations_str)
    except ValueError:
        return False

    digest = hashlib.pbkdf2_hmac(_ALGORITHM, plain_password.encode("utf-8"), bytes.fromhex(salt), iterations)
    return hmac.compare_digest(digest.hex(), expected_hex)


def is_hashed(stored_value: str) -> bool:
    """True if a stored password value is already in 'iterations$salt$hash' form."""
    if not stored_value or stored_value.count("$") != 2:
        return False
    iterations_str, salt, digest_hex = stored_value.split("$")
    return iterations_str.isdigit() and len(salt) == _SALT_BYTES * 2 and len(digest_hex) == 64
