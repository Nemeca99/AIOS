# Soul of Waifu - Docker Setup

This guide explains how to run Soul of Waifu using Docker containers for easy deployment and management.

## 🐳 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- NVIDIA Docker (for GPU support) - optional but recommended
- X11 server (for GUI) - Linux only

### Basic Usage

1. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

## 🖥️ GUI Support

### Linux (X11)

1. **Allow Docker to access X11:**
   ```bash
   xhost +local:docker
   ```

2. **Run with GUI support:**
   ```bash
   DISPLAY=$DISPLAY docker-compose up
   ```

### Windows

For Windows users, the GUI should work automatically with WSL2 or Docker Desktop.

### macOS

The GUI should work with Docker Desktop for Mac.

## 🎮 GPU Support

### NVIDIA GPU

1. **Install NVIDIA Container Toolkit:**
   ```bash
   # Ubuntu/Debian
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

2. **Run with GPU support:**
   ```bash
   docker-compose up --build
   ```

## 🔊 Audio Support

### Linux

Audio devices are automatically mounted. Make sure your user is in the `audio` group:

```bash
sudo usermod -a -G audio $USER
```

### Windows/macOS

Audio should work automatically with Docker Desktop.

## 📁 Data Persistence

The following directories are mounted as volumes for data persistence:

- `./app/data` - Application data
- `./app/cache` - Cache files
- `./logs` - Log files
- `./assets` - Asset files
- `./app/configuration` - Configuration files

## 🔧 Configuration

### Environment Variables

You can customize the container using environment variables:

```yaml
environment:
  - DISPLAY=:0
  - PYTHONUNBUFFERED=1
  - CUDA_VISIBLE_DEVICES=0
```

### Ports

- `8080` - Main web interface (if available)
- `7860` - Alternative web port

## 🚀 Advanced Usage

### Local LLM Server

Run a separate local LLM server:

```bash
docker-compose --profile llm-server up
```

This will start both Soul of Waifu and a local LLM server.

### Custom Build

Build with specific options:

```bash
docker build -t soul-waifu:custom .
docker run -it --rm soul-waifu:custom
```

### Development Mode

For development with live code changes:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 🛠️ Troubleshooting

### GUI Issues

1. **X11 connection failed:**
   ```bash
   xhost +local:docker
   ```

2. **Permission denied:**
   ```bash
   sudo chmod 666 /tmp/.X11-unix/X0
   ```

### Audio Issues

1. **No audio devices:**
   ```bash
   sudo usermod -a -G audio $USER
   # Then logout and login again
   ```

2. **Permission denied for audio:**
   ```bash
   sudo chmod 666 /dev/snd/*
   ```

### GPU Issues

1. **NVIDIA Docker not working:**
   ```bash
   docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

2. **CUDA not available:**
   Check if NVIDIA drivers and Docker GPU support are properly installed.

## 📊 Monitoring

### View Logs

```bash
docker-compose logs -f soul-of-waifu
```

### Container Stats

```bash
docker stats soul-of-waifu
```

### Shell Access

```bash
docker-compose exec soul-of-waifu bash
```

## 🔒 Security Notes

- The container runs with elevated privileges for audio/GPU access
- X11 access is enabled for GUI support
- Consider using Docker secrets for sensitive configuration

## 📝 Example Commands

```bash
# Build and run
docker-compose up --build

# Run with GPU support
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Remove volumes (careful!)
docker-compose down -v

# Rebuild without cache
docker-compose build --no-cache
```

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify prerequisites are installed
3. Check file permissions
4. Ensure Docker has access to required devices

For more help, refer to the main Soul of Waifu documentation or create an issue on GitHub.
