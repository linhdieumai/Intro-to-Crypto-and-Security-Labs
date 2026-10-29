#A1
def extended_euclid(a, b, show_table=False):
    rows = []
    def calculate(a, b):
        if b == 0:
            d, x, y = a, 1, 0
            q = None
        else:
            q = a // b
            d, x1, y1 = calculate(b, a % b)
            x = y1
            y = x1 - q * y1
        rows.append((a, b, q, d, x, y))
        return d, x, y
    result = calculate(a, b)

    if show_table:
        print(f"{'a':>8} {'b':>8} {'⌊a/b⌋':>8} " f"{'d':>8} {'x':>8} {'y':>8}")
        for a, b, q, d, x, y in reversed(rows):
            quotient = '-' if q is None else str(q)
            print(f"{a:8} {b:8} {quotient:>8} " f"{d:8} {x:8} {y:8}")

    return result
#A2
def mod_inv(a,n):
    """Return b such that a*b = 1 mod n, or raise ValueError if no such b exists."""
    d, x, y = extended_euclid(a, n)
    if d != 1:
        raise ValueError(f"{a} has no inverse mod {n}")
    else:
        return x % n
#B1
def poly_mul(a,b):
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result

def poly_divmod(a,b):
    q = 0
    while a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        q ^= (1 << shift)
        a ^= (b << shift)
    return (q, a)

def poly_mulmod(a,b,mod):
    product = poly_mul(a, b)
    _, remainder = poly_divmod(product, mod)
    return remainder
#B2
def poly_ext_euclid(a, b, show_table=False):
    rows = []

    def calculate(a, b):
        if b == 0:
            d, x, y = a, 1, 0
            q = None
        else:
            q, r = poly_divmod(a, b)
            d, x1, y1 = calculate(b, r)
            x = y1
            y = x1 ^ poly_mul(q, y1)
        rows.append((a, b, q, d, x, y))
        return d, x, y
    result = calculate(a, b)

    if show_table:
        print(f"{'a':>8} {'b':>8} {'a div b':>10} "
              f"{'d':>8} {'x':>8} {'y':>8}")
        for a, b, q, d, x, y in reversed(rows):
            a_str = f"0x{a:X}"
            b_str = f"0x{b:X}"
            q_str = "-" if q is None else f"0x{q:X}"
            d_str = f"0x{d:X}"
            x_str = f"0x{x:X}"
            y_str = f"0x{y:X}"
            print(f"{a_str:>8} {b_str:>8} {q_str:>10} "
                  f"{d_str:>8} {x_str:>8} {y_str:>8}")

    return result

def poly_inv(a,P):
    d, x, y = poly_ext_euclid(a, P)
    if d != 1:
        raise ValueError(f"{a} has no inverse mod {P}")
    else:
        return poly_mulmod(x, 1, P)

def inverse_table(P):
    t = [0] * (1 << (P.bit_length()-1))
    for a in range(1,1<<(P.bit_length()-1)):
        t[a] = poly_inv(a, P)
    return t
