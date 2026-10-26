"""IT4010E - Lab 05: Extended Euclidean Algorithm and Modular Inverse.

Student name: Đặng Thuỳ Minh, Mai Thị Diệu Linh, Nguyễn Minh Dũng
Student ID:   202416808, 202416807, 202416682

Rules: implement gcd, extended_euclid and mod_inv yourself.
math.gcd and pow(a, -1, n) may only be used to CHECK your results.
"""
import math
import random
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper: run f(*args) `reps` times, return (result, average time in seconds)
# ---------------------------------------------------------------------------
def timed(f, *args, reps=1):
    start = time.perf_counter()
    for _ in range(reps):
        result = f(*args)
    return result, (time.perf_counter() - start) / reps


# ---------------------------------------------------------------------------
# Task 1
# ---------------------------------------------------------------------------
def gcd(a, b):
    """Return gcd(a, b) using the Euclidean algorithm (iterative)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_euclid(a, b):
    """Return (d, x, y) such that d = gcd(a, b) = a*x + b*y (iterative)."""
    old_r, r = abs(a), abs(b)
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    # The loop works on |a|, |b|; fix the signs so that a*x + b*y = d.
    if a < 0:
        old_x = -old_x
    if b < 0:
        old_y = -old_y
    return old_r, old_x, old_y


# ---------------------------------------------------------------------------
# Task 2
# ---------------------------------------------------------------------------
def mod_inv(a, n):
    """Return a^(-1) mod n; raise ValueError if gcd(a, n) != 1."""
    if n <= 0:
        raise ValueError("modulus must be a positive integer")
    d, x, _ = extended_euclid(a, n)
    if d != 1:
        raise ValueError(f"{a} has no modular inverse modulo {n}")
    return x % n


# ---------------------------------------------------------------------------
# Task 3
# ---------------------------------------------------------------------------
def load_moduli(path="moduli.txt"):
    with open(path, encoding="ascii") as f:
        return [int(line) for line in f if line.strip()]


def pairwise_gcd(moduli, gcd_func=gcd):
    """Compute gcd(N_i, N_j) for all i < j.

    Return (number_of_gcds, shares) where shares[i] is a list of
    (j, g) with 1 < g = gcd(N_i, N_j).
    """
    n = len(moduli)
    count = 0
    shares = {}
    for i in range(n):
        for j in range(i + 1, n):
            g = gcd_func(moduli[i], moduli[j])
            count += 1
            if g != 1:
                shares.setdefault(i, []).append((j, g))
                shares.setdefault(j, []).append((i, g))
    return count, shares


def factor_from_shares(moduli, shares):
    """Return {i: (p, q, [indices sharing a prime])} with p * q = N_i."""
    result = {}
    for i, pairs in shares.items():
        N = moduli[i]
        p = next((g for _, g in pairs if 1 < g < N), None)
        if p is None:          # N_i equal to some N_j: cannot split it this way
            continue
        q = N // p
        assert p * q == N and 1 < p < N
        result[i] = (min(p, q), max(p, q), sorted(j for j, _ in pairs))
    return result


# ---------------------------------------------------------------------------
# Bonus: batch GCD
# ---------------------------------------------------------------------------
def product_tree(moduli):
    """Return the list of levels: [moduli, products of pairs, ..., [P]]."""
    if not moduli:
        return []
    levels = [list(moduli)]
    while len(levels[-1]) > 1:
        cur = levels[-1]
        nxt = [cur[k] * cur[k + 1] for k in range(0, len(cur) - 1, 2)]
        if len(cur) % 2:
            nxt.append(cur[-1])
        levels.append(nxt)
    return levels


def remainder_tree(levels):
    """Top-down: each node v gets (parent remainder) mod v^2.

    Return the leaves z_i = P mod N_i^2.
    """
    remainders = levels[-1][:]                      # root: P mod P^2 = P
    for level in reversed(levels[:-1]):
        remainders = [remainders[k // 2] % (v * v) for k, v in enumerate(level)]
    return remainders


def batch_gcd(moduli):
    """Return [g_1, ..., g_n] with g_i = gcd(N_i, product of all other N_j)."""
    if not moduli:
        return []
    levels = product_tree(moduli)
    leaves = remainder_tree(levels)
    return [gcd(z // N, N) for z, N in zip(leaves, moduli)]


def factor_with_batch(moduli):
    """Factor every N_i found by batch GCD.

    If g_i == N_i (both primes of N_i are shared), fall back to
    gcd(N_i, N_j) with the other moduli to split N_i (Question 4).
    """
    result = {}
    for i, (N, g) in enumerate(zip(moduli, batch_gcd(moduli))):
        if g == 1:
            continue
        if g == N:
            g = next((h for j, M in enumerate(moduli)
                      if j != i and 1 < (h := gcd(N, M)) < N), None)
            if g is None:
                continue
        p, q = sorted((g, N // g))
        assert p * q == N
        result[i] = (p, q)
    return result


def short(x, k=12):
    s = str(x)
    return s if len(s) <= 2 * k + 3 else f"{s[:k]}...{s[-k:]}"


if __name__ == "__main__":
    rng = random.Random(2025)

    # ---------------- Task 1 ----------------
    print("Task 1")
    print("extended_euclid(99, 78)   =", extended_euclid(99, 78))
    print("extended_euclid(899, 493) =", extended_euclid(899, 493))
    assert extended_euclid(99, 78) == (3, -11, 14)
    assert extended_euclid(899, 493) == (29, -6, 11)

    # ---------------- Task 1 + 2: timing table ----------------
    print("\nTiming (average of 20 repetitions, milliseconds)")
    print(f"{'bits':>6} {'extended_euclid':>16} {'mod_inv':>10} {'pow(a,-1,n)':>12}")
    for bits in (512, 1024, 2048, 4096, 8192):
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        a = rng.getrandbits(bits) | (1 << (bits - 1))
        while math.gcd(a, n) != 1:
            a = rng.getrandbits(bits) | (1 << (bits - 1))

        (d, x, y), t_ee = timed(extended_euclid, a, n, reps=20)
        assert a * x + n * y == d == math.gcd(a, n)
        inv, t_inv = timed(mod_inv, a, n, reps=20)
        inv_ref, t_pow = timed(pow, a, -1, n, reps=20)
        assert inv == inv_ref and a * inv % n == 1
        print(f"{bits:>6} {t_ee*1e3:>16.3f} {t_inv*1e3:>10.3f} {t_pow*1e3:>12.3f}")

    # ---------------- Task 2: Mersenne prime, mod_inv vs Fermat ----------------
    p = 2**2203 - 1
    a = rng.getrandbits(2000) | (1 << 1999)
    inv1, t1 = timed(mod_inv, a, p, reps=20)
    inv2, t2 = timed(pow, a, p - 2, p, reps=20)
    assert inv1 == inv2 and a * inv1 % p == 1
    print("\nTask 2: inverse of a random 2000-bit a modulo p = 2^2203 - 1 (20 reps)")
    print(f"  mod_inv(a, p)     : {t1*1e3:8.3f} ms")
    print(f"  pow(a, p - 2, p)  : {t2*1e3:8.3f} ms   (Fermat is {t2/t1:.1f}x slower)")

    # ---------------- Task 3: pairwise gcd ----------------
    moduli = load_moduli(Path(__file__).with_name("moduli.txt"))
    print(f"\nTask 3: {len(moduli)} moduli loaded")

    start = time.perf_counter()
    n_gcd, shares = pairwise_gcd(moduli, gcd)
    t_own = time.perf_counter() - start
    print(f"  own gcd  : {n_gcd} gcds in {t_own:.3f} s "
          f"({t_own / n_gcd * 1e6:.1f} us per gcd)")

    start = time.perf_counter()
    n_gcd2, shares2 = pairwise_gcd(moduli, math.gcd)
    t_math = time.perf_counter() - start
    print(f"  math.gcd : {n_gcd2} gcds in {t_math:.3f} s "
          f"({t_math / n_gcd2 * 1e6:.1f} us per gcd)")
    assert shares == shares2

    factored = factor_from_shares(moduli, shares)
    print(f"\n  Moduli that share a prime: {len(factored)}")
    for i, (pp, qq, others) in sorted(factored.items()):
        print(f"  N[{i}] shares a prime with {others}")
        print(f"      p = {pp}")
        print(f"      q = {qq}")

    # ---------------- Bonus: batch GCD ----------------
    sample = [21, 33, 65, 323]
    assert batch_gcd(sample) == [3, 3, 1, 1], batch_gcd(sample)
    print("\nBonus: batch_gcd([21, 33, 65, 323]) =", batch_gcd(sample))

    start = time.perf_counter()
    batch_factored = factor_with_batch(moduli)
    t_batch = time.perf_counter() - start
    assert set(batch_factored) == set(factored)
    assert all(batch_factored[i] == factored[i][:2] for i in factored)
    print(f"  batch GCD on moduli.txt: {len(batch_factored)} moduli factored in "
          f"{t_batch:.3f} s (same as Task 3)")
    print(f"  speed-up vs pairwise own gcd: {t_own / t_batch:.1f}x")