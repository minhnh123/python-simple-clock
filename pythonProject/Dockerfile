FROM ubuntu:latest
LABEL authors="Tran Nhat Minh"

ENTRYPOINT ["top", "-b"]
# Sử dụng image cơ bản là Python
FROM python:3.10-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Sao chép tất cả file từ thư mục hiện tại vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install -r requirements.txt

# Expose cổng 5000
EXPOSE 5000

# Lệnh để chạy ứng dụng
CMD ["python", "app.py"]
