import math

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


def frequency_test(sequence:str) -> float:
    """
    Frequency bitwise test
    :param sequence:bitwise sequence
    :return:P-value
    """
    S=(sequence.count("1")-sequence.count("0"))/math.sqrt(len(sequence))
    return math.erf(S/math.sqrt(2))