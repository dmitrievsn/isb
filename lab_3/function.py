from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def sm4_encrypt(key: bytes, text: bytes) -> bytes:
    """
    Encrypts text using the SM4 algorithm in CBC mode
    :param key:the encryption key is 16 bytes (128 bits) long
    :param text:text for encryption in the form of bytes
    :return:encrypted text
    """
    if len(key) != 16:
        raise ValueError("The key must be 16 bytes (128 bits)")
    iv = os.urandom(16)
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    pad_length = 16 - (len(text) % 16)
    padded_plaintext = text + bytes([pad_length] * pad_length)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext
