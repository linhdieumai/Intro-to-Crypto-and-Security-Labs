"""IT4010E - Lab 07: RSA Decryption with the CRT"""
import json
import time

DATA_FILE = "Lab07\\lab07_testdata.json"


def load_keys(path: str = DATA_FILE) -> dict:
    with open(path) as f:
        return {k["name"]: k for k in json.load(f)["keys"]}


# ---------- Task 1 ----------
def rsa_decrypt(y: int, d: int, n: int) -> int:
    """Standard RSA decryption: y^d mod n."""
    return pow(y,d,n)


# ---------- Task 2 ----------
def crt_precompute(d: int, p: int, q: int) -> tuple[int, int, int, int]:
    """Return (dp, dq, cp, cq)."""
    # TODO
    raise NotImplementedError


def rsa_decrypt_crt(y: int, d: int, p: int, q: int, pre=None) -> int:
    """RSA decryption using the CRT."""
    if pre is None:
        pre = crt_precompute(d, p, q)
    dp, dq, cp, cq = pre
    # Step 1: transformation to the CRT domain
    # Step 2: exponentiation in the CRT domain
    # Step 3: inverse transformation (recombination)
    # TODO
    raise NotImplementedError


# ---------- Task 3 ----------
def test_given(keys: dict) -> None:
    k = keys["given-190"]
    y = k["vectors"][0]["y"]
    x1 = rsa_decrypt(y, k["d"], k["n"])
    x2 = rsa_decrypt_crt(y, k["d"], k["p"], k["q"])
    print("x (standard) =", x1)
    print("x (CRT)      =", x2)
    print("check x^e mod n == y:", pow(x2, k["e"], k["n"]) == y)


def test_all(keys: dict) -> None:
    for name, k in keys.items():
        n, d, p, q = k["n"], k["d"], k["p"], k["q"]
        c = k["crt"]
        pre = crt_precompute(d, p, q)
        assert pre == (c["dp"], c["dq"], c["cp"], c["cq"]), name
        ok = 0
        for v in k["vectors"]:
            if (rsa_decrypt(v["y"], d, n) == v["x"]
                    and rsa_decrypt_crt(v["y"], d, p, q, pre) == v["x"]):
                ok += 1
            else:
                print(f"  FAIL {name}: {v['label']}")
        print(f"{name}: {ok}/{len(k['vectors'])} vectors OK")


# ---------- Task 4 ----------
def benchmark(keys: dict, repeat: int = 10) -> None:
    print(f"{'Key size':>8} | {'Standard (ms)':>13} | {'CRT (ms)':>8} | {'Speed-up':>8}")
    print("-" * 50)
    for name, k in keys.items():
        if name not in ["rsa-1024", "rsa-2048", "rsa-4096"]:
            continue
        n, d, p, q = k["n"], k["d"], k["p"], k["q"]
        y = k["vectors"][0]["y"]

        start = time.perf_counter()
        for _ in range(repeat):
            rsa_decrypt(y, d, n)
        t1 = (time.perf_counter() - start) / repeat

        pre = crt_precompute(d, p, q)
        start = time.perf_counter()
        for _ in range(repeat):
            rsa_decrypt_crt(y, d, p, q, pre)
        t2 = (time.perf_counter() - start) / repeat
        standard_ms = t1 * 1000
        crt_ms = t2 * 1000
        print(f"{name.removeprefix('rsa-'):>8} | {standard_ms:13.3f} | {crt_ms:8.3f} | {t1 / t2:8.2f}x")


if __name__ == "__main__":
    keys = load_keys()
    #test_given(keys)
    #test_all(keys)
    benchmark(keys)
