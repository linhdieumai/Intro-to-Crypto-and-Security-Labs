# Lab 04 – Modes of Operation (Group 05)

## Bảng phân công

| Thành viên | MSSV | Phụ trách | Câu hỏi | Thư mục |
|---|---|---|---|---|
| Đặng Thùy Minh | 202416808 | ECB + padding 10…0 | 1–3 | `ECB/` |
| Mai Thị Diệu Linh | 202416807 | CBC + padding PKCS5 | 4–7 | `CBC/` |
| Nguyễn Minh Dũng | 202416682 | OFB | 8–9 | `OFB/` |
| Nguyễn Minh Dũng | 202416682 | CFB | 10–11 | `CFB/` |
| Đặng Thùy Minh | 202416807 | CTR | 12–15 | `CTR/` |

## Yêu cầu

- Python 3.8+
- PyCryptodome, chỉ dùng để mã hóa/giải mã **một khối** AES (`AES.MODE_ECB`). Cả 5 mode đều tự cài đặt.

```
pip install pycryptodome
```
---

## ECB mode

### File

| File | Nội dung |
|---|---|
| `ECB/ecb.py` | `ecb_encrypt`, `ecb_decrypt`, padding `10...0` (thêm / kiểm tra / gỡ) |
| `ECB/ecb_input.txt` | Câu 1–3, mỗi dòng: `<câu> <key hex> <ciphertext hex>`; dòng bắt đầu bằng `#` là chú thích |
| `ECB/ecb_output.txt` | Plaintext giải ra (tạo khi chạy) |

### Lệnh chạy

```
cd ECB
python ecb.py ecb_input.txt ecb_output.txt
```

Nếu không truyền tham số, chương trình dùng mặc định `ecb_input.txt` và `ecb_output.txt`:
```
cd ECB
python ecb.py
```

Plaintext được in ra màn hình và ghi vào `ecb_output.txt`:

```
Question 1: Basic CBC mode encryption needs padding.
Question 2: Our implementation uses rand. IV
Question 3: This is a secret message.
```

### Ghi chú cài đặt

- ECB không dùng IV: ciphertext chính là `y₀ ‖ y₁ ‖ ...`, giải mã từng block bằng `Dec_k`.
- Padding `10...0`: thêm byte `0x80` rồi `b−1` byte `0x00` (với `b = 16 − len mod 16`); **luôn thêm**, kể cả khi plaintext đã bội 16 (khi đó thêm cả block `0x80 00...00`).
- Khi giải mã, kiểm tra padding: tìm byte `0x80` cuối cùng, mọi byte sau nó phải là `0x00`, và tổng số byte đệm ≤ 16. Padding sai hoặc độ dài ciphertext không phải bội 16 thì báo `ValueError` (in ra `ERROR: ...` cho câu đó).
- ECB mang tính tất định (`xᵢ = xⱼ ⇒ yᵢ = yⱼ`) — chỉ dùng cho mục đích học tập, không dùng trong thực tế. Ở Câu 1, `y₀ = y₂` cho thấy pattern trong plaintext bị lộ.

---

## CBC mode

### File

| File | Nội dung |
|---|---|
| `CBC/cbc.py` | `cbc_encrypt`, `cbc_decrypt`, padding PKCS5 (thêm / kiểm tra / gỡ) |
| `CBC/cbc_input.txt` | Câu 4–7, mỗi dòng: `<câu> <key hex> <ciphertext hex>`; dòng bắt đầu bằng `#` là chú thích |
| `CBC/cbc_output.txt` | Plaintext giải ra (tạo khi chạy) |

### Lệnh chạy

```
cd CBC
python cbc.py cbc_input.txt cbc_output.txt
```

Nếu không truyền tham số, chương trình dùng mặc định `cbc_input.txt` và `cbc_output.txt`:

```
cd CBC
python cbc.py
```

Plaintext được in ra màn hình và ghi vào `cbc_output.txt`:

```
Question 4: Basic CBC mode encryption needs padding.
Question 5: Our implementation uses rand. IV
Question 6: Never let a CBC IV be predictable to attackers.
Question 7: Hello, SoICT!
```

### Ghi chú cài đặt

- Padding sai hoặc độ dài ciphertext sai thì báo lỗi `ValueError` (in ra `ERROR: ...` cho câu đó).
