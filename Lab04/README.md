# Lab 04 – Modes of Operation (Group XX)

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
