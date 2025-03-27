from typing import Literal, TypedDict, Optional, Union

RFC4648 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
RFC4648_HEX = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
CROCKFORD = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'

Variant = Literal["RFC3548", "RFC4648", "RFC4648-HEX", "Crockford"]


class Options(TypedDict, total=False):
    padding: bool


def to_data_view(data) -> bytes:
    if isinstance(data, (bytes, bytearray)):
        return data
    elif isinstance(data, str):
        return data.encode('utf-8')
    else:
        raise TypeError("Unsupported data type")


def encode(data: Union[str, bytes], *, variant: Variant, options: Optional[Options] = None) -> str:
    if options is None:
        options = {}

    if variant == 'RFC3548' or variant == 'RFC4648':
        alphabet = RFC4648
        default_padding = True
    elif variant == 'RFC4648-HEX':
        alphabet = RFC4648_HEX
        default_padding = True
    elif variant == 'Crockford':
        alphabet = CROCKFORD
        default_padding = False
    else:
        raise ValueError('Unknown base32_tiny variant: ' + variant)

    padding = options.get('padding', default_padding)
    view = to_data_view(data)

    bits = 0
    value = 0
    output = ''

    for byte in view:
        value = (value << 8) | byte
        bits += 8

        while bits >= 5:
            output += alphabet[(value >> (bits - 5)) & 31]
            bits -= 5

    if bits > 0:
        output += alphabet[(value << (5 - bits)) & 31]

    if padding:
        while (len(output) % 8) != 0:
            output += '='

    return output

