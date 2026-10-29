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

#P2
print("\nP2. Modular inverse (A2):\n")
for a, n in [(7, 40), (17, 3120), (6, 9), (65537, 2**64), (2**64 + 13, 2**127 - 1)]:
    try:
        inv = mod_inv(a, n)
        assert a * inv % n == 1
        print(f"inverse of {a} mod {n} = {inv}")
    except ValueError:
        print(f"inverse of {a} mod {n} = none")

#P3
print("\nP3. Polynomial arithmetic (B1):\n")
print("poly_mul(0x1B, 0x35)         =", hex(poly_mul(0x1B, 0x35)))
print("poly_mul(0xFF, 0xFF)         =", hex(poly_mul(0xFF, 0xFF)))
print("poly_mulmod(0x02,0x87,AES)   =", hex(poly_mulmod(0x02, 0x87, AES)))
print("poly_mulmod(0xCA,0x53,AES)   =", hex(poly_mulmod(0xCA, 0x53, AES)))
print("poly_mulmod(0x1FF,0x100,511) =", hex(poly_mulmod(0x1FF, 0x100, GF512)))
q, r = poly_divmod(0x1234, 0x11B)
print("poly_divmod(0x1234, 0x11B)   = (q, r) =", hex(q), hex(r))
q, r = poly_divmod(0xFFFF, 0x211)
print("poly_divmod(0xFFFF, 0x211)   = (q, r) =", hex(q), hex(r))

#P4
print("\nP4. Extended Euclid for polynomials (B2):\n")
for a, b in [(0x95, AES), (0x1FF, GF512)]:
    print(f"\n(a, b) = (0x{a:X}, 0x{b:X})")
    d, x, y = poly_ext_euclid(a, b, show_table=True)
    assert poly_mul(a, x) ^ poly_mul(b, y) == d

#P5
print("\nP5. Polynomial inverse (B3):\n")
cases = [(AES, 0x02), (AES, 0x03), (AES, 0x95), (AES, 0xFF),
         (GF512, 0x0F0), (GF512, 0x123),
         (R101, 0x02), (R101, 0x05), (GCM, 0x02)]
for P, a in cases:
    Pname = "GCM" if P == GCM else f"0x{P:X}"
    try:
        inv = poly_inv(a, P)
        assert poly_mulmod(a, inv, P) == 1
        print(f"P={Pname:>6}  a=0x{a:<4X} -> 0x{inv:X}")
    except ValueError:
        d = poly_ext_euclid(a, P)[0]
        print(f"P={Pname:>6}  a=0x{a:<4X} -> none (gcd = 0x{d:X})")

#P6
print("\nP6. Inverse tables (B4):\n")
t9 = inverse_table(GF512)
for a in (0x0AB, 0x0FF, 0x155, 0x1A0):
    print(f"GF(2^9): 0x{a:03X}^-1 = 0x{t9[a]:03X}")
t8 = inverse_table(AES)
for a in (0x10, 0xC6):
    print(f"GF(2^8): 0x{a:02X}^-1 = 0x{t8[a]:02X}")

print("\nGF(2^9) grid (rows = high digit, cols = low hex digit):")
print("   " + " ".join(f"{c:>3x}" for c in range(16)))
for row in range(32):
    print(f"{row:2x}|" + " ".join(f"{t9[row*16+c]:03x}" for c in range(16)))