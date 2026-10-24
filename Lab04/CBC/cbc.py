import sys, os
from Crypto.Cipher import AES

def xor(a,b):
    return bytes(x^y for x,y in zip(a,b))

def pkcs5_pad(data):
    b = 16 - (len(data) % 16)
    return data + bytes([b]) * b

def pkcs5_unpad(data):
    b = data[-1]
    if(b<1 or b>16 or data[-b:] != bytes([b]) * b):
        raise ValueError("Invalid PKCS5 padding")
    return data[:-b]

def cbc_encrypt(key,plaintext):
    aes = AES.new(key, AES.MODE_ECB)
    data = pkcs5_pad(plaintext)
    iv = os.urandom(16)
    prev,out = iv, [iv]
    for i in range(0,len(data),16):
        y = aes.encrypt(xor(data[i:i+16], prev))
        out.append(y)
        prev = y
    return b"".join(out)

def cbc_decrypt(key, ciphertext):
    if (len(ciphertext) < 32 or len(ciphertext) % 16 != 0):
        raise ValueError("Invalid ciphertext length")
    aes = AES.new(key, AES.MODE_ECB)
    prev = ciphertext[:16]
    out = []
    for i in range(16,len(ciphertext), 16):
        y = ciphertext[i:i+16]
        out.append(xor(aes.decrypt(y), prev))
        prev = y
    return pkcs5_unpad(b"".join(out))

def run(infile, outfile):
    results = []
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            q, mode, key_hex, ct_hex = line.split()   
            if mode.upper() != "CBC":                 
                continue
            try:
                pt = cbc_decrypt(bytes.fromhex(key_hex), bytes.fromhex(ct_hex))
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
    outfile = sys.argv[2] if len(sys.argv) > 2 else "cbc_output.txt"
    for q, text in run(infile, outfile):
        print(f"Question {q}: {text}")