import socket
from datetime import datetime
import pytz  # Thư viện hỗ trợ múi giờ

# Khởi tạo server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Địa chỉ và cổng server
    server_socket.listen(1)
    print("Server đang chờ kết nối...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Kết nối từ {address}")

        # Nhận tên quốc gia từ Client
        country = client_socket.recv(1024).decode('utf-8')

        # Tìm thời gian hiện tại tại quốc gia
        try:
            timezone = pytz.timezone(country)
            current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        except pytz.UnknownTimeZoneError:
            current_time = "Quốc gia không tồn tại."

        # Gửi thời gian về Client
        client_socket.send(current_time.encode('utf-8'))
        client_socket.close()

# Chạy server
start_server()
