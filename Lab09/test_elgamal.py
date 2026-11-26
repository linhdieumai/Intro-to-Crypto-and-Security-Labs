"""Tests for Tasks 2-4.

Run all:          python -m pytest -v test_elgamal.py
Run one task:     python -m pytest -v test_elgamal.py -k task2
"""

import pytest

import elgamal
from group import exp_g, is_valid_element

# Known-answer test vectors (fixed sk and ephemeral b).
SK = bytes.fromhex("8869683b67f8367f63a2d30ebd081269c01c73871da7821fb4e9ccbbe12e650c")
PK = bytes.fromhex("80bbe45def40f65708e1e2441542e66be2d8cf81dcb7db9721c3194b7bca7a92")
B = bytes.fromhex("a177ce083be456e6248fed12a58c0e2dd51dc90e52654fb66a4f4c321aa05702")
M = b"IT4010E: ElGamal in practice"
CT = bytes.fromhex(
    "3e8080c39ac6f3a4dfa5d2a7af01f9d0d3e794529cc95017a1469b2a3133ef93"
    "f2daff45259ca8258ccf95115c10a11a54deebb529ea8676cb953a6812a32cff"
    "e89df0296481dc51b30db803"
)
U = CT[:32]
H_PK_U = bytes.fromhex("3eb7a0159fc7042269ce15d1774aa1bd5b6581b9a7290f5dcf1a9d3e8cf3dea9")

IDENTITY = bytes([1]) + bytes(31)                         # order 1
ORDER_2 = bytes([0xEC]) + bytes([0xFF]) * 30 + bytes([0x7F])  # order 2


# ---------------- Task 2: key generation ----------------

def test_task2_keygen_consistent():
    pk, sk = elgamal.keygen()
    assert len(pk) == 32 and len(sk) == 32
    assert exp_g(sk) == pk
    assert is_valid_element(pk)


def test_task2_keygen_random():
    assert elgamal.keygen()[1] != elgamal.keygen()[1]


# ---------------- Task 3: H, E_s, D_s, encrypt ----------------

def test_task3_hash_known_answer():
    assert elgamal.H(PK, U) == H_PK_U


def test_task3_symmetric_roundtrip():
    k = bytes(range(32))
    assert elgamal.D_s(k, elgamal.E_s(k, b"hello")) == b"hello"


def test_task3_symmetric_wrong_key():
    c = elgamal.E_s(bytes(32), b"hello")
    with pytest.raises(ValueError):
        elgamal.D_s(bytes([1]) * 32, c)


def test_task3_encrypt_known_answer():
    assert elgamal.encrypt(PK, M, b=B) == CT


def test_task3_ciphertext_length():
    assert len(elgamal.encrypt(PK, b"hello")) == 32 + 16 + 5


def test_task3_encrypt_randomised():
    assert elgamal.encrypt(PK, M) != elgamal.encrypt(PK, M)


@pytest.mark.parametrize("bad_pk", [IDENTITY, ORDER_2, bytes(31)],
                         ids=["identity", "order2", "short"])
def test_task3_encrypt_rejects_invalid_pk(bad_pk):
    with pytest.raises(ValueError):
        elgamal.encrypt(bad_pk, M)


# ---------------- Task 4: decrypt ----------------

def test_task4_decrypt_known_answer():
    assert elgamal.decrypt(SK, CT) == M


@pytest.mark.parametrize("m", [b"", b"x", b"hello world", bytes(1000)])
def test_task4_roundtrip(m):
    pk, sk = elgamal.keygen()
    assert elgamal.decrypt(sk, elgamal.encrypt(pk, m)) == m


def test_task4_wrong_key():
    _, other_sk = elgamal.keygen()
    with pytest.raises(ValueError):
        elgamal.decrypt(other_sk, CT)


@pytest.mark.parametrize("pos", [0, 31, 32, 47, 48, -1])
def test_task4_tampering(pos):
    bad = bytearray(CT)
    bad[pos] ^= 1
    with pytest.raises(ValueError):
        elgamal.decrypt(SK, bytes(bad))


def test_task4_short_ciphertext():
    with pytest.raises(ValueError):
        elgamal.decrypt(SK, CT[:40])


@pytest.mark.parametrize("u", [IDENTITY, ORDER_2], ids=["identity", "order2"])
def test_task4_small_order_u(u):
    with pytest.raises(ValueError):
        elgamal.decrypt(SK, u + CT[32:])
