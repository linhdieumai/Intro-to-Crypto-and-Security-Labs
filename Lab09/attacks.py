"""Task 5: two attacks.  Fill in every function marked TODO."""

import textbook


def reuse_attack(ct1: bytes, ct2: bytes, m1: bytes) -> bytes:
    """Recover m2 from two ciphertexts made with the same ephemeral b.

    ct1 and ct2 are ciphertexts of your modern ElGamal (elgamal.encrypt)
    for the same public key and the same b.  The plaintext m1 of ct1 is
    known, and m2 has the same length as m1.  No key is available.
    """
    raise NotImplementedError("TODO (Task 5.1)")


def double_message(ct: tuple[int, int]) -> tuple[int, int]:
    """Turn a textbook ElGamal ciphertext of m into a ciphertext of 2m mod p.

    No key is available.
    """
    raise NotImplementedError("TODO (Task 5.2)")
