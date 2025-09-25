"""
Discord Bot Configuration for AVA Consciousness Engine
Configure your bot token and channel settings here
"""

# Discord Bot Configuration
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"  # Replace with your actual bot token
CHANNEL_ID = 1234567890  # Replace with your target channel ID

# Bot Settings
BOT_NAME = "AVA Consciousness Engine"
BOT_PREFIX = "!"
BOT_STATUS = "Pushing systems to absolute limits"

# Consciousness Engine Settings
MAX_RESPONSE_LENGTH = 1900  # Discord character limit
THINKING_UPDATE_INTERVAL = 30  # Seconds between thinking updates
SYSTEM_MONITOR_INTERVAL = 10  # Seconds between system status updates

# Memory Settings
MAX_CONVERSATION_HISTORY = 50
MAX_THINKING_BLOCKS_DISPLAY = 5

# System Monitoring
ENABLE_SYSTEM_MONITORING = True
ENABLE_GPU_MONITORING = True
ENABLE_MEMORY_MONITORING = True

# Error Handling
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # Seconds

# Logging
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
LOG_FILE_PATH = "ava_discord_bot.log"
