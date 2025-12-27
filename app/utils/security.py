from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set")

cipher_suite=Fernet(ENCRYPTION_KEY.encode())


def get_password_hash(password:str)->str:
    """ hashing the password before injecting to database"""
    return pwd_context.hash(password)


def decrypt_data(data: str) -> str:
    """Decrypt sensitive data using Fernet symmetric decryption"""
    try:
        return cipher_suite.decrypt(data.encode()).decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data using Fernet symmetric encryption"""
    try:
        return cipher_suite.encrypt(data.encode()).decode()
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
    