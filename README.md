# Website TakeNotes
<hr>
## Yêu cầu
- Máy phải được cài python 3.9 trở lên.
- Đã clone repo này về.

## Cách cài đặt virtualenv

👉🏿 **Cài đặt virtualenv bằng pip**
```Bash
pip install virtualenv
```
👉🏿 **tạo venv**
```Bash
python -m venv [name venv] 
```
hoặc
```Bash
virtualenv venv -p C:\Users\[username]\AppData\Local\Programs\Python\Python39\python.exe
```
Với cách này ta sẽ chỉ định phiên bản python hiện tại mà ta đang sử dụng với cờ **-p**

## Sử dụng
Sau khi cài đặt xong ta có thể tiến hành chạy app ở mode debug bằng cách gõ lệnh
```Bash
python .\wsgi.py
```
