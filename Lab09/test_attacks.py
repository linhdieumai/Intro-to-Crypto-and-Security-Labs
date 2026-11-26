"""Tests for Task 5.  Run:  python -m pytest -v test_attacks.py"""

import attacks
import elgamal
from group import random_exponent
import textbook


def test_reuse_attack():
    pk, _ = elgamal.keygen()
    b = random_exponent()
    m1 = b"Transfer 100 USD to Bob.  Ref 01"
    m2 = b"The launch code is 4969-467-941."
    ct1 = elgamal.encrypt(pk, m1, b=b)
    ct2 = elgamal.encrypt(pk, m2, b=b)
    assert attacks.reuse_attack(ct1, ct2, m1) == m2


def test_double_message():
    for m in (1, 2, 33, 200, 248, 466):
        pk, sk = textbook.keygen()
        ct = textbook.encrypt(pk, m)
        forged = attacks.double_message(ct)
        assert forged != ct
        assert textbook.decrypt(sk, forged) == (2 * m) % textbook.P
