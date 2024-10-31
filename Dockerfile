# Dockerfile
FROM nvidia/cuda:12.2.0-base-ubuntu22.04
# Set up environment
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Install FastAPI and dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy server code
COPY server.py /app/server.py
WORKDIR /app

# Expose the FastAPI port
EXPOSE 8881

# Run FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8881"]
