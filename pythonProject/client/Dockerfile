# Sử dụng Python 3.10 (hoặc phiên bản tương thích)
FROM python:3.12

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép mã nguồn vào container
COPY client.py /app/client.py

# Cài đặt các thư viện cần thiết
RUN pip install pytz tk

# Lệnh chạy client (sử dụng giao diện GUI)
CMD ["python", "client.py"]
