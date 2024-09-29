import re

import bcrypt


# Function to hash password
def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


# Function to check if password is hashed
def is_hash(password: str) -> bool:
    bcrypt_pattern = r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{22}[./A-Za-z0-9]{31}$"
    return bool(re.match(bcrypt_pattern, password))


if __name__ == "__main__":
    # Test the password hashing and verification functions
    password = "password"
    hashed_password = hash_password(password)
    print(f"Password: {password}")
    print(f"Hashed Password: {hashed_password}")
    print(f"Password Verification: {verify_password(password, hashed_password)}")
    print(
        f"Password Verification: {verify_password('wrong_password', hashed_password)}"
    )
