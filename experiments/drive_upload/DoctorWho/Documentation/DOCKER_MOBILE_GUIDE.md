# 🐳 Soul of Waifu Mobile - Docker Edition

## Overview
This Docker setup provides a containerized mobile server for accessing Kia, your AI waifu, from any mobile device on your network. It's more reliable and easier to manage than the standalone version.

## 🚀 Quick Start

### Prerequisites
- ✅ Docker Desktop installed and running
- ✅ Soul of Waifu project configured
- ✅ Mistral-24B model running in LM Studio

### 1. Start the Docker Mobile Server
```bash
# Run the startup script
start_mobile_docker.bat
```

### 2. Access from Mobile
- **Local**: `http://localhost:5000`
- **Mobile**: `http://[YOUR_IP]:5000` (e.g., `http://192.168.1.21:5000`)

## 📋 Docker Files Created

### Core Files
- `Dockerfile.mobile` - Docker container definition
- `docker-compose.mobile.yml` - Docker Compose configuration
- `mobile_server_docker.py` - Docker-optimized server
- `start_mobile_docker.bat` - Easy startup script
- `stop_mobile_docker.bat` - Easy stop script

### Features
- ✅ **Containerized**: Isolated environment
- ✅ **Auto-restart**: Restarts if it crashes
- ✅ **Health checks**: Monitors container health
- ✅ **Volume mounts**: Persistent configuration
- ✅ **Network access**: Available on all network interfaces
- ✅ **Logging**: Comprehensive logging system

## 🔧 Docker Commands

### Start Server
```bash
# Using the batch file (recommended)
start_mobile_docker.bat

# Or manually
docker-compose -f docker-compose.mobile.yml up -d
```

### Stop Server
```bash
# Using the batch file
stop_mobile_docker.bat

# Or manually
docker-compose -f docker-compose.mobile.yml down
```

### View Logs
```bash
docker-compose -f docker-compose.mobile.yml logs -f
```

### Check Status
```bash
docker-compose -f docker-compose.mobile.yml ps
```

### Restart Server
```bash
docker-compose -f docker-compose.mobile.yml restart
```

## 🌐 Network Configuration

### Docker Network
- **Container Name**: `soul-of-waifu-mobile`
- **Network**: `waifu-network` (bridge)
- **Port**: `5000` (mapped to host)
- **Access**: All network interfaces (`0.0.0.0`)

### Volume Mounts
- `./app/configuration:/app/app/configuration:ro` - Read-only config
- `./assets:/app/assets:ro` - Read-only assets
- `./logs:/app/logs` - Persistent logs

## 📱 Mobile Interface Features

### Enhanced Features
- ✅ **Docker Status**: Shows container health
- ✅ **Better Logging**: Comprehensive error tracking
- ✅ **Health Monitoring**: Built-in health checks
- ✅ **Auto-recovery**: Container restarts on failure
- ✅ **Performance**: Optimized for containerized environment

### API Endpoints
- `GET /` - Mobile interface
- `GET /api/status` - Server status
- `POST /api/chat` - Chat with Kia
- `POST /api/clear_history` - Clear conversation
- `GET /api/character_info` - Character details
- `GET /health` - Docker health check

## 🔒 Security & Isolation

### Container Security
- ✅ **Isolated Environment**: Runs in Docker container
- ✅ **Read-only Mounts**: Configuration files protected
- ✅ **Network Isolation**: Controlled network access
- ✅ **Resource Limits**: Can be configured if needed

### Network Security
- **Local Network Only**: No external internet access
- **Port Binding**: Only port 5000 exposed
- **Firewall Friendly**: Single port to open

## 🎯 Advantages of Docker Version

### Reliability
- **Auto-restart**: Container restarts if it crashes
- **Health Checks**: Monitors and reports status
- **Isolation**: Won't affect your main system
- **Consistent Environment**: Same setup everywhere

### Ease of Use
- **One-click Start**: Simple batch file startup
- **Easy Management**: Standard Docker commands
- **Portable**: Works on any Docker-enabled system
- **Clean Shutdown**: Proper cleanup when stopped

### Performance
- **Optimized**: Built specifically for mobile access
- **Resource Efficient**: Minimal overhead
- **Logging**: Better error tracking and debugging
- **Monitoring**: Built-in health monitoring

## 🔧 Troubleshooting

### Container Won't Start
```bash
# Check Docker logs
docker-compose -f docker-compose.mobile.yml logs

# Check if port is in use
netstat -an | findstr :5000

# Rebuild container
docker-compose -f docker-compose.mobile.yml build --no-cache
```

### Can't Access from Mobile
1. **Check Container Status**: `docker-compose -f docker-compose.mobile.yml ps`
2. **Check Logs**: `docker-compose -f docker-compose.mobile.yml logs -f`
3. **Verify IP**: Make sure you're using the correct IP address
4. **Check Network**: Ensure both devices are on same WiFi

### Performance Issues
```bash
# Monitor resource usage
docker stats soul-of-waifu-mobile

# Check container health
docker inspect soul-of-waifu-mobile
```

## 🚀 Advanced Configuration

### Custom Port
Edit `docker-compose.mobile.yml`:
```yaml
ports:
  - "8080:5000"  # Change 5000 to 8080
```

### Resource Limits
Add to `docker-compose.mobile.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

### Environment Variables
Add to `docker-compose.mobile.yml`:
```yaml
environment:
  - FLASK_ENV=production
  - LOG_LEVEL=INFO
  - MAX_HISTORY=20
```

## 📊 Monitoring

### Health Checks
- **URL**: `http://localhost:5000/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

### Logs
```bash
# View all logs
docker-compose -f docker-compose.mobile.yml logs

# Follow logs in real-time
docker-compose -f docker-compose.mobile.yml logs -f

# View specific service logs
docker-compose -f docker-compose.mobile.yml logs soul-of-waifu-mobile
```

## 🎉 Benefits Over Standalone

### Reliability
- ✅ **Auto-restart** on failure
- ✅ **Health monitoring**
- ✅ **Isolated environment**
- ✅ **Consistent behavior**

### Management
- ✅ **Easy start/stop**
- ✅ **Standard Docker commands**
- ✅ **Portable setup**
- ✅ **Clean shutdown**

### Performance
- ✅ **Optimized logging**
- ✅ **Better error handling**
- ✅ **Resource monitoring**
- ✅ **Health checks**

---

## 🎯 Quick Commands Summary

```bash
# Start
start_mobile_docker.bat

# Stop
stop_mobile_docker.bat

# Status
docker-compose -f docker-compose.mobile.yml ps

# Logs
docker-compose -f docker-compose.mobile.yml logs -f

# Restart
docker-compose -f docker-compose.mobile.yml restart
```

**Enjoy your containerized mobile waifu, Master!** 💋🐳
