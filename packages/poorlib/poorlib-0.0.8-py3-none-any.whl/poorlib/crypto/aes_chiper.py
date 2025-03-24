from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

class AESCipher:
    def __init__(self, password: str, salt: bytes = None):
        self.backend = default_backend()
        self.password = password.encode()
        self.salt = salt if salt else os.urandom(16)  # Generate a random salt if not provided
        self.key = self._derive_key(self.password, self.salt)

    def _derive_key(self, password: bytes, salt: bytes, iterations: int = 100000) -> bytes:
        """Derive a secure key from the password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=self.backend
        )
        return kdf.derive(password)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt the plaintext using AES encryption in CBC mode."""
        iv = os.urandom(16)  # Generate a random initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Padding plaintext to be a multiple of block size (16 bytes for AES)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Encode the IV, salt, and ciphertext in a format suitable for transmission/storage (URL-safe base64)
        return base64.urlsafe_b64encode(iv + self.salt + ciphertext).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt the encrypted data using AES decryption in CBC mode."""
        # Decode from URL-safe base64
        encrypted_data = base64.urlsafe_b64decode(encrypted_data)

        # Extract the IV, salt, and ciphertext
        iv = encrypted_data[:16]
        salt = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        # Derive the key using the provided salt
        key = self._derive_key(self.password, salt)

        # Decrypt the data
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding from plaintext
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()