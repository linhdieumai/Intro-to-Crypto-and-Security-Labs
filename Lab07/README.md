# Lab 07 – RSA Decryption with the CRT (Group 05)

## Bảng phân công

| Thành viên | MSSV | Phụ trách |
|---|---|---|
| Đặng Thùy Minh | 202416808 | Task 3 |
| Mai Thị Diệu Linh | 202416807 | Task 1 + Task 4 |
| Nguyễn Minh Dũng | 202416682 | Task 2 |

Chạy: `python3 lab07_rsa_crt.py` (file `lab07_testdata.json` đặt cùng thư mục).

## Test results

### Small primes – toy-143 (p = 11, q = 13, e = 7, d = 103, y = 15)

| Quantity | Value |
|---|---|
| yp, yq | 4, 2 |
| dp, dq | 3, 7 |
| xp, xq | 9, 11 |
| cp, cq | 6, 6 |
| x | 141 |

All values match the worked example table.

### Large primes – given-190 (exercise ciphertext y = 12345678901234567890)

- x (standard) = 324309952877571399564352792629998816095895977177801581031
- x (CRT)      = 324309952877571399564352792629998816095895977177801581031
- check x^e mod n == y: True

### All keys in `lab07_testdata.json`

`crt_precompute` returns the `crt` field of every key, and both functions return the expected x:

- toy-143: 8/8 vectors OK
- given-190: 1/1 vectors OK
- rsa-1024: 10/10 vectors OK
- rsa-2048: 10/10 vectors OK
- rsa-4096: 10/10 vectors OK

## Timing table (Task 4)

Average time per decryption: 10 ciphertexts × 10 repetitions = 100 decryptions per method,
CRT with precomputed (dp, dq, cp, cq), measured with `time.perf_counter()`.

| Key size | Standard (ms) | CRT (ms) | Speed-up |
|---|---|---|---|
| 1024 | 2.508 | 0.749 | 3.35x |
| 2048 | 16.291 | 4.097 | 3.98x |
| 4096 | 111.135 | 25.851 | 4.30x |

### Comparison with the expected speed-up of 4

The CRT method is clearly faster for every key size, and the gain grows with the key size.
For 2048 and 4096 bits the measured speed-up (about 4.0x and 4.3x) is very close to the
theoretical value of 4, because each of the two exponentiations works with a modulus and an
exponent of half the size. For 1024 bits the speed-up is lower (about 3.35x): the numbers are
smaller, so the fixed costs of Steps 1 and 3 and of the Python function calls are a larger
share of the total. The measured values can be a little above or below 4 because Python's
big-integer arithmetic does not follow the schoolbook k³ cost exactly, and timings vary
slightly between runs and machines. The edge-case vectors (x = 0, x = 1) are cheap for both
methods and slightly lower the average times.
