import re

from .encode import Variant

RFC4648 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
RFC4648_HEX = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
CROCKFORD = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def read_char(alphabet: str, char: str) -> int:
    idx = alphabet.find(char)
    if idx == -1:
        raise ValueError(f'Invalid character found: {char}')
    return idx


def decode(input_str: str, variant: Variant) -> bytes:
    if variant == 'RFC3548' or variant == 'RFC4648':
        alphabet = RFC4648
        input_str = re.sub(r'=+$', '', input_str)
    elif variant == 'RFC4648-HEX':
        alphabet = RFC4648_HEX
        input_str = re.sub(r'=+$', '', input_str)
    elif variant == 'Crockford':
        alphabet = CROCKFORD
        input_str = input_str.upper().replace('O', '0').replace('L', '1').replace('I', '1')
    else:
        raise ValueError(f'Unknown base32 variant: {variant}')

    length = len(input_str)
    bits = 0
    value = 0
    index = 0
    output = bytearray((length * 5 // 8))  # Allocate space for decoded bytes

    for char in input_str:
        value = (value << 5) | read_char(alphabet, char)
        bits += 5

        if bits >= 8:
            output[index] = (value >> (bits - 8)) & 0xFF
            index += 1
            bits -= 8

    return bytes(output)


