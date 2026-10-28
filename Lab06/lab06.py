#A1
def extended_euclid(a,b):
    """Return (d,x,y) such that d = gcd(a,b) = a*x + b*y."""
    if b == 0:
        return (a, 1, 0)
    else:
        d, x1, y1 = extended_euclid(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (d, x, y)
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
def poly_ext_euclid(a,b):
    if b == 0:
        return (a, 1, 0)
    q,r = poly_divmod(a,b)
    d, x1, y1 = poly_ext_euclid(b,r)
    return (d, y1, x1 ^ poly_mul(q, y1))

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


