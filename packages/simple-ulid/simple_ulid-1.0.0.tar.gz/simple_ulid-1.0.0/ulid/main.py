import secrets
from datetime import datetime, timezone

CROCKFORD_BASE32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def new():
    """
    Generate a ULID (Universally Unique Lexicographically Sortable Identifier).

    Steps:
        1. Get the current timestamp in milliseconds
        2. Convert the timestamp to a 50-bit binary string
        3. Generate 80 random bits for uniqueness
        4. Convert the 130-bit binary string into a 26-character ULID using Base32 encoding
    """
    current_timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    epoch_bits = '{0:050b}'.format(current_timestamp)
    random_bits = '{0:080b}'.format(secrets.randbits(80))
    bits = epoch_bits + random_bits
    return ''.join(CROCKFORD_BASE32[int(bits[i: i + 5], base=2)] for i in range(0, 130, 5))
