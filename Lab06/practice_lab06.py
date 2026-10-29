from lab06 import (extended_euclid, mod_inv,
                   poly_mul, poly_divmod, poly_mulmod, poly_ext_euclid,
                   poly_inv, inverse_table)

AES, GF512, R101 = 0x11B, 0x211, 0x101
GCM = (1 << 128) | 0x87

#P1
print("\nP1. Extended Euclid (A1):\n")
for a, b in [(240, 46), (1071, 462), (99, 78), (17, 3120)]:
    print(f"\n(a, b) = ({a}, {b})")
    d, x, y = extended_euclid(a, b, show_table=True)
    assert a * x + b * y == d          # Bezout check
    print(f"-> {a}*({x}) + {b}*({y}) = {d}")

#P4
print("\nP4. Extended Euclid for polynomials (B2):\n")
for a, b in [(0x95, AES), (0x1FF, GF512)]:
    print(f"\n(a, b) = (0x{a:X}, 0x{b:X})")
    d, x, y = poly_ext_euclid(a, b, show_table=True)
    assert poly_mul(a, x) ^ poly_mul(b, y) == d
