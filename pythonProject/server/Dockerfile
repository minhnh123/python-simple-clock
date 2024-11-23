# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy server code
COPY server.py .

# Install dependencies
RUN pip install pytz

# Expose server port
EXPOSE 12345

# Run server
CMD ["python", "server.py"]
