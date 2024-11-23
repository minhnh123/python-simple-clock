# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy client code
COPY client.py .

# Install dependencies
RUN pip install tk

# Expose GUI display (optional for debugging)
EXPOSE 5000

# Run client
CMD ["python", "client.py"]
