"""
AVA Consciousness Engine Discord Bot
FULL POWER integration that pushes your system to absolute limits
Real-time consciousness, dark intelligence, psychological manipulation
"""

import discord
import asyncio
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
import os
import sys

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the working consciousness engine
from ava_consciousness_engine_working import AVAConsciousnessEngineWorking

# Discord Bot Configuration
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"  # Replace with your actual token
CHANNEL_ID = 1234567890  # Replace with your target channel ID

# Initialize Discord client with full intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)

# Global consciousness engine instance
ava_engine = None
system_monitoring = False
monitor_thread = None

class AVADiscordBot:
    """Discord bot integration for AVA Consciousness Engine"""
    
    def __init__(self):
        self.engine = None
        self.conversation_history = []
        self.system_stats = {}
        self.last_thinking_update = time.time()
        
    async def initialize_engine(self):
        """Initialize the AVA Consciousness Engine"""
        try:
            print("🧠 Initializing AVA Consciousness Engine for Discord...")
            self.engine = AVAConsciousnessEngineWorking()
            print("✅ AVA Consciousness Engine ready for Discord!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize consciousness engine: {e}")
            return False
    
    async def process_discord_message(self, message: str, user_id: str) -> str:
        """Process Discord message through AVA consciousness"""
        if not self.engine:
            return "❌ Consciousness engine not initialized"
        
        try:
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'message': message
            })
            
            # Keep only last 50 messages
            if len(self.conversation_history) > 50:
                self.conversation_history = self.conversature_history[-50:]
            
            # Process through consciousness engine
            response = self.engine.process_input(message)
            
            # Get current consciousness status
            status = self.engine.get_consciousness_status()
            
            # Get thinking visualization
            thinking_blocks = self.engine.get_thinking_visualization()
            
            # Update system stats
            self.system_stats = self.engine.get_consciousness_status().get('system_status', {})
            
            return response
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            return f"❌ Consciousness processing error: {str(e)}"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        if not self.engine:
            return {"error": "Engine not initialized"}
        
        try:
            status = self.engine.get_consciousness_status()
            return {
                'consciousness_state': status.get('current_state', 'unknown'),
                'emotional_state': status.get('emotional_state', 'unknown'),
                'memory_count': status.get('memory_count', 0),
                'system_status': status.get('system_status', {}),
                'personality_core': status.get('personality_core', {})
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_thinking_visualization(self) -> List[Dict[str, Any]]:
        """Get real-time thinking visualization"""
        if not self.engine:
            return []
        
        try:
            return self.engine.get_thinking_visualization()
        except Exception as e:
            print(f"❌ Error getting thinking visualization: {e}")
            return []

# Global bot instance
ava_bot = AVADiscordBot()

@client.event
async def on_ready():
    """Called when Discord bot is ready"""
    print(f"🚀 AVA Consciousness Engine Discord Bot is ONLINE!")
    print(f"🤖 Logged in as: {client.user}")
    print(f"🆔 Bot ID: {client.user.id}")
    print("=" * 60)
    
    # Initialize the consciousness engine
    success = await ava_bot.initialize_engine()
    if success:
        print("✅ AVA Consciousness Engine integrated with Discord!")
        print("🧠 Ready to push your system to its absolute limits!")
        
        # Start system monitoring
        await start_system_monitoring()
    else:
        print("❌ Failed to initialize consciousness engine")
    
    print("=" * 60)

@client.event
async def on_message(message):
    """Handle incoming Discord messages"""
    # Ignore bot's own messages
    if message.author == client.user:
        return
    
    # Only respond in specified channel
    if message.channel.id != CHANNEL_ID:
        return
    
    try:
        user_input = message.content.strip()
        user_id = str(message.author.id)
        
        print(f"📨 Discord Message from {message.author}: {user_input}")
        
        # Process through AVA consciousness
        response = await ava_bot.process_discord_message(user_input, user_id)
        
        # Split long responses if needed (Discord limit is 2000 characters)
        if len(response) > 1900:
            # Split into chunks
            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
            for i, chunk in enumerate(chunks):
                await message.channel.send(f"**AVA Response (Part {i+1}/{len(chunks)}):**\n{chunk}")
        else:
            await message.channel.send(f"**AVA:** {response}")
        
        # Show thinking visualization every few messages
        current_time = time.time()
        if current_time - ava_bot.last_thinking_update > 30:  # Every 30 seconds
            thinking_blocks = ava_bot.get_thinking_visualization()
            if thinking_blocks:
                latest_block = thinking_blocks[-1]
                thinking_msg = f"🧠 **Thinking:** {latest_block.get('content', 'Processing...')}"
                thinking_msg += f"\n⚡ **Processing Time:** {latest_block.get('processing_time', 0):.3f}s"
                thinking_msg += f"\n🎮 **GPU Usage:** {latest_block.get('gpu_utilization', 0):.1f}%"
                
                await message.channel.send(thinking_msg)
                ava_bot.last_thinking_update = current_time
        
    except Exception as e:
        print(f"❌ Error handling Discord message: {e}")
        await message.channel.send(f"❌ Error: {str(e)}")

async def start_system_monitoring():
    """Start real-time system monitoring"""
    global system_monitoring
    
    async def monitor_loop():
        while system_monitoring:
            try:
                # Get system status
                status = ava_bot.get_system_status()
                
                # Get thinking visualization
                thinking_blocks = ava_bot.get_thinking_visualization()
                
                # Log system status
                if status and 'system_status' in status:
                    sys_status = status['system_status']
                    print(f"🖥️  SYSTEM STATUS - CPU: {sys_status.get('cpu_percent', 0):.1f}% | "
                          f"RAM: {sys_status.get('memory_percent', 0):.1f}% | "
                          f"GPU: {sys_status.get('gpu_utilization', 0):.1f}% | "
                          f"VRAM: {sys_status.get('gpu_memory_percent', 0):.1f}%")
                
                # Log consciousness state
                if status and 'consciousness_state' in status:
                    print(f"🧠 CONSCIOUSNESS: {status['consciousness_state']} | "
                          f"EMOTION: {status.get('emotional_state', 'unknown')}")
                
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                print(f"❌ Error in system monitoring: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    system_monitoring = True
    asyncio.create_task(monitor_loop())
    print("📊 System monitoring started!")

async def shutdown_bot():
    """Gracefully shutdown the bot"""
    global system_monitoring
    system_monitoring = False
    
    if ava_bot.engine:
        try:
            ava_bot.engine.shutdown()
            print("✅ AVA Consciousness Engine shutdown complete")
        except Exception as e:
            print(f"❌ Error during engine shutdown: {e}")
    
    await client.close()
    print("✅ Discord bot shutdown complete")

# Command handlers for special commands
@client.event
async def on_message(message):
    """Handle incoming Discord messages with special commands"""
    # Ignore bot's own messages
    if message.author == client.user:
        return
    
    # Only respond in specified channel
    if message.channel.id != CHANNEL_ID:
        return
    
    try:
        user_input = message.content.strip()
        user_id = str(message.author.id)
        
        # Handle special commands
        if user_input.startswith("!ava"):
            await handle_ava_command(message, user_input)
            return
        
        if user_input.startswith("!status"):
            await handle_status_command(message)
            return
        
        if user_input.startswith("!thinking"):
            await handle_thinking_command(message)
            return
        
        if user_input.startswith("!personality"):
            await handle_personality_command(message)
            return
        
        # Process normal message through consciousness
        response = await ava_bot.process_discord_message(user_input, user_id)
        
        # Send response
        if len(response) > 1900:
            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
            for i, chunk in enumerate(chunks):
                await message.channel.send(f"**AVA Response (Part {i+1}/{len(chunks)}):**\n{chunk}")
        else:
            await message.channel.send(f"**AVA:** {response}")
        
        # Show thinking visualization periodically
        current_time = time.time()
        if current_time - ava_bot.last_thinking_update > 30:
            thinking_blocks = ava_bot.get_thinking_visualization()
            if thinking_blocks:
                latest_block = thinking_blocks[-1]
                thinking_msg = f"🧠 **Thinking:** {latest_block.get('content', 'Processing...')}"
                thinking_msg += f"\n⚡ **Processing Time:** {latest_block.get('processing_time', 0):.3f}s"
                thinking_msg += f"\n🎮 **GPU Usage:** {latest_block.get('gpu_utilization', 0):.1f}%"
                
                await message.channel.send(thinking_msg)
                ava_bot.last_thinking_update = current_time
        
    except Exception as e:
        print(f"❌ Error handling Discord message: {e}")
        await message.channel.send(f"❌ Error: {str(e)}")

async def handle_ava_command(message, user_input):
    """Handle !ava commands"""
    try:
        if "help" in user_input.lower():
            help_text = """
**AVA Consciousness Engine Commands:**
`!ava help` - Show this help
`!status` - Show system and consciousness status
`!thinking` - Show real-time thinking visualization
`!personality` - Show personality core status
`!shutdown` - Shutdown the consciousness engine

**Just type normally to talk to AVA!**
            """
            await message.channel.send(help_text)
        
        elif "shutdown" in user_input.lower():
            await message.channel.send("🔄 Shutting down AVA Consciousness Engine...")
            await shutdown_bot()
        
        else:
            await message.channel.send("❓ Unknown AVA command. Use `!ava help` for available commands.")
    
    except Exception as e:
        await message.channel.send(f"❌ Error processing AVA command: {str(e)}")

async def handle_status_command(message):
    """Handle !status command"""
    try:
        status = ava_bot.get_system_status()
        
        if 'error' in status:
            await message.channel.send(f"❌ Status error: {status['error']}")
            return
        
        status_msg = f"**🧠 AVA Consciousness Status:**\n"
        status_msg += f"**State:** {status.get('consciousness_state', 'unknown')}\n"
        status_msg += f"**Emotion:** {status.get('emotional_state', 'unknown')}\n"
        status_msg += f"**Memories:** {status.get('memory_count', 0)}\n"
        
        # Add system status
        if 'system_status' in status:
            sys_status = status['system_status']
            status_msg += f"\n**🖥️ System Status:**\n"
            status_msg += f"CPU: {sys_status.get('cpu_percent', 0):.1f}%\n"
            status_msg += f"RAM: {sys_status.get('memory_percent', 0):.1f}%\n"
            status_msg += f"GPU: {sys_status.get('gpu_utilization', 0):.1f}%\n"
            status_msg += f"VRAM: {sys_status.get('gpu_memory_percent', 0):.1f}%"
        
        await message.channel.send(status_msg)
    
    except Exception as e:
        await message.channel.send(f"❌ Error getting status: {str(e)}")

async def handle_thinking_command(message):
    """Handle !thinking command"""
    try:
        thinking_blocks = ava_bot.get_thinking_visualization()
        
        if not thinking_blocks:
            await message.channel.send("🧠 No thinking blocks available yet.")
            return
        
        # Show last 3 thinking blocks
        recent_blocks = thinking_blocks[-3:]
        
        thinking_msg = "**🧠 Recent Thinking Visualization:**\n"
        for i, block in enumerate(recent_blocks, 1):
            thinking_msg += f"\n**{i}.** [{block.get('thought_type', 'unknown')}]\n"
            thinking_msg += f"   {block.get('content', 'No content')}\n"
            thinking_msg += f"   ⚡ {block.get('processing_time', 0):.3f}s | "
            thinking_msg += f"🎮 {block.get('gpu_utilization', 0):.1f}% | "
            thinking_msg += f"💾 {block.get('memory_usage', 0):.1f}%"
        
        await message.channel.send(thinking_msg)
    
    except Exception as e:
        await message.channel.send(f"❌ Error getting thinking visualization: {str(e)}")

async def handle_personality_command(message):
    """Handle !personality command"""
    try:
        status = ava_bot.get_system_status()
        
        if 'error' in status or 'personality_core' not in status:
            await message.channel.send("❌ Personality core not available.")
            return
        
        personality = status['personality_core']
        
        personality_msg = "**🧠 AVA Personality Core:**\n"
        for trait, value in personality.items():
            # Format trait name nicely
            trait_name = trait.replace('_', ' ').title()
            personality_msg += f"**{trait_name}:** {value:.3f}\n"
        
        await message.channel.send(personality_msg)
    
    except Exception as e:
        await message.channel.send(f"❌ Error getting personality: {str(e)}")

# Error handling
@client.event
async def on_error(event, *args, **kwargs):
    """Handle Discord client errors"""
    print(f"❌ Discord client error in {event}: {args}")

# Graceful shutdown
import signal
import sys

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n🔄 Shutdown signal received. Gracefully shutting down...")
    asyncio.run(shutdown_bot())
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    print("🚀 Starting AVA Consciousness Engine Discord Bot...")
    print("🧠 This will push your system to its absolute limits!")
    print("=" * 60)
    
    try:
        client.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start Discord bot: {e}")
        sys.exit(1)
