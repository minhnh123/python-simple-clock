import socket
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import math
from pytz import all_timezones, timezone
import requests


# Global variables for clock
initial_time = None
received_time = None  # Global variable to avoid errors
time_delta = timedelta()
UPDATE_INTERVAL = 100  # Update every 100 ms for smooth animation

# Global variables for countdown timer
countdown_running = False
countdown_time_left = 0
countdown_paused = False

# Global reminders list
reminders = []

# Get weather data for a given city
def get_weather(city_name, api_key):
    # URL API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            # Trích xuất thông tin thời tiết
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather_info = f"{weather_description.capitalize()}\nTemp: {temperature}°C\nHumidity: {humidity}%"
            return weather_info
        else:
            return "Error: City not found"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# Get the initial time and weather information
def get_initial_time():
    global initial_time
    country = country_combobox.get()

    if not country:
        messagebox.showwarning("Warning", "Please select a country")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Send country name to the server
        client_socket.send(country.encode('utf-8'))

        # Receive time from the server
        received_time_str = client_socket.recv(1024).decode('utf-8')
        client_socket.close()

        if "Country not found" in received_time_str:
            messagebox.showerror("Error", received_time_str)
            return

        # Convert the received time string to datetime object
        received_time = datetime.strptime(received_time_str, '%Y-%m-%d %H:%M:%S')

        # Convert the time to the selected country's timezone
        country_tz = timezone(country)
        initial_time = received_time.astimezone(country_tz)

        # Get weather information
        city_name = country.split('/')[-1]  # Extract city name from timezone (e.g., 'Europe/London' -> 'London')
        api_key = ""  # Replace with your API key
        weather_info = get_weather(city_name, api_key)

        # Check if weather info was successfully retrieved
        if "Error" in weather_info:
            weather_label.config(text="Weather Info: " + weather_info)
        else:
            weather_label.config(text=weather_info)  # Display weather info without adding "Weather:"

        # Update the digital time label with only the time
        digital_time_label.config(text=initial_time.strftime('%Y-%m-%d, %H:%M:%S'))

        update_clock()

    except ConnectionError:
        messagebox.showerror("Error", "Cannot connect to server")




# Function to update the clock hands smoothly
def update_clock():
    global initial_time
    if initial_time is not None:
        # Get the actual current time based on the timezone
        current_time = datetime.now().astimezone(initial_time.tzinfo)
        fractional_second = current_time.second + current_time.microsecond / 1_000_000
        fractional_minute = current_time.minute + fractional_second / 60
        fractional_hour = (current_time.hour % 12) + fractional_minute / 60

        # Calculate smooth angles for each hand
        hour_angle = fractional_hour * 30  # each hour is 30 degrees
        minute_angle = fractional_minute * 6  # each minute is 6 degrees
        second_angle = fractional_second * 6  # each second is 6 degrees

        # Clear old hands
        canvas.delete("hands")

        # Draw hour, minute, and second hands
        draw_hand(hour_angle, 50, "blue")  # Hour hand
        draw_hand(minute_angle, 70, "green")  # Minute hand
        draw_hand(second_angle, 90, "red")  # Second hand

        # Display digital time
        digital_time_label.config(text=current_time.strftime('%Y-%m-%d, %H:%M:%S'))

        # Call update_clock again after a very short interval for smooth animation
        canvas.after(33, update_clock)  # Update every 33ms (~30fps)

# Function to draw clock hands
def draw_hand(angle, length, color):
    # Calculate the endpoint of the hand
    angle_rad = math.radians(angle - 90)
    x = 100 + length * math.cos(angle_rad)
    y = 100 + length * math.sin(angle_rad)
    canvas.create_line(100, 100, x, y, width=2, fill=color, tags="hands")

# Draw clock face
def draw_clock_face():
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        outer_x = 100 + 90 * math.cos(angle)
        outer_y = 100 + 90 * math.sin(angle)
        inner_x = 100 + (80 if i % 5 == 0 else 85) * math.cos(angle)
        inner_y = 100 + (80 if i % 5 == 0 else 85) * math.sin(angle)
        width = 2 if i % 5 == 0 else 1
        canvas.create_line(outer_x, outer_y, inner_x, inner_y, width=width, fill="black")

    for i in range(12):
        angle = math.radians(i * 30 - 60)
        x = 100 + 75 * math.cos(angle)
        y = 100 + 75 * math.sin(angle)
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 10))

# Countdown timer functions
def start_countdown():
    global countdown_running, countdown_time_left, countdown_paused

    if countdown_running and not countdown_paused:
        messagebox.showwarning("Warning", "Countdown is already running!")
        return

    if countdown_paused:
        countdown_paused = False
        countdown_running = True
        update_countdown()
        return

    try:
        minutes = int(countdown_minutes_entry.get())
        seconds = int(countdown_seconds_entry.get())
        countdown_time_left = minutes * 60 + seconds
        if countdown_time_left <= 0:
            raise ValueError
        countdown_running = True
        update_countdown()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid positive numbers for minutes and seconds.")

def update_countdown():
    global countdown_running, countdown_time_left, countdown_paused

    if countdown_running and not countdown_paused:
        if countdown_time_left > 0:
            minutes, seconds = divmod(countdown_time_left, 60)
            countdown_label.config(text=f"{minutes:02}:{seconds:02}")
            countdown_time_left -= 1
            root.after(1000, update_countdown)
        else:
            countdown_running = False
            countdown_label.config(text="Time's up!")
            messagebox.showinfo("Countdown", "Time's up!")

def stop_countdown():
    global countdown_running, countdown_paused
    countdown_paused = True
    countdown_running = False

def reset_countdown():
    global countdown_running, countdown_paused, countdown_time_left
    countdown_running = False
    countdown_paused = False
    countdown_time_left = 0
    countdown_label.config(text="00:00")

# Hàm đặt nhắc nhở
def set_reminder():
    global reminders

    selected_date = cal.get_date()
    reminder_time = reminder_time_entry.get().strip()
    reminder_text = reminder_text_entry.get().strip()

    if not is_valid_time_format(reminder_time):
        messagebox.showerror("Error", "Invalid time format! Use HH:MM (24-hour format).")
        return

    country = country_combobox.get()
    if country not in all_timezones:
        messagebox.showerror("Error", "Please select a valid timezone.")
        return

    try:
        reminder_datetime_str = f"{selected_date} {reminder_time}"
        reminder_datetime = datetime.strptime(reminder_datetime_str, "%m/%d/%y %H:%M")
        reminder_datetime = timezone(country).localize(reminder_datetime)

        if not reminder_text:
            messagebox.showerror("Error", "Reminder text cannot be empty.")
            return

        reminders.append((reminder_datetime, reminder_text))
        messagebox.showinfo("Success", f"Reminder set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')} ({country})")
    except ValueError:
        messagebox.showerror("Error", "Invalid date or time.")


def is_valid_time_format(time_string):
    try:
        # Kiểm tra xem có đúng định dạng HH:MM hay không
        datetime.strptime(time_string, "%H:%M")
        return True
    except ValueError:
        return False

def check_reminders():
    global reminders, initial_time

    # Nếu chưa có thời gian ban đầu, chờ 1 giây rồi kiểm tra lại
    if not initial_time:
        root.after(1000, check_reminders)
        return

    country = country_combobox.get()
    if country not in all_timezones:
        root.after(1000, check_reminders)
        return

    try:
        # Lấy thời gian hiện tại theo múi giờ
        current_time = datetime.now().astimezone(timezone(country))
    except Exception as e:
        print(f"[DEBUG] Timezone error: {e}")
        root.after(1000, check_reminders)
        return

    # Kiểm tra nhắc nhở
    for reminder in reminders[:]:
        reminder_time, reminder_text = reminder
        if current_time >= reminder_time:
            messagebox.showinfo("Reminder", f"Reminder: {reminder_text}")
            reminders.remove(reminder)

    root.after(1000, check_reminders)


# Calendar mode
def show_calendar():
    global cal, reminder_time_entry, reminder_text_entry

    calendar_window = tk.Toplevel(root)
    calendar_window.title("Calendar Mode")

    cal = Calendar(calendar_window, selectmode='day')  # Tạo calendar trong cửa sổ con
    cal.pack(pady=10)

    ttk.Label(calendar_window, text="Reminder Time (HH:MM):").pack(pady=5)
    reminder_time_entry = ttk.Entry(calendar_window, width=10)
    reminder_time_entry.pack()

    ttk.Label(calendar_window, text="Reminder Text:").pack(pady=5)
    reminder_text_entry = ttk.Entry(calendar_window, width=30)
    reminder_text_entry.pack()

    ttk.Button(calendar_window, text="Set Reminder", command=set_reminder).pack(pady=10)

# Tìm kiếm múi giờ và cập nhật danh sách trong combobox
def search_timezone(*args):
    search_term = search_entry.get().strip().lower()
    if not search_term:
        filtered_timezones = all_timezones
    else:
        filtered_timezones = [tz for tz in all_timezones if search_term in tz.lower()]

    country_combobox['values'] = filtered_timezones
    if filtered_timezones:
        country_combobox.set(filtered_timezones[0])
    else:
        messagebox.showinfo("Info", "No timezones match your search.")


# GUI setup
root = tk.Tk()
root.title("World Clock & Countdown Timer")

# Time zone section
frame_top = ttk.Frame(root, padding="10")
frame_top.pack(fill="x")

ttk.Label(frame_top, text="Select a country:", font=("Arial", 12)).pack(side="left", padx=5)
country_combobox = ttk.Combobox(frame_top, values=all_timezones, state="readonly")
country_combobox.pack(side="left", padx=5)
country_combobox.set("Select a country")

ttk.Button(frame_top, text="Get Time", command=get_initial_time).pack(side="left", padx=5)
ttk.Button(frame_top, text="Calendar Mode", command=show_calendar).pack(side="left", padx=5)

frame_search = ttk.Frame(root, padding="10")  # Search bar frame
frame_search.pack(fill="x")

ttk.Label(frame_search, text="Search Timezone:", font=("Arial", 12)).pack(side="left", padx=5)
search_entry = ttk.Entry(frame_search, width=30)  # Search bar
search_entry.pack(side="left", padx=5)

search_entry.bind("<KeyRelease>", search_timezone)

canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(pady=10)
canvas.create_oval(10, 10, 190, 190)
draw_clock_face()

digital_time_label = ttk.Label(root, text="", font=("Arial", 14), anchor="center", justify="center")
digital_time_label.pack()


# Thêm một label để hiển thị thông tin thời tiết
weather_label = ttk.Label(root, text="", font=("Arial", 12))
weather_label.pack(pady=10)


frame_bottom = ttk.Frame(root, padding="10")
frame_bottom.pack()

ttk.Label(frame_bottom, text="Minutes:").grid(row=0, column=0)
countdown_minutes_entry = ttk.Entry(frame_bottom, width=5)
countdown_minutes_entry.grid(row=0, column=1)

ttk.Label(frame_bottom, text="Seconds:").grid(row=0, column=2)
countdown_seconds_entry = ttk.Entry(frame_bottom, width=5)
countdown_seconds_entry.grid(row=0, column=3)

countdown_label = ttk.Label(frame_bottom, text="00:00", font=("Arial", 24))
countdown_label.grid(row=1, column=0, columnspan=4, pady=10)

ttk.Button(frame_bottom, text="Start", command=start_countdown).grid(row=2, column=0)
ttk.Button(frame_bottom, text="Stop", command=stop_countdown).grid(row=2, column=1)
ttk.Button(frame_bottom, text="Reset", command=reset_countdown).grid(row=2, column=2)

check_reminders()
root.mainloop() 