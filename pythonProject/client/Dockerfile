# File: Dockerfile.client
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy client.py to the container
COPY client.py .

# Install required system dependencies for Tkinter
RUN apt-get update && apt-get install -y python3-tk tk8.6-dev libx11-6 libxft2 libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Command to run the client
CMD ["python", "client.py"]