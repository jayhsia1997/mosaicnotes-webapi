"""
Password Provider for DI
"""
import bcrypt
import secrets
from typing import Tuple


class PasswordProvider:
    """Password Provider for hashing and verification"""
    
    @staticmethod
    def generate_salt() -> str:
        """
        Generate a random salt
        """
        return secrets.token_hex(32)
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
        """
        Hash password with salt
        :param password:
        :param salt:
        :return: (password_hash, salt)
        """
        if salt is None:
            salt = PasswordProvider.generate_salt()

        # Combine password and salt
        password_with_salt = password + salt

        # Hash the password
        password_bytes = password_with_salt.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        return password_hash.decode('utf-8'), salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """
        Verify password against hash and salt
        """
        try:
            # Combine password and salt
            password_with_salt = password + salt
            password_bytes = password_with_salt.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')

            # Verify password
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False