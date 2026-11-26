"""Task 6: compare your ElGamal with libsodium's sealed box (provided).

Run:  python benchmark.py      (takes a few seconds)
"""

import timeit

from nacl.public import PrivateKey, SealedBox

import elgamal
from group import exp, exp_g, is_valid_element, random_exponent

M = bytes(64)
N = 2000


def per_call_us(f) -> float:
    return timeit.timeit(f, number=N) / N * 1e6


def main():
    pk, sk = elgamal.keygen()
    ct = elgamal.encrypt(pk, M)
    x = random_exponent()

    box_sk = PrivateKey.generate()
    box_pk = box_sk.public_key
    box_ct = SealedBox(box_pk).encrypt(M)

    print(f"message length            {len(M)} bytes")
    print(f"your ciphertext           {len(ct)} bytes")
    print(f"sealed-box ciphertext     {len(box_ct)} bytes")
    print()
    print("time per call (microseconds)")
    print(f"  exp_g (g^x)             {per_call_us(lambda: exp_g(x)):8.1f}")
    print(f"  exp   (h^x)             {per_call_us(lambda: exp(pk, x)):8.1f}")
    print(f"  is_valid_element        {per_call_us(lambda: is_valid_element(pk)):8.1f}")
    print(f"  keygen                  {per_call_us(elgamal.keygen):8.1f}")
    print(f"  encrypt                 {per_call_us(lambda: elgamal.encrypt(pk, M)):8.1f}")
    print(f"  decrypt                 {per_call_us(lambda: elgamal.decrypt(sk, ct)):8.1f}")
    print(f"  sealed box encrypt      {per_call_us(lambda: SealedBox(box_pk).encrypt(M)):8.1f}")
    print(f"  sealed box decrypt      {per_call_us(lambda: SealedBox(box_sk).decrypt(box_ct)):8.1f}")


if __name__ == "__main__":
    main()
