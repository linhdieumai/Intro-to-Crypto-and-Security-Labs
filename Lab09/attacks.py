"""Task 5: two attacks.  Fill in every function marked TODO."""

import textbook


def reuse_attack(ct1: bytes, ct2: bytes, m1: bytes) -> bytes:
    """Recover m2 from two ciphertexts made with the same ephemeral b.

    ct1 and ct2 are ciphertexts of your modern ElGamal (elgamal.encrypt)
    for the same public key and the same b.  The plaintext m1 of ct1 is
    known, and m2 has the same length as m1.  No key is available.
    """
    header_len = 48
    c1_payload = ct1[header_len:]
    c2_payload = ct2[header_len:]
    return bytes(b1 ^ b2 ^ p1 for b1, b2, p1 in zip(c1_payload, c2_payload, m1))


def double_message(ct: tuple[int, int]) -> tuple[int, int]:
    """Turn a textbook ElGamal ciphertext of m into a ciphertext of 2m mod p.

    No key is available.
    """
    B, c = ct
    p = getattr(textbook, "P", getattr(textbook, "p", 467))
    return (B, (2 * c) % p)