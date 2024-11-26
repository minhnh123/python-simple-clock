import socket
from datetime import datetime
import pytz
import threading


# Hàm xử lý từng kết nối client
def handle_client(client_socket, address):
    print(f"[{datetime.now()}] Kết nối từ {address}")

    try:
        # Nhận tên quốc gia từ Client
        country = client_socket.recv(1024).decode('utf-8')[:100]

        # Tìm thời gian hiện tại tại quốc gia
        try:
            timezone = pytz.timezone(country)
            current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        except pytz.UnknownTimeZoneError:
            current_time = "Error: Country not found."
        except Exception as e:
            current_time = f"Error: {str(e)}"

        # Gửi thời gian về Client
        client_socket.send(current_time.encode('utf-8'))
        print(f"[{datetime.now()}] Đã gửi thời gian: {current_time} tới {address}")
    except Exception as e:
        print(f"[{datetime.now()}] Lỗi xử lý client {address}: {e}")
    finally:
        client_socket.close()
        print(f"[{datetime.now()}] Kết nối từ {address} đã đóng.")


# Khởi tạo server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Địa chỉ và cổng server
    server_socket.listen(5)  # Cho phép tối đa 5 kết nối trong hàng đợi
    print("Server đang chờ kết nối...")

    while True:
        try:
            # Chấp nhận kết nối từ client
            client_socket, address = server_socket.accept()

            # Tạo luồng mới để xử lý kết nối client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

        except KeyboardInterrupt:
            print("Server dừng hoạt động.")
            server_socket.close()
            break


# Chạy server
if __name__ == "__main__":
    start_server()
