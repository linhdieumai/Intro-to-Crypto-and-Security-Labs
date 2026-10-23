import sys, os
from Crypto.Cipher import AES


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def pad10(data):
    b = 16 - (len(data) % 16)       
    return data + b"\x80" + b"\x00" * (b - 1)


def unpad10(data):
    i = len(data) - 1
    while i >= 0 and data[i] == 0x00: #tìm byte cuối = duyệt các byte sau = 0
        i -= 1
    if i < 0 or data[i] != 0x80:
        raise ValueError("Invalid 10...0 padding")
    # padding hợp lệ: 0x80 + toàn 0x00 tổng độ dài đệm <= 16
    if len(data) - i > 16:
        raise ValueError("Invalid 10...0 padding (too long)")
    return data[:i]


def ecb_encrypt(key, plaintext):
    aes = AES.new(key, AES.MODE_ECB)
    data = pad10(plaintext)
    out = []
    for i in range(0, len(data), 16):
        out.append(aes.encrypt(data[i:i + 16]))
    return b"".join(out) 


def ecb_decrypt(key, ciphertext):
    if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
        raise ValueError("Invalid ciphertext length")
    aes = AES.new(key, AES.MODE_ECB)
    out = []
    for i in range(0, len(ciphertext), 16):
        out.append(aes.decrypt(ciphertext[i:i + 16]))
    return unpad10(b"".join(out))

def run(infile, outfile):
    results = []
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            q, mode, key_hex, ct_hex = parts[0], parts[1], parts[2], parts[3]
            if mode != "ECB":
                continue
            try:
                pt = ecb_decrypt(bytes.fromhex(key_hex), bytes.fromhex(ct_hex))
                text = pt.decode("utf-8", errors="replace")
            except ValueError as e:
                text = f"ERROR: {e}"
            results.append((int(q), text))
    with open(outfile, "w", encoding="utf-8") as f:
        for q, text in results:
            f.write(f"Question {q}: {text}\n")
    return results


if __name__ == "__main__":
    infile = sys.argv[1] if len(sys.argv) > 1 else "lab04_questions.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "ecb_output.txt"
    for q, text in run(infile, outfile):
        print(f"Question {q}: {text}")