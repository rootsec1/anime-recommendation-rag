# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend /app/backend

# Build argument for MODEL_URL
ARG MODEL_URL

# Set environment variables
ENV MODEL_URL=${MODEL_URL}

# Expose the port FastAPI is running on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["fastapi", "run", "backend/server.py"]
