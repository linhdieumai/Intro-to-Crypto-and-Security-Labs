"""The group G used in this lab (provided, do not modify).

G is the subgroup of prime order

    n = 2^252 + 27742317777372353535851937790883648493

of the elliptic curve edwards25519, as implemented by libsodium.  It is a
cyclic group of prime order n, exactly the "group G of order n with
generator g" of the slides.

libsodium writes the group additively (point addition, scalar
multiplication).  In this lab we keep the multiplicative notation of the
lecture:

    lecture         libsodium
    g^x             crypto_scalarmult_ed25519_base_noclamp(x)
    y^x             crypto_scalarmult_ed25519_noclamp(x, y)
    exponent x      a scalar modulo n, 32 bytes (little-endian)
    element y       a point, 32 bytes

Group elements and exponents are both `bytes` objects of length 32.
"""

import os

import nacl.bindings as sodium

ELEMENT_BYTES = sodium.crypto_core_ed25519_BYTES        # 32
EXPONENT_BYTES = sodium.crypto_core_ed25519_SCALARBYTES  # 32


def random_exponent() -> bytes:
    """Return a uniformly random non-zero exponent modulo n (32 bytes)."""
    while True:
        x = sodium.crypto_core_ed25519_scalar_reduce(os.urandom(64))
        if x != bytes(EXPONENT_BYTES):
            return x


def exp_g(x: bytes) -> bytes:
    """Return g^x.  Raises an exception if the result is the identity."""
    return sodium.crypto_scalarmult_ed25519_base_noclamp(x)


def exp(element: bytes, x: bytes) -> bytes:
    """Return element^x.  Raises an exception if the result is the identity."""
    return sodium.crypto_scalarmult_ed25519_noclamp(x, element)


def is_valid_element(element: bytes) -> bool:
    """Return True if `element` is an element of G of order n.

    Rejects wrong lengths, encodings that are not points of the curve,
    the identity and the other points of small order.
    """
    return (len(element) == ELEMENT_BYTES
            and sodium.crypto_core_ed25519_is_valid_point(element))
