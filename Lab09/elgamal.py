"""ElGamal public-key encryption, modern view.

Implement the slide "ElGamal system (a modern view)":

    G()            a <- Z_n,  h = g^a,  sk = a,  pk = h
    E(pk, m)       b <- Z_n,  u = g^b,  v = h^b,  k = H(u, v),
                   c = E_s(k, m),  return (u, c)
    D(sk, (u, c))  v = u^a,  k = H(u, v),  return D_s(k, c)

The group G is the prime-order subgroup of edwards25519 (see group.py).
libsodium provides the group, H = SHA-256 and the symmetric cipher
(E_s, D_s) = secretbox.

Fill in every function marked TODO.  Do not change the function signatures:
the tests in test_elgamal.py rely on them.
"""

import nacl.bindings as sodium
from nacl.exceptions import CryptoError

from group import ELEMENT_BYTES, exp, exp_g, is_valid_element, random_exponent

KEY_BYTES = sodium.crypto_secretbox_KEYBYTES      # 32
NONCE = bytes(sodium.crypto_secretbox_NONCEBYTES)  # 24 zero bytes
MAC_BYTES = sodium.crypto_secretbox_MACBYTES      # 16


def keygen() -> tuple[bytes, bytes]:
    """Return (pk, sk) with sk = a random and pk = h = g^a."""
    a = random_exponent()
    sk = a
    h = exp_g(a)
    if not is_valid_element(h) or len(h) != ELEMENT_BYTES or len(sk) != ELEMENT_BYTES:
        raise ValueError("Invalid key generation")
    return h, sk


def H(u: bytes, v: bytes) -> bytes:
    """Hash function H: G^2 -> K, namely SHA-256(u || v).

    Use sodium.crypto_hash_sha256.
    """
    if len(u) != ELEMENT_BYTES or len(v) != ELEMENT_BYTES or not is_valid_element(u) or not is_valid_element(v):
        raise ValueError("Invalid input to H")
    return sodium.crypto_hash_sha256(b"".join([u, v]))


def E_s(k: bytes, m: bytes) -> bytes:
    """Symmetric encryption of m under the one-time key k.

    Use sodium.crypto_secretbox_easy with the constant NONCE.
    """
    try:
        return sodium.crypto_secretbox_easy(m, NONCE, k)
    except CryptoError:
        raise ValueError("Encryption failed")   


def D_s(k: bytes, c: bytes) -> bytes:
    """Symmetric decryption of c under the key k.

    Use sodium.crypto_secretbox_open_easy with the constant NONCE.
    Raise ValueError if libsodium rejects c (it raises CryptoError).
    """
    try:
        return sodium.crypto_secretbox_open_easy(c, NONCE, k)
    except CryptoError:
        raise ValueError("Decryption failed")   

def encrypt(pk: bytes, m: bytes, b: bytes | None = None) -> bytes:
    """Return the ciphertext u || c  (32 bytes of u followed by c).


    If b is None, choose the ephemeral exponent b at random.  The parameter
    b exists only for the experiments and the known-answer tests: real code
    must never let the caller choose it.


    Raise ValueError if pk is not a valid group element.
    """
    if not is_valid_element(pk):
        raise ValueError("Invalid public key")
    if b is None:
        b = random_exponent()
    u = exp_g(b)
    v = exp(pk, b)
    k = H(u, v)
    c = E_s(k, m)
    return u + c

def decrypt(sk: bytes, ct: bytes) -> bytes:
    """Return the plaintext of ct = u || c.

    Raise ValueError if ct is too short, if u is not a valid group element,
    or if the symmetric decryption fails.
    """
    if len(ct) < ELEMENT_BYTES:
        raise ValueError("Ciphertext is too short")
    u = ct[:ELEMENT_BYTES]
    c = ct[ELEMENT_BYTES:]
    if not is_valid_element(u):
        raise ValueError("Invalid ciphertext")
    v = exp(sk, 1)  
    k = H(u, v)
    m = D_s(k, c)
    return m

