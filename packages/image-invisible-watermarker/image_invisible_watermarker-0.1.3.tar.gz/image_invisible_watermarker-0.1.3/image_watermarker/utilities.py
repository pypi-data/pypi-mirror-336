def text_to_binary(text):
    """
    Converts a given text string into a binary string representation.

    Each character in the text is converted to its ASCII code, which is then
    formatted as an 8-bit binary string. The resulting binary strings are
    concatenated to form the final binary string.

    Args:
        text (str): The text string to convert.

    Returns:
        str: A binary string representation of the input text.
    """
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    """
    Converts a binary string representation back into a text string.

    The binary string is split into 8-bit chunks, each of which is converted
    to its corresponding ASCII character. The characters are then joined to
    form the final text string.

    Args:
        binary (str): The binary string to convert.

    Returns:
        str: A text string converted from the binary string.
    """
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)
