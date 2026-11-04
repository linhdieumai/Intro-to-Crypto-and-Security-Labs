# Lab 04 – Modes of Operation (Group 05)

## Bảng phân công

| Thành viên | MSSV | Phụ trách |
|---|---|---|---|---|
| Đặng Thùy Minh | 202416808 | Task 3 |
| Mai Thị Diệu Linh | 202416807 | Task 1 + Task 4 |
| Nguyễn Minh Dũng | 202416682 | Task 2 |


## Test results
## xp = 9, xq = 11

cp = 6, cq = 6
x  = 141
x (standard) = 324309952877571399564352792629998816095895977177801581031
x (CRT)      = 324309952877571399564352792629998816095895977177801581031
check x^e mod n == y: True
toy-143: 8/8 vectors OK
given-190: 1/1 vectors OK
rsa-1024: 10/10 vectors OK
rsa-2048: 10/10 vectors OK
rsa-4096: 10/10 vectors OK
Key size | Standard (ms) | CRT (ms) | Speed-up |
    1024 |         0.028 |    0.031 |     0.88x |
    2048 |         0.054 |    0.060 |     0.91x |
    4096 |         0.106 |    0.192 |     0.55x |
    
## Timing tables

