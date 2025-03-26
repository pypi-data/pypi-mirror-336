# base32_tiny

Base32 encoding/decoding, RFC3548, RFC4648, RFC4648_HEX, Crockford


## Installation

using pip

```
$ pip install base32_tiny
```

using poetry

```
$ poetry add base32_tiny
```

## Usage

```
from base32_tiny import decode, encode

content = "hello, there!" 
#content_bytes = b"hello, there!"

result_rfc3548 = encode(content, variant="RFC3548")
print(result_rfc3548)  # output: NBSWY3DPFQQHI2DFOJSSC===
print(decode(result_rfc3548, variant="RFC3548").decode("utf-8") == content)  # output: True

result_rfc4648 = encode(content, variant="RFC4648")
print(result_rfc4648)  # output: NBSWY3DPFQQHI2DFOJSSC===
print(decode(result_rfc4648, variant="RFC4648"))  # output: b'hello, there!'


result_rfc4648_HEX = encode(content, variant="RFC4648-HEX")
print(result_rfc4648_HEX)  # output: D1IMOR3F5GG78Q35E9II2===
print(decode(result_rfc4648_HEX, variant="RFC4648-HEX"))  # output: b'hello, there!'


result_crockford = encode(content, variant="Crockford")
print(result_crockford)  # output: D1JPRV3F5GG78T35E9JJ2
print(decode(result_crockford, variant="Crockford"))  # output: b'hello, there!'
```

### API Reference
#### def encode(data: Union[str, bytes], *, variant: Variant, options: Optional[Options] = None) -> str
#### def decode(input_str: str, variant: Variant) -> bytes

```python
from typing import TypedDict, Literal
class Options(TypedDict, total=False):
    padding: bool
Variant = Literal["RFC3548", "RFC4648", "RFC4648-HEX", "Crockford"]
```