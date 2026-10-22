import sys, os
from turtle import mode
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


if __name__ == '__main__':
    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, 'r') as f:
        key = bytes.fromhex(f.readline().strip())           
        ciphertext = bytes.fromhex("".join(f.read().split()))  
    decrypted = cbc_decrypt(key, ciphertext)
    with open(outfile, 'wb') as f:
        f.write(decrypted)
    print(f"CBC: wrote {outfile}")