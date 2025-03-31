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
    return math.erf(abs(V-2*len(sequence)*percentage_units*(1-percentage_units))/(2*math.sqrt(2*len(sequence))*percentage_units*(1-percentage_units)))

