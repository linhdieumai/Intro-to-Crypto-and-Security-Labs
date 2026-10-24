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
- ECB mang tính tất định (`xᵢ = xⱼ ⇒ yᵢ = yⱼ`) - không được dùng trong thực tế. Ở Câu 1, `y₀ = y₂` cho thấy pattern trong plaintext bị lộ.

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

---

## OFB mode

### File

| File | Nội dung |
| :--- | :--- |
| `OFB/ofb.py` | Hàm `ofb_decrypt` |
| `OFB/ofb_output.txt`| Plaintext giải ra (tạo khi chạy) |

### Lệnh chạy

```bash
cd OFB
python ofb.py lab04_questions.txt ofb_output.txt
```

Nếu không truyền tham số, chương trình dùng mặc định `lab04_questions.txt` và `ofb_output.txt`:

```bash
cd OFB
python ofb.py
```

### Ghi chú cài đặt
- OFB sử dụng một IV ngẫu nhiên dài 16-byte. IV này được đặt ở ngay trước các block ciphertext.   
- Khi giải mã, hệ thống phải lấy IV từ phần đầu tiên của ciphertext.   
- Chế độ OFB không sử dụng padding. Block cuối cùng có thể ngắn hơn 16 byte.   
- Quá trình giải mã tái tạo lại cùng một keystream bằng cách tính $s_{i}=Enc_{k}(s_{i-1})$ với $s_{-1}=IV$. Bản rõ được tính ra thông qua công thức $x_{i}=y_{i}\oplus s_{i}$.   
- Block cuối cùng (nếu ngắn) chỉ được XOR với số lượng byte tương ứng lấy từ đầu ra của hàm $Enc()$. Do đó, độ dài của ciphertext sẽ dài hơn plaintext chính xác 16 byte.   

---

## CFB mode

### File

| File | Nội dung |
| :--- | :--- |
| `CFB/cfb.py` | Hàm `cfb_decrypt` |
| `CFB/cfb_output.txt`| Plaintext giải ra (tạo khi chạy) |

### Lệnh chạy

```bash
cd CFB
python cfb.py lab04_questions.txt cfb_output.txt
```

Nếu không truyền tham số, chương trình dùng mặc định `lab04_questions.txt` và `cfb_output.txt`:

```bash
cd CFB
python cfb.py
```

### Ghi chú cài đặt
- CFB sử dụng một IV ngẫu nhiên 16-byte. IV này được ghi dưới dạng rõ ở trước các block ciphertext.   
- Chế độ CFB không sử dụng padding. Block cuối cùng của plaintext có thể ngắn hơn 16 byte.   
- Quá trình mã hóa tính toán từng block bằng công thức $y_{i}=x_{i}\oplus Enc_{k}(y_{i-1})$ với $y_{-1}=IV$.   
- Việc tự thiết kế và tìm ra cách thức giải mã cho chế độ này là một phần yêu cầu của bài thực hành.   
- Block cuối cùng bị thiếu byte chỉ được XOR với đúng số lượng byte tương ứng của hàm $Enc()$. Ciphertext đầu ra có độ dài dài hơn plaintext chính xác 16 byte của IV.

---
## CTR mode

### File

| File | Nội dung |
|---|---|
| `CTR/ctr.py` | `ctr_encrypt`, `ctr_decrypt`, sinh keystream từ counter 128-bit (không dùng padding) |
| `CTR/ctr_input.txt` | Câu 12–15, mỗi dòng: `<câu> <key hex> <ciphertext hex>`; dòng bắt đầu bằng `#` là chú thích |
| `CTR/ctr_output.txt` | Plaintext giải ra (tạo khi chạy) |

### Lệnh chạy
```
cd CTR
python ctr.py ctr_input.txt ctr_output.txt
```

Nếu không truyền tham số, chương trình dùng mặc định `ctr_input.txt` và `ctr_output.txt`:
```
cd CTR
python ctr.py
```
Plaintext được in ra màn hình và ghi vào `ctr_output.txt`:
```
Question 12: CTR mode lets you build a stream cipher from a block cipher.
Question 13: Always avoid the two time pad!
Question 14: The Battle of Hastings, fought on 14 October 1066, is the event that famously began the Norman conquest of England.
Question 15: All that is gold does not glitter; not all those who wander are lost...
```

### Ghi chú cài đặt
- CTR không dùng padding: khối cuối có thể ngắn hơn 16 byte và chỉ XOR với đúng số byte keystream cần thiết. Ciphertext dài hơn plaintext đúng 16 byte (phần IV).
- IV (16 byte đầu ciphertext) được xem là số nguyên **128-bit big-endian**; keystream block thứ `i` là `Enc_k(IV + i mod 2¹²⁸)`. Counter **không được gửi đi**, chỉ IV được ghi công khai ở đầu ciphertext.
- Phải xử lý **counter 128-bit đầy đủ** và **mod 2¹²⁸** - Câu 14 (IV gần `0xFF...FF`) và Câu 15 (IV toàn `0xFF`, counter quay về 0 ngay block thứ 2) kiểm tra đúng điểm này.
- Encrypt và decrypt dùng chung một hàm `ctr_crypt` (CTR đối xứng: `yᵢ = xᵢ ⊕ ksᵢ` và `xᵢ = yᵢ ⊕ ksᵢ`). Ciphertext ngắn hơn 16 byte (thiếu IV) thì báo `ValueError` (in ra `ERROR: ...` cho câu đó).
---
