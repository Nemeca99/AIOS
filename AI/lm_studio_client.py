#!/usr/bin/env python3
"""
LM Studio Client for Mistral-Nemo-Instruct-2407-abliterated@q8_0
Works with LM Studio server running locally
"""

import os
import json
import asyncio
import logging
import requests
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI

class LMStudioClient:
    """
    LM Studio client for Mistral model
    Connects to LM Studio server running locally
    """
    
    def __init__(self, server_url: str = None):
        self.logger = logging.getLogger("LMStudioClient")
        
        # Auto-detect Docker environment
        if os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER'):
            default_url = "http://host.docker.internal:1234/v1"
            print("🐳 Docker environment detected - using host.docker.internal")
        else:
            default_url = "http://localhost:1234/v1"
            print("🖥️ Local environment detected - using localhost")
        
        self.server_url = server_url or os.getenv("LM_STUDIO_URL", default_url)
        self.client = None
        self.server_running = False
    
    def check_server_status(self):
        """Check if LM Studio server is running"""
        try:
            import requests
            response = requests.get(f"{self.server_url}/models", timeout=5)
            self.server_running = response.status_code == 200
            return self.server_running
        except:
            self.server_running = False
            return False
        
        # Model configuration
        self.model_name = "mistral-nemo-instruct-2407-abliterated@q8_0"
        
        print(f"🔧 LM Studio Client")
        print(f"   Server: {self.server_url}")
        print(f"   Model: {self.model_name}")
        
        # Test connection immediately
        self.test_connection()
    
    def test_connection(self) -> bool:
        """Test connection to LM Studio server"""
        try:
            response = requests.get(f"{self.server_url.replace('/v1', '')}/v1/models", timeout=5)
            if response.status_code == 200:
                self.server_running = True
                print("✅ LM Studio server connected")
                return True
            else:
                print(f"❌ LM Studio server error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ LM Studio connection failed: {e}")
            self.server_running = False
            return False
    
    async def start_server(self) -> bool:
        """Check if LM Studio server is running"""
        try:
            self.logger.info("Checking LM Studio server...")
            
            # Test connection to LM Studio
            response = requests.get(f"{self.server_url}/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                self.logger.info(f"LM Studio server running with {len(models.get('data', []))} models")
                
                # Initialize OpenAI client only after confirming server is running
                try:
                    # Use a simple HTTP client instead of AsyncOpenAI to avoid version conflicts
                    self.client = None  # We'll use requests directly
                    self.server_running = True
                    self.logger.info("LM Studio client ready!")
                    return True
                except Exception as client_error:
                    self.logger.error(f"Failed to initialize OpenAI client: {client_error}")
                    return False
            else:
                self.logger.error(f"LM Studio server error: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to connect to LM Studio: {e}")
            return False
    
    async def generate_character_response(
        self, 
        character_name: str, 
        user_input: str, 
        memory: List[Dict] = None
    ) -> str:
        """Generate character response using LM Studio"""
        
        if not self.server_running:
            return "LM Studio server not available"
        
        try:
            # Build conversation context
            messages = []
            
            # Add system prompt
            system_prompt = f"""You are {character_name}, a helpful AI assistant. 
Respond naturally and conversationally. Keep responses concise but engaging."""
            messages.append({"role": "system", "content": system_prompt})
            
            # Add memory context if available
            if memory:
                for mem in memory[-5:]:  # Last 5 memories
                    if "user" in mem and "assistant" in mem:
                        messages.append({"role": "user", "content": mem["user"]})
                        messages.append({"role": "assistant", "content": mem["assistant"]})
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Generate response using requests directly
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            response = requests.post(
                f"{self.server_url}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=300  # 5 minutes for local model
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    return "No response generated"
            else:
                self.logger.error(f"LM Studio API error: {response.status_code}")
                return f"API error: {response.status_code}"
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {e}"
    
    async def generate_response(self, prompt: str) -> str:
        """Generate simple response"""
        
        if not self.server_running:
            return "LM Studio server not available"
        
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                return "No response generated"
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"Error: {e}"
    
    async def stop_server(self):
        """Stop the client (LM Studio server runs independently)"""
        self.logger.info("LM Studio client stopped")
        self.server_running = False
        self.client = None
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "server_url": self.server_url,
            "server_running": self.server_running,
            "model_name": self.model_name
        }

# Test function
async def main():
    """Test LM Studio client"""
    print("🔧 Testing LM Studio Client...")
    
    client = LMStudioClient()
    
    # Check server
    if await client.start_server():
        print("✅ LM Studio server connected")
        
        # Test response
        response = await client.generate_response("Hello, how are you?")
        print(f"🤖 Response: {response}")
        
        # Test character response
        char_response = await client.generate_character_response("Luna", "Tell me about yourself")
        print(f"🌙 Character Response: {char_response}")
        
        # Stop client
        await client.stop_server()
    else:
        print("❌ Failed to connect to LM Studio server")
        print("Please start LM Studio and load your Mistral model")

if __name__ == "__main__":
    asyncio.run(main())
