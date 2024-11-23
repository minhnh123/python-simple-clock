import socket
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import math
from pytz import all_timezones

# Global variables for clock
initial_time = None
time_delta = timedelta()
UPDATE_INTERVAL = 100  # Update every 100 ms for smooth animation

# Global variables for countdown timer
countdown_running = False
countdown_time_left = 0
countdown_paused = False


# Function to connect to the server and get the initial time
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
        received_time = client_socket.recv(1024).decode('utf-8')
        client_socket.close()

        if "Country not found" in received_time:
            messagebox.showerror("Error", received_time)
            return

        # Save initial time and start the clock
        initial_time = datetime.strptime(received_time, '%Y-%m-%d %H:%M:%S')
        update_clock()

    except ConnectionError:
        messagebox.showerror("Error", "Cannot connect to server")


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


# Function to draw clock hands
def draw_hand(angle, length, color):
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


# GUI
root = tk.Tk()
root.title("World Clock & Countdown Timer")

# Time zone section
frame_top = ttk.Frame(root, padding="10")
frame_top.pack(fill="x")

ttk.Label(frame_top, text="Select a country:", font=("Arial", 12)).pack(side="left", padx=5)

# Combobox for countries
country_combobox = ttk.Combobox(frame_top, values=all_timezones, state="readonly")
country_combobox.pack(side="left", padx=5)
country_combobox.set("Select a country")

# Button to get time
ttk.Button(frame_top, text="Get Time", command=get_initial_time).pack(side="left", padx=5)

# Clock canvas
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(pady=10)
canvas.create_oval(10, 10, 190, 190)
draw_clock_face()

# Digital clock display
digital_time_label = ttk.Label(root, text="", font=("Arial", 16))
digital_time_label.pack(pady=10)

# Countdown timer section
frame_bottom = ttk.Frame(root, padding="10")
frame_bottom.pack()

ttk.Label(frame_bottom, text="Minutes:").grid(row=0, column=0)
countdown_minutes_entry = ttk.Entry(frame_bottom, width=5)
countdown_minutes_entry.grid(row=0, column=1)

ttk.Label(frame_bottom, text="Seconds:").grid(row=0, column=2)
countdown_seconds_entry = ttk.Entry(frame_bottom, width=5)
countdown_seconds_entry.grid(row=0, column=3)

ttk.Button(frame_bottom, text="Start", command=start_countdown).grid(row=1, column=0)
ttk.Button(frame_bottom, text="Pause", command=stop_countdown).grid(row=1, column=1)
ttk.Button(frame_bottom, text="Reset", command=reset_countdown).grid(row=1, column=2)

# Countdown label
countdown_label = ttk.Label(root, text="00:00", font=("Arial", 20))
countdown_label.pack(pady=20)

root.mainloop()
