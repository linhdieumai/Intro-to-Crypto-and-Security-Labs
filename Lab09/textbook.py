"""Textbook ElGamal over Z_p^* with the toy parameters of the lecture
(provided, do not modify).  Insecure: for Task 5 only.

    pk = A = g^a,   sk = a
    E(pk, m) = (B, c)  with  B = g^b,  k = A^b,  c = m * k   (all mod p)
    D(sk, (B, c)) = c * k^(-1)  with  k = B^a
"""

import secrets

P = 467
G = 2


def keygen() -> tuple[int, int]:
    a = secrets.randbelow(P - 3) + 2          # a in {2, ..., p-2}
    return pow(G, a, P), a


def encrypt(pk: int, m: int) -> tuple[int, int]:
    if not 1 <= m < P:
        raise ValueError("message must be in {1, ..., p-1}")
    b = secrets.randbelow(P - 3) + 2
    k = pow(pk, b, P)
    return pow(G, b, P), (m * k) % P


def decrypt(sk: int, ct: tuple[int, int]) -> int:
    B, c = ct
    k = pow(B, sk, P)
    return (c * pow(k, -1, P)) % P
