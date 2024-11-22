import socket
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import math

# Global variables for clock
initial_time = None
time_delta = timedelta()

# Global variables for countdown timer
countdown_running = False
countdown_time_left = 0


# Function to connect to the server and get the initial time
def get_initial_time():
    global initial_time
    country = country_entry.get()

    if not country:
        messagebox.showwarning("Warning", "Please enter a country name")
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


# Function to update the clock hands
def update_clock():
    global initial_time, time_delta
    if initial_time is not None:
        current_time = initial_time + time_delta
        hour, minute, second = current_time.hour % 12, current_time.minute, current_time.second

        # Calculate angles for clock hands
        hour_angle = (hour + minute / 60) * 30
        minute_angle = (minute + second / 60) * 6
        second_angle = second * 6

        # Clear old hands
        canvas.delete("hands")

        # Draw hour hand
        draw_hand(hour_angle, 50, "blue")

        # Draw minute hand
        draw_hand(minute_angle, 70, "green")

        # Draw second hand
        draw_hand(second_angle, 90, "red")

        # Display digital time
        digital_time_label.config(text=current_time.strftime('%Y-%m-%d, %H:%M:%S'))

        # Increment time by 1 second
        time_delta += timedelta(seconds=1)

        # Call update_clock after 1000ms (1 second)
        canvas.after(1000, update_clock)


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
    global countdown_running, countdown_time_left

    if countdown_running:
        messagebox.showwarning("Warning", "Countdown is already running!")
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
    global countdown_running, countdown_time_left

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
    global countdown_running
    countdown_running = False


# GUI
root = tk.Tk()
root.title("World Clock with Countdown Timer")

# Time zone section
tk.Label(root, text="Enter country name:").pack()
country_entry = tk.Entry(root)
country_entry.pack()

tk.Button(root, text="Get Time", command=get_initial_time).pack()

# Clock canvas
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack()
canvas.create_oval(10, 10, 190, 190)
draw_clock_face()

# Digital clock display
digital_time_label = tk.Label(root, text="", font=("Arial", 16))
digital_time_label.pack()

# Countdown timer section
tk.Label(root, text="Countdown Timer").pack(pady=10)
countdown_frame = tk.Frame(root)
countdown_frame.pack()

tk.Label(countdown_frame, text="Minutes:").grid(row=0, column=0)
countdown_minutes_entry = tk.Entry(countdown_frame, width=5)
countdown_minutes_entry.grid(row=0, column=1)

tk.Label(countdown_frame, text="Seconds:").grid(row=0, column=2)
countdown_seconds_entry = tk.Entry(countdown_frame, width=5)
countdown_seconds_entry.grid(row=0, column=3)

tk.Button(countdown_frame, text="Start", command=start_countdown).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(countdown_frame, text="Stop", command=stop_countdown).grid(row=1, column=2, columnspan=2, pady=5)

# Countdown label
countdown_label = tk.Label(root, text="00:00", font=("Arial", 20))
countdown_label.pack(pady=10)

root.mainloop()
