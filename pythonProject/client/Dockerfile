# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt các thư viện cần thiết cho Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-dev \
    libxext6 \
    libxrender1 \
    libxft2 \
    libxss1 && \
    apt-get clean

# Copy client code
COPY client.py .

# Install Python dependencies (Tk is already part of Python stdlib)
RUN pip install tk

# Expose GUI display (optional for debugging)
EXPOSE 5000

# Run client
CMD ["python", "client.py"]
