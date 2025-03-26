from enum import Enum

class SecretType(Enum):
    """Enumeration of supported secret types"""
    TEXT = "text"
    JSON = "json"


class SecretsStoreError(Exception):
    """Base exception class for SecretsStore errors"""
    pass


class SecretNotFoundError(SecretsStoreError):
    """Raised when a secret cannot be found"""
    pass


class SecretAccessError(SecretsStoreError):
    """Raised when access to a secret is denied"""
    pass


class SecretConversionError(SecretsStoreError):
    """Raised when a secret cannot be converted to the desired format"""
    pass