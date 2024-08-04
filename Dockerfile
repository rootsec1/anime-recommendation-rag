# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install gcc and python3-dev
RUN apt-get update && apt-get install -y gcc python3-dev

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend/ /app/

# Build argument for MODEL_URL
ARG MODEL_URL

# Set environment variables
ENV MODEL_URL=${MODEL_URL}
ENV PYTHONPATH=/app
ENV TOKENIZERS_PARALLELISM=false

# Expose the port FastAPI is running on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["fastapi", "run", "/app/server.py"]
