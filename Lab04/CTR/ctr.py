import sys, os
from Crypto.Cipher import AES

BLOCK = 16
MOD128 = 1 << 128


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def ctr_crypt(key, iv, data):
    aes = AES.new(key, AES.MODE_ECB)
    out = []
    ctr = int.from_bytes(iv, "big")        # IV là số nguyên 128-bit big-endian
    for i in range(0, len(data), BLOCK):
        # keystream block: Enc(IV + i mod 2^128)
        ks = aes.encrypt(((ctr + i // BLOCK) % MOD128).to_bytes(16, "big"))
        chunk = data[i:i + BLOCK]
        # khối cuối có thể ngắn: chỉ XOR đúng len(chunk) byte
        out.append(xor(chunk, ks[:len(chunk)]))
    return b"".join(out)


def ctr_encrypt(key, plaintext):
    iv = os.urandom(16)
    return iv + ctr_crypt(key, iv, plaintext)


def ctr_decrypt(key, ciphertext):
    if len(ciphertext) < 16:
        raise ValueError("Ciphertext too short (missing IV)")
    iv, body = ciphertext[:16], ciphertext[16:]
    return ctr_crypt(key, iv, body)


def run(infile, outfile):
    results = []
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            q, mode, key_hex, ct_hex = parts[0], parts[1], parts[2], parts[3]
            if mode != "CTR":
                continue
            try:
                pt = ctr_decrypt(bytes.fromhex(key_hex), bytes.fromhex(ct_hex))
                text = pt.decode("utf-8", errors="replace")
            except ValueError as e:
                text = f"ERROR: {e}"
            results.append((int(q), text))

    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)

    with open(outfile, "w", encoding="utf-8") as f:
        for q, text in results:
            f.write(f"Question {q}: {text}\n")
    return results


if __name__ == "__main__":
    infile = sys.argv[1] if len(sys.argv) > 1 else "lab04_questions.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "ctr_output.txt"
    for q, text in run(infile, outfile):
        print(f"Question {q}: {text}")
