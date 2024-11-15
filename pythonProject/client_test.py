import pytz
import socket
import tkinter as tk
from datetime import datetime, timedelta
import math

# Initialize global variables
initial_time = None
time_delta = timedelta()
UPDATE_INTERVAL = 100  # Update every 100 ms for smooth animation

# City time zones dictionary
city_timezones = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Ho Chi Minh": "Asia/Ho_Chi_Minh"
}


# Function to connect to the server and get the initial time
def get_initial_time():
    global initial_time
    selected_city = city_var.get()  # Get the selected city from dropdown

    if not selected_city:
        tk.messagebox.showwarning("Warning", "Please select a city")
        return

    timezone = city_timezones.get(selected_city)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Send the timezone name to the server
        client_socket.send(timezone.encode('utf-8'))

        # Receive the time from the server
        received_time = client_socket.recv(1024).decode('utf-8')
        client_socket.close()

        if "Quốc gia không tồn tại" in received_time:
            tk.messagebox.showerror("Error", received_time)
            return

        # Save the initial time and start the clock
        initial_time = datetime.strptime(received_time, '%Y-%m-%d %H:%M:%S')
        update_clock()

    except ConnectionError:
        tk.messagebox.showerror("Error", "Unable to connect to the server")


# Function to update the clock hands smoothly
def update_clock():
    global initial_time, time_delta
    if initial_time is not None:
        # Calculate fractional times for smooth movement
        current_time = initial_time + time_delta
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

        # Increment the time by the update interval
        time_delta += timedelta(milliseconds=UPDATE_INTERVAL)

        # Call update_clock again after 100 ms for smooth animation
        canvas.after(UPDATE_INTERVAL, update_clock)


# Function to draw a clock hand
def draw_hand(angle, length, color):
    angle_rad = math.radians(angle - 90)
    x = 100 + length * math.cos(angle_rad)
    y = 100 + length * math.sin(angle_rad)
    canvas.create_line(100, 100, x, y, width=2, fill=color, tags="hands")


# Draw clock face with hour numbers and minute marks
def draw_clock_face():
    for i in range(60):
        angle = math.radians(i * 6 - 90)  # each minute is 6 degrees
        outer_x = 100 + 90 * math.cos(angle)
        outer_y = 100 + 90 * math.sin(angle)
        inner_x = 100 + (80 if i % 5 == 0 else 85) * math.cos(angle)
        inner_y = 100 + (80 if i % 5 == 0 else 85) * math.sin(angle)
        width = 2 if i % 5 == 0 else 1
        canvas.create_line(outer_x, outer_y, inner_x, inner_y, width=width, fill="black")

    # Draw hour numbers
    for i in range(12):
        angle = math.radians(i * 30 - 60)  # Adjust so 12 is at the top
        x = 100 + 70 * math.cos(angle)
        y = 100 + 70 * math.sin(angle)
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12), fill="black")

    canvas.create_oval(96, 96, 104, 104, fill="black")


# GUI setup
root = tk.Tk()
root.title("World Clock Client")

tk.Label(root, text="Select City:").pack()

# Dropdown for selecting city
city_var = tk.StringVar(root)
city_var.set("New York")  # Default city
city_menu = tk.OptionMenu(root, city_var, *city_timezones.keys())
city_menu.pack()

tk.Button(root, text="Get Time", command=get_initial_time).pack()

# Create canvas for the analog clock
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack()

# Draw the clock face
canvas.create_oval(10, 10, 190, 190)
draw_clock_face()

# Add digital time display
digital_time_label = tk.Label(root, text="", font=("Arial", 16))
digital_time_label.pack()

root.mainloop()
