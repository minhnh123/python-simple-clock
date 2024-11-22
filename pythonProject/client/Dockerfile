# File: Dockerfile.client
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy client.py to the container
COPY client.py .

# Install necessary Python libraries
RUN pip install tk

# Command to run the client
CMD ["python", "client.py"]