"""Bonus: break hybrid ElGamal over Z_p^* when p - 1 is smooth.

Run:  python bonus.py challenge.json

Attack (Pohlig-Hellman):
  1. Factor n = p - 1 (trial division, then Pollard rho with Miller-Rabin).
  2. For every prime power q^e dividing n, compute a mod q^e by working in the
     subgroup of order q^e: digit by digit, each digit is a discrete log in a
     group of order q (baby-step giant-step, or Pollard rho for large q).
  3. Combine the residues with the Chinese remainder theorem -> a mod (p - 1).
  4. Decrypt (u, c) as the receiver: v = u^a, k = SHA256(u || v), secretbox.

Only the Python standard library and PyNaCl are used.
"""

import json
import math
import random
import sys
from hashlib import sha256

import nacl.bindings as sodium

NONCE = bytes(sodium.crypto_secretbox_NONCEBYTES)
BSGS_LIMIT = 1 << 40          # use BSGS for q below this, Pollard rho above


# ---------------------------------------------------------------- factoring

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho_factor(n: int) -> int:
    """Return a non-trivial factor of the composite n (Brent's variant)."""
    if n % 2 == 0:
        return 2
    while True:
        y, c, m = random.randrange(1, n), random.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g


def factor(n: int) -> dict[int, int]:
    """Return the factorisation of n as {prime: exponent}."""
    result: dict[int, int] = {}

    def add(q, e=1):
        result[q] = result.get(q, 0) + e

    for q in range(2, 100000):
        if q * q > n:
            break
        while n % q == 0:
            add(q)
            n //= q
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if is_probable_prime(m):
            add(m)
        else:
            d = pollard_rho_factor(m)
            stack += [d, m // d]
    return result


# ------------------------------------------------- discrete log, prime order

def bsgs(g: int, h: int, q: int, p: int) -> int:
    """Return x in [0, q) with g^x = h mod p, where g has prime order q."""
    m = math.isqrt(q) + 1
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * g % p
    step = pow(g, -m, p)                       # g^(-m)
    y = h
    for i in range(m + 1):
        if y in table:
            return (i * m + table[y]) % q
        y = y * step % p
    raise ValueError("discrete log not found")


def rho_log(g: int, h: int, q: int, p: int) -> int:
    """Pollard rho for logarithms in the subgroup of prime order q."""
    def step(x, a, b):
        s = x % 3
        if s == 0:
            return x * x % p, 2 * a % q, 2 * b % q
        if s == 1:
            return x * g % p, (a + 1) % q, b
        return x * h % p, a, (b + 1) % q

    while True:
        a0, b0 = random.randrange(q), random.randrange(q)
        x = pow(g, a0, p) * pow(h, b0, p) % p
        X, A, B = x, a0, b0
        a, b = a0, b0
        while True:
            x, a, b = step(x, a, b)
            X, A, B = step(*step(X, A, B))
            if x == X:
                break
        # g^a h^b = g^A h^B  ->  (b - B) log h = A - a  (mod q)
        r = (b - B) % q
        if r != 0:
            return (A - a) * pow(r, -1, q) % q


def log_prime_order(g: int, h: int, q: int, p: int) -> int:
    if h == 1:
        return 0
    return bsgs(g, h, q, p) if q < BSGS_LIMIT else rho_log(g, h, q, p)


# ----------------------------------------------------------- Pohlig-Hellman

def log_prime_power(g: int, h: int, q: int, e: int, p: int, n: int) -> int:
    """Return a mod q^e, where h = g^a and g generates Z_p^* (order n)."""
    gamma = pow(g, n // q, p)                  # element of order q
    x = 0
    for k in range(e):
        # remove the digits already known, project onto the order-q subgroup
        hk = pow(pow(g, -x, p) * h % p, n // q ** (k + 1), p)
        d = log_prime_order(gamma, hk, q, p)
        x += d * q ** k
    return x


def crt(residues: list[tuple[int, int]]) -> int:
    x, m = 0, 1
    for r, mod in residues:
        t = (r - x) * pow(m, -1, mod) % mod
        x += m * t
        m *= mod
    return x % m


def pohlig_hellman(g: int, h: int, p: int) -> int:
    n = p - 1
    fac = factor(n)
    big = max(fac)
    print(f"p - 1 has {len(fac)} distinct prime factors, "
          f"largest has {big.bit_length()} bits", file=sys.stderr)
    residues = []
    for q, e in sorted(fac.items()):
        residues.append((log_prime_power(g, h, q, e, p, n), q ** e))
    return crt(residues)


# ---------------------------------------------------------------- decryption

def decrypt(p: int, a: int, u: int, c: bytes) -> bytes:
    L = (p.bit_length() + 7) // 8
    v = pow(u, a, p)
    k = sha256(u.to_bytes(L, "big") + v.to_bytes(L, "big")).digest()
    return sodium.crypto_secretbox_open_easy(c, NONCE, k)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python bonus.py challenge.json")
    with open(sys.argv[1]) as f:
        data = json.load(f)
    p, g, h, u = (int(data[key], 16) for key in ("p", "g", "h", "u"))
    c_hex = data["c"]
    c = bytes.fromhex(c_hex[2:] if c_hex.startswith("0x") else c_hex)

    a = pohlig_hellman(g, h, p)
    assert pow(g, a, p) == h, "wrong secret key"
    m = decrypt(p, a, u, c)
    print(hex(a))
    print(m.decode())


if __name__ == "__main__":
    main()
