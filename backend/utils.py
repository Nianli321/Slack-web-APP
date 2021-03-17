from secrets import token_bytes
from sys import byteorder


def generate_luid(size=60):
    """
    Generates a Javascript friendly (< 64 bit) integer with enough size (>32 bit) to be locally unique
    """
    if 32 < size < 64:
        return int.from_bytes(token_bytes(size), byteorder)
    else:
        raise ValueError(
            "Must generate the UUID size between size 32 and 64 bits")
