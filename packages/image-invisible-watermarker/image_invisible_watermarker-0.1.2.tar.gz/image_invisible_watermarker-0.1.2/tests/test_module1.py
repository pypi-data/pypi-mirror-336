import pytest
from image_watermarker import module1

def test_text_to_binary():
    assert module1.text_to_binary("hello") == "0110100001100101011011000110110001101111"
def test_binary_to_text():
    assert module1.binary_to_text("0110100001100101011011000110110001101111") == "hello"
