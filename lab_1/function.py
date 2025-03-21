import json

from constant import alphabet

def read_key(key_path)->dict[str:str]:
    """
    A function for reading the json encryption key.
    :param key_path:path to the file with the encryption key
    :return:dictionary from the key data
    """
    try:
        with open(key_path,"r",encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error: {e}")


def read_txt_file(file_path: str) -> str:
    """
    A function for reading a text file.
    :param file_path: path to the text file
    :return:text file as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")


def write_txt_file(data: str,file_path: str)->None:
    """
    A function for writing text to a file
    :param data: data to enter into the file
    :param file_path: the path to the file to save the data
    :return: None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(data))
    except Exception as e:
        print(f"Error: {e}")


def decryption(data: str, key: dict[str, str]) -> str:
    """
    A function for text decryption
    :param data: data for decryption
    :param key: decryption key
    :return: decrypted text
    """
    if data is None or key is None:
        return "There is no text or encryption key!"
    result = ""
    for lit in data:
        if lit in key:
            result += key[lit]
        else:
            result += lit
    return result


def caesar_cipher(data:str) -> str:
    """
    Encrypts the specified text using the Caesar cipher
    :param data: data for encryption
    :return: encrypted text
    """
    result = ""
    for char in data.lower():
        if char in alphabet:
            base = ord('а')
            encrypted_char = chr((ord(char) - base + 150) % 32 + base)
            result += encrypted_char
        else:
            result += char
    return result


def frequency(data: str) -> dict:
    """
    A function for calculating the frequency of occurrence of characters in the text
    :param data:encrypted data
    :return:frequency of occurrence of symbols
    """
    dic = dict()
    for i in set(data):
        dic[i] = data.count(i)
    for k in dic:
        dic[k] = dic[k] / len(data)
    sorted_dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
    return sorted_dic


def save_frequency(file_path: str, text: str) -> None:
    """
    A function to save the frequency of occurrence
    :param file_path:the path to the file to save the frequency
    :param text:text for frequency analysis
    :return:None
    """
    with open(file_path, 'w', encoding = "utf-8") as file:
        json.dump(frequency(text), file,ensure_ascii=False)
