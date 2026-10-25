"""IT4010E - Lab 05: Extended Euclidean Algorithm and Modular Inverse.

Student name:
Student ID:

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
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

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
    with open(path, encoding="ascii") as moduli_file:
        return [int(line) for line in moduli_file if line.strip()]


def find_shared_primes(moduli):
    """Return a dict {index: p} for every N[index] that shares a prime p with another N."""
    factors = batch_gcd(moduli)
    shared = {}

    for index, (modulus, factor) in enumerate(zip(moduli, factors)):
        if 1 < factor < modulus:
            shared[index] = factor
            continue

        if factor == modulus:
            for other_index, other_modulus in enumerate(moduli):
                if other_index == index:
                    continue
                common_factor = gcd(modulus, other_modulus)
                if 1 < common_factor < modulus:
                    shared[index] = common_factor
                    break

    return shared


# ---------------------------------------------------------------------------
# Bonus: batch GCD
# ---------------------------------------------------------------------------
def product_tree(moduli):
    """Return the list of levels: [moduli, products of pairs, ..., [P]]."""
    if not moduli:
        return []

    levels = [list(moduli)]
    while len(levels[-1]) > 1:
        current_level = levels[-1]
        next_level = [
            current_level[index] * current_level[index + 1]
            for index in range(0, len(current_level) - 1, 2)
        ]
        if len(current_level) % 2:
            next_level.append(current_level[-1])
        levels.append(next_level)
    return levels


def batch_gcd(moduli):
    """Return [g_1, ..., g_n] with g_i = gcd(N_i, product of all other N_j)."""
    if not moduli:
        return []
    if any(modulus <= 0 for modulus in moduli):
        raise ValueError("all moduli must be positive integers")

    total_product = product_tree(moduli)[-1][0]
    result = []
    for modulus in moduli:
        product_remainder = total_product % (modulus * modulus)
        other_product = product_remainder // modulus
        result.append(gcd(modulus, other_product))
    return result


if __name__ == "__main__":
    # Task 1: small tests
    print(extended_euclid(99, 78))     # expected (3, -11, 14)
    print(extended_euclid(899, 493))   # expected (29, -6, 11)

    # Task 1 and 2: timing table for large numbers
    rng = random.Random(2025)
    print("\nTiming (average microseconds per call)")
    print(f"{'bits':>6} {'gcd':>12} {'extended Euclid':>18} {'mod inverse':>14}")
    for bits in (256, 512, 1024, 2048):
        modulus = rng.getrandbits(bits) | 1
        value = rng.randrange(2, modulus)
        while gcd(value, modulus) != 1:
            value = rng.randrange(2, modulus)

        _, gcd_time = timed(gcd, value, modulus, reps=100)
        _, euclid_time = timed(extended_euclid, value, modulus, reps=100)
        inverse, inverse_time = timed(mod_inv, value, modulus, reps=100)
        assert gcd(value, modulus) == math.gcd(value, modulus)
        assert (value * inverse) % modulus == 1
        print(
            f"{bits:>6} {gcd_time * 1e6:>12.2f} "
            f"{euclid_time * 1e6:>18.2f} {inverse_time * 1e6:>14.2f}"
        )

    # Task 3: factor the numbers in moduli.txt that share a prime
    moduli_path = Path(__file__).with_name("moduli.txt")
    moduli = load_moduli(moduli_path)
    shared_primes = find_shared_primes(moduli)
    print(f"\nShared-prime moduli: {len(shared_primes)} of {len(moduli)}")
    for index, prime in sorted(shared_primes.items()):
        modulus = moduli[index]
        print(f"N[{index}] = {prime} * {modulus // prime}")

    # Bonus: check batch_gcd([21, 33, 65, 323]) == [3, 3, 1, 1], then run it on moduli.txt
    sample = [21, 33, 65, 323]
    expected = [3, 3, 1, 1]
    sample_gcds = batch_gcd(sample)
    assert sample_gcds == expected, (sample_gcds, expected)

    dataset_gcds = batch_gcd(moduli)
    print(f"\nBatch GCD completed for {len(dataset_gcds)} moduli.")
    print(f"Moduli with a non-trivial shared factor: {sum(value > 1 for value in dataset_gcds)}")
