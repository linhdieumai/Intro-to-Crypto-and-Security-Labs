"""IT4010E - Lab 05: Extended Euclidean Algorithm and Modular Inverse.

Student name:
Student ID:

Rules: implement gcd, extended_euclid and mod_inv yourself.
math.gcd and pow(a, -1, n) may only be used to CHECK your results.
"""
import math
import random
import time


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
    # TODO
    raise NotImplementedError


def extended_euclid(a, b):
    """Return (d, x, y) such that d = gcd(a, b) = a*x + b*y (iterative)."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 2
# ---------------------------------------------------------------------------
def mod_inv(a, n):
    """Return a^(-1) mod n; raise ValueError if gcd(a, n) != 1."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 3
# ---------------------------------------------------------------------------
def load_moduli(path="moduli.txt"):
    return [int(line) for line in open(path)]


def find_shared_primes(moduli):
    """Return a dict {index: p} for every N[index] that shares a prime p with another N."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Bonus: batch GCD
# ---------------------------------------------------------------------------
def product_tree(moduli):
    """Return the list of levels: [moduli, products of pairs, ..., [P]]."""
    # TODO
    raise NotImplementedError


def batch_gcd(moduli):
    """Return [g_1, ..., g_n] with g_i = gcd(N_i, product of all other N_j)."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # Task 1: small tests
    print(extended_euclid(99, 78))     # expected (3, -11, 14)
    print(extended_euclid(899, 493))   # expected (29, -6, 11)

    # Task 1 and 2: timing table for large numbers
    # TODO

    # Task 3: factor the numbers in moduli.txt that share a prime
    # TODO

    # Bonus: check batch_gcd([21, 33, 65, 323]) == [3, 3, 1, 1], then run it on moduli.txt
    # TODO
