import base64
import re

from cryptography.fernet import Fernet

ENCRYPTION_REGEX = r'^enc{(.+)}$'


class Crypt:

    @classmethod
    def is_encrypted_value(cls, value) -> bool:
        return not not re.match(ENCRYPTION_REGEX, value)

    @classmethod
    def _extract_encrypted_value(cls, value) -> str:
        return re.match(ENCRYPTION_REGEX, value).group(1)

    @classmethod
    def generate_key(cls) -> str:
        key_bytes = Fernet.generate_key()
        return base64.encodebytes(key_bytes).decode('utf-8')

    @classmethod
    def decrypt_value(cls, value: str, key: str) -> str:
        if not key:
            return value
        key_bytes = base64.decodebytes(key.encode('utf-8'))
        value_bytes = base64.decodebytes(cls._extract_encrypted_value(value).encode('utf-8'))
        decrypted_bytes = Fernet(key=key_bytes).decrypt(value_bytes)
        return decrypted_bytes.decode('utf-8')

    @classmethod
    def encrypt_value(cls, value: str, key: str) -> str:
        key_bytes = base64.decodebytes(key.encode('utf-8'))
        encrypted_bytes = Fernet(key=key_bytes).encrypt(value.encode('utf-8'))
        return 'enc{' + base64.encodebytes(encrypted_bytes).decode('utf-8').strip().replace('\n', '') + '}'


if __name__ == '__main__':
    key = Crypt.generate_key()
    message = 'Hello World'
    encrypt_value = Crypt.encrypt_value(message, key)
    print(encrypt_value)
    print(Crypt.is_encrypted_value(encrypt_value))
    print(Crypt._extract_encrypted_value(encrypt_value))
    print(Crypt.decrypt_value(encrypt_value, key))
