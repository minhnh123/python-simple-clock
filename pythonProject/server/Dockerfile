# File: Dockerfile.server
FROM python:3.12

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép mã nguồn vào container
COPY server.py /app/server.py

# Cài đặt các thư viện cần thiết
RUN pip install pytz

# Expose port 12345
EXPOSE 12345

# Lệnh chạy server
CMD ["python", "server.py"]
