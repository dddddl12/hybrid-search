# Use an official Python image to run the Python backend
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the image
COPY . .

# Expose the port the backend listens on
EXPOSE 8080

# Command to run the backend service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
