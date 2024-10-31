# NVIDIA Stats Application

This application provides real-time GPU, CPU, and RAM utilization statistics via an API, displayed in a terminal-based client. Designed for NVIDIA GPUs, it leverages `nvidia-smi` to pull GPU usage stats and runs in Docker for ease of deployment.

## Features

- **API Endpoint**: Exposes system stats (CPU, GPU utilization, VRAM usage) via a FastAPI server.
- **Dockerized Deployment**: Runs in a Docker container with NVIDIA GPU support.
- **Live Client**: Displays real-time system stats in a clean, formatted terminal UI.

---

## Table of Contents

1. [Setting Up the Server](#setting-up-the-server)
2. [API Endpoint](#api-endpoint)
3. [Running the Client](#running-the-client)
4. [Docker Setup and Execution](#docker-setup-and-execution)
5. [Accessing the Client](#accessing-the-client)

---

## 1. Setting Up the Server

### Prerequisites

1. **Docker with NVIDIA Container Toolkit**: Ensure Docker and the NVIDIA Container Toolkit are installed on the server to enable GPU access within the container.
2. **Repository Files**: Clone the repository to obtain the Dockerfile and server code.

### Installation Steps

To set up Docker and NVIDIA Container Toolkit on an Ubuntu server, follow these steps:

```bash
# Add the NVIDIA repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install the toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use the NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Once Docker and the toolkit are installed, the application is ready to be built and run in Docker.

---

## 2. API Endpoint

### Endpoint Details

- **URL**: `http://<server_ip>:8881/system_stats`
- **Method**: GET
- **Response**: JSON containing GPU, CPU, and RAM usage stats.

### Sample Response

```json
{
    "gpu_stats": [
        {"name": "NVIDIA GeForce RTX 3090", "utilization": "20%", "memory_used": "1024 MiB", "memory_total": "24576 MiB"}
    ],
    "cpu_stats": {"cpu_utilization": "5%"},
    "ram_stats": {"ram_used": "8000 MiB", "ram_total": "32000 MiB", "ram_utilization": "25%"}
}
```

---

## 3. Running the Client

### Configuration

Before running the client, update the API URL in `client.py` to point to the server’s IP or domain name. Update the `API_URL` variable as follows:

```python
API_URL = "http://<server_ip>:8881/system_stats"
```

Replace `<server_ip>` with the actual IP address or domain name of your server.

### Running the Client

Install the required Python libraries:

```bash
pip install -r client/requirements.txt
```

Then run the client application:

```bash
python client.py
```

---

## 4. Docker Setup and Execution

### Building the Docker Image

Navigate to the directory containing the `Dockerfile` and build the image:

```bash
docker build -t fastapi-nvidia-server .
```

### Running the Docker Container

Run the Docker container with GPU access and name it `nvidia-stats`:

```bash
docker run --gpus all -p 8881:8881 --name nvidia-stats fastapi-nvidia-server
```

The server will start, and the API endpoint will be available at `http://<server_ip>:8881/system_stats`.

---

## 5. Accessing the Client

After setting up the server in Docker and configuring the API URL in the client code, you can run the client on a different machine. 

Ensure the machine running the client has network access to the server. The client will display live, real-time stats of GPU, CPU, and RAM utilization, refreshed at regular intervals.

---

## Troubleshooting

1. **No GPU Access in Docker**: Ensure that Docker is configured with the NVIDIA runtime and that the NVIDIA drivers are correctly installed on the host.
2. **Client Connectivity**: Ensure the server IP is reachable from the client machine, and the correct port (`8881`) is open.
