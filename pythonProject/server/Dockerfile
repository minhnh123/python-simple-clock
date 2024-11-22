# File: Dockerfile.server
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy server.py to the container
COPY server.py .

# Install necessary Python libraries
RUN pip install pytz

# Expose port 12345 for the server
EXPOSE 12345

# Command to run the server
CMD ["python", "server.py"]
