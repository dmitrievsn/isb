import math

from scipy.special import gammainc


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
    S=abs(sequence.count("1")-sequence.count("0"))/math.sqrt(len(sequence))
    return math.erfc(S/math.sqrt(2))


def consecutive_bits_test(sequence:str) -> float:
    """
    A test for identical consecutive bits
    :param sequence:bitwise sequence
    :return:P-value
    """
    percentage_units = sequence.count("1")/len(sequence)
    if not(abs(percentage_units-1/2)<2/math.sqrt(len(sequence))):
        return 0
    V = sum(sequence[i] != sequence[i + 1] for i in range(len(sequence) - 1))
    return math.erfc(abs(V-2*len(sequence)*percentage_units*(1-percentage_units))/(2*math.sqrt(2*len(sequence))*percentage_units*(1-percentage_units)))


def block_statistic(sequence:str) -> tuple:
    """
    Calculates statistic of identical bits in each block of 8 bits in the sequence
    :param sequence: bitwise sequence
    :return: statistic
    """
    V1, V2, V3, V4 = 0, 0, 0, 0
    for i in range(0, len(sequence), 8):
        max_len = 0
        current_len = 0
        for bit in sequence[i:i + 8]:
            if bit == "1":
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0
        match max_len:
            case 1: V1 += 1
            case 2: V2 += 1
            case 3: V3 += 1
            case _: V4 += 1
    return V1, V2, V3, V4


def test_identical_consecutive_bits(statistic:tuple) -> float:
    """
    Test for the longest sequence of units in a block
    :param statistic: statistic
    :return: P-value
    """
    P = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_square = 0
    for i in range(0, 4):
        chi_square += ((statistic[i] - 16 * P[i]) ** 2) / (16 * P[i])
    return gammainc(3 / 2, chi_square / 2)


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