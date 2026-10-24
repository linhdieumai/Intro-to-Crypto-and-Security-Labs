import sys
import os
from Crypto.Cipher import AES

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def decrypt_cfb(key_hex, ciphertext_hex):
    key = bytes.fromhex(key_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)
    iv = ciphertext[:16]
    y = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = bytearray()
    prev_y = iv
    for i in range(0, len(y), 16):
        y_i = y[i:i+16]
        s_i = cipher.encrypt(prev_y)
        x_i = xor_bytes(y_i, s_i[:len(y_i)])
        plaintext.extend(x_i)
        prev_y = y_i
        
    return plaintext.decode('utf-8', errors='ignore')

def run(infile, outfile):
    results = []
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            q, mode, key_hex, ct_hex = parts[0], parts[1], parts[2], parts[3]
            if mode != "CFB":
                continue      
            try:
                text = decrypt_cfb(key_hex, ct_hex)
            except ValueError as e:
                text = f"ERROR: {e}"
            results.append((int(q), text))
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        for q, text in results:
            f.write(f"Question {q}: {text}\n")
            
    return results

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_in = os.path.join(os.path.dirname(script_dir), "lab04_questions.txt")
    default_out = os.path.join(script_dir, "cfb_output.txt")
    infile = sys.argv[1] if len(sys.argv) > 1 else default_in
    outfile = sys.argv[2] if len(sys.argv) > 2 else default_out
    for q, text in run(infile, outfile):
        print(f"Question {q}: {text}")