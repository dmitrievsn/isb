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


def sm4_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypts cipher text using the SM4 algorithm in CBC mode
    :param key:the decryption key is 16 bytes (128 bits) long
    :param ciphertext:cipher text
    :return:decrypted text
    """
    if len(key) != 16:
        raise ValueError("The key must be 16 bytes (128 bits)")
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(actual_ciphertext) + decryptor.finalize()
    pad_length = padded_text[-1]
    text = padded_text[:-pad_length]
    return text


def read_txt_file(file_path: str) -> bytes:
    """
    A function for reading a text file as bytes.
    :param file_path: path to the text file
    :return: text file as bytes
    """
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")
        return b''


def write_txt_file(data: bytes, file_path: str) -> None:
    """
    A function for writing bytes to a file.
    :param data: data to enter into the file as bytes
    :param file_path: the path to the file to save the data
    :return: None
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error: {e}")