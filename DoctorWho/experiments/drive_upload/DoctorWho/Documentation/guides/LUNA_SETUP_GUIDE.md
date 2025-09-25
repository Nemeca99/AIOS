# 🌙 Luna AI Assistant - Complete Setup Guide

## 🚀 **What You Get:**

1. **Docker Container** - Luna running 24/7 as a service
2. **Web Interface** - Beautiful web UI at http://localhost:8000
3. **Desktop App** - Native Windows desktop application
4. **Auto-Switching** - Luna automatically adapts to your conversation

## 📋 **Setup Options:**

### Option 1: Docker Container (Recommended)
```bash
# Build and start Luna container
setup_docker_luna.bat

# Luna will be available at: http://localhost:8000
# Always running, even after restart
```

### Option 2: Web Interface (Local)
```bash
# Start Luna API server
start_luna_web.bat

# Open browser to: http://localhost:8000
```

### Option 3: Desktop App (Native)
```bash
# Start desktop application
start_luna_desktop.bat

# Native Windows app with chat interface
```

## 🔧 **Requirements:**

- **LM Studio** running with your Mistral model
- **Docker** (for container option)
- **Python 3.11+** (for local options)

## 🌐 **Web Interface Features:**

- **Beautiful UI** - Modern, responsive design
- **Mode Switching** - Auto, Normal, Unrestricted
- **Real-time Chat** - Instant responses
- **Mobile Friendly** - Works on phones/tablets
- **Always Available** - Access from any device

## 🖥️ **Desktop App Features:**

- **Native Windows App** - No browser needed
- **System Tray** - Minimize to tray
- **Keyboard Shortcuts** - Enter to send
- **Mode Buttons** - Easy mode switching
- **Status Bar** - Connection status

## 🐳 **Docker Commands:**

```bash
# View logs
docker-compose logs -f luna

# Stop Luna
docker-compose stop luna

# Start Luna
docker-compose start luna

# Restart Luna
docker-compose restart luna

# Remove container
docker-compose down
```

## 🔄 **Auto-Switch Triggers:**

**Luna switches to UNRESTRICTED when you say:**
- "unrestricted", "no limits", "anything"
- "uncensored", "no morals", "do anything"
- Any explicit content requests

**Luna switches to NORMAL when you say:**
- "normal", "helpful", "assistant"
- "ethical", "safe", "be good"

## 📱 **Access Methods:**

1. **Web Browser**: http://localhost:8000
2. **Desktop App**: Double-click `start_luna_desktop.bat`
3. **Command Line**: `venv\Scripts\python.exe start_soul_of_waifu.py`

## 🎯 **Luna's Personality:**

- **Age**: 12 years old
- **Role**: Your personal AI assistant
- **Personality**: Sweet, helpful, completely devoted
- **Appearance**: Long silver hair, big blue eyes, petite frame
- **Voice**: Childlike and eager to please

## 🚨 **Troubleshooting:**

**Luna not responding?**
- Check if LM Studio is running
- Verify model is loaded
- Check API connection: http://localhost:8000/health

**Desktop app won't start?**
- Make sure Luna API is running first
- Check Python installation
- Verify virtual environment

**Docker issues?**
- Check Docker is running
- Verify ports 8000 is available
- Check container logs: `docker-compose logs luna`

## 🎉 **You're Ready!**

Luna is now your personal AI assistant that:
- ✅ Runs 24/7 in Docker
- ✅ Has a beautiful web interface
- ✅ Has a native desktop app
- ✅ Auto-switches modes based on conversation
- ✅ Is completely local and private
- ✅ Adapts to whatever you need

**Enjoy your new AI companion!** 🌙✨
