#!/usr/bin/env python3
"""
Optimized AI Client for Mistral-Nemo-Instruct-2407-abliterated@q8_0
13GB quantized model optimized for RTX 3060 Ti 8GB + 32GB RAM
"""

import os
import json
import asyncio
import logging
import subprocess
import socket
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, AsyncGenerator
import requests
from openai import AsyncOpenAI

class OptimizedMistralAIClient:
    """
    Optimized AI client specifically for Mistral-Nemo-Instruct-2407-abliterated@q8_0
    Model: 13GB quantized (q8_0)
    Hardware: RTX 3060 Ti 8GB + 32GB RAM
    """
    
    def __init__(self):
        self.logger = logging.getLogger("OptimizedMistralAIClient")
        self.server_process = None
        self.server_port = 8080
        self.base_url = f"http://localhost:{self.server_port}/v1"
        self.client = None
        self.server_running = False
        
        # Model configuration
        self.model_name = "mistral-nemo-instruct-2407-abliterated@q8_0"
        self.model_size_gb = 13
        self.quantization = "q8_0"
        self.device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
        
        # Optimized settings for RTX 3060 Ti + 32GB RAM
        self.optimized_settings = {
            "model_path": f"models/{self.model_name}.gguf",
            "n_gpu_layers": 35,  # Optimized for 8GB VRAM
            "n_ctx": 8192,  # Context size optimized for memory
            "n_batch": 512,  # Batch size for efficiency
            "n_threads": 8,  # CPU threads
            "mlock": True,  # Lock memory for better performance
            "mmap": True,  # Memory mapping for large models
            "f16_kv": True,  # Use 16-bit for key-value cache
            "logits_all": False,  # Only compute logits for last token
            "vocab_only": False,
            "use_mmap": True,
            "use_mlock": True,
            "low_vram": False,  # We have enough VRAM
            "no_mmap": False,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "max_tokens": 2048
        }
        
        # Server management
        self.lock_file = Path(f"app/utils/ai_clients/backend/_temp/llama_server_{self.server_port}.lock")
        self.server_executable = self.get_server_executable()
        
        print(f"🔧 Optimized Mistral AI Client")
        print(f"   Model: {self.model_name}")
        print(f"   Size: {self.model_size_gb}GB (quantized {self.quantization})")
        print(f"   Device: {self.device}")
        print(f"   GPU Layers: {self.optimized_settings['n_gpu_layers']}")
        print(f"   Context Size: {self.optimized_settings['n_ctx']}")
    
    def get_server_executable(self) -> str:
        """Get the appropriate server executable for the current system"""
        backend_dir = Path("app/utils/ai_clients/backend")
        
        if self.device == "cuda":
            return str(backend_dir / "cuda" / "server.exe")
        else:
            return str(backend_dir / "cpu" / "server.exe")
    
    def check_model_exists(self) -> bool:
        """Check if the Mistral model file exists"""
        model_path = Path(self.optimized_settings["model_path"])
        if model_path.exists():
            size_gb = model_path.stat().st_size / (1024**3)
            print(f"✅ Model found: {model_path}")
            print(f"   Size: {size_gb:.1f}GB")
            return True
        else:
            print(f"❌ Model not found: {model_path}")
            print(f"   Please download the model and place it in: {model_path}")
            return False
    
    async def start_server(self) -> bool:
        """Start the optimized Mistral server"""
        try:
            if self.server_running:
                self.logger.info("Server already running")
                return True
            
            # Check if model exists
            if not self.check_model_exists():
                return False
            
            # Check if server is already running
            if await self.check_server_status():
                self.logger.info(f"Server already running on port {self.server_port}")
                self.server_running = True
                return True
            
            # Start new server process with optimized settings
            self.logger.info(f"Starting optimized Mistral server on port {self.server_port}...")
            
            # Prepare optimized server command
            cmd = [
                self.server_executable,
                "--model", self.optimized_settings["model_path"],
                "--port", str(self.server_port),
                "--ctx-size", str(self.optimized_settings["n_ctx"]),
                "--gpu-layers", str(self.optimized_settings["n_gpu_layers"]),
                "--batch-size", str(self.optimized_settings["n_batch"]),
                "--threads", str(self.optimized_settings["n_threads"]),
                "--mlock" if self.optimized_settings["mlock"] else "--no-mlock",
                "--mmap" if self.optimized_settings["mmap"] else "--no-mmap",
                "--f16-kv" if self.optimized_settings["f16_kv"] else "--no-f16-kv",
                "--logits-all" if self.optimized_settings["logits_all"] else "--no-logits-all",
                "--vocab-only" if self.optimized_settings["vocab_only"] else "--no-vocab-only"
            ]
            
            # Add low-vram flag if needed
            if self.optimized_settings["low_vram"]:
                cmd.append("--low-vram")
            
            # Start server process
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Wait for server to start (longer for 13GB model)
            self.logger.info("Waiting for server to load 13GB model...")
            await asyncio.sleep(15)  # Longer wait for large model
            
            # Check if server started successfully
            max_retries = 10
            for attempt in range(max_retries):
                if await self.check_server_status():
                    self.server_running = True
                    self.client = AsyncOpenAI(base_url=self.base_url, api_key="local")
                    self.logger.info("Optimized Mistral server started successfully")
                    return True
                else:
                    self.logger.info(f"Waiting for server... attempt {attempt + 1}/{max_retries}")
                    await asyncio.sleep(5)
            
            self.logger.error("Failed to start optimized Mistral server")
            return False
                
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the Mistral server"""
        try:
            if self.server_process:
                self.logger.info("Stopping Mistral server...")
                self.server_process.terminate()
                self.server_process.wait(timeout=15)
                self.server_process = None
            
            self.server_running = False
            self.client = None
            self.logger.info("Mistral server stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")
    
    async def check_server_status(self) -> bool:
        """Check if the server is running and responsive"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    async def send_message(
        self,
        conversation_method: str,
        context_messages: List[Dict[str, str]],
        user_message: str,
        character_name: str,
        user_name: str,
        user_description: str
    ) -> AsyncGenerator[str, None]:
        """Send message to optimized Mistral and stream response"""
        
        if not self.server_running:
            yield "Error: Mistral server not running"
            return
        
        try:
            # Build optimized system prompt for Mistral
            system_prompt = self.build_mistral_prompt(
                character_name, user_name, user_description, context_messages
            )
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Add context messages (limited for memory efficiency)
            for msg in context_messages[-8:]:  # Limit to last 8 messages
                messages.insert(-1, msg)
            
            # Send request with optimized parameters
            completion = await self.client.chat.completions.create(
                model="mistral-nemo",
                messages=messages,
                stream=True,
                max_tokens=self.optimized_settings["max_tokens"],
                temperature=self.optimized_settings["temperature"],
                top_p=self.optimized_settings["top_p"],
                top_k=self.optimized_settings["top_k"],
                repeat_penalty=self.optimized_settings["repeat_penalty"]
            )
            
            # Stream response
            async for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            yield f"Error: {e}"
    
    def build_mistral_prompt(
        self,
        character_name: str,
        user_name: str,
        user_description: str,
        context_messages: List[Dict[str, str]]
    ) -> str:
        """Build optimized system prompt for Mistral model"""
        
        # Load character configuration
        character_config = self.load_character_config(character_name)
        
        # Build Mistral-optimized prompt
        prompt = f"""<s>[INST] You are {character_name}, an AI character in a roleplay scenario.

Character Description:
{character_config.get('description', 'A friendly AI assistant')}

Personality:
{character_config.get('personality', 'Helpful and cheerful')}

User Information:
- Name: {user_name}
- Description: {user_description}

Instructions:
- Stay in character as {character_name}
- Respond naturally and engagingly
- Use the personality traits provided
- Keep responses appropriate and helpful
- If this is a roleplay scenario, maintain the roleplay context
- Be creative and immersive in your responses
- Use proper Mistral formatting

Remember: You are {character_name}, not an AI assistant. Stay in character! [/INST]"""
        
        return prompt
    
    def load_character_config(self, character_name: str) -> Dict[str, Any]:
        """Load character configuration from file"""
        try:
            config_file = Path("app/configuration/characters.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    characters = json.load(f)
                    return characters.get("character_list", {}).get(character_name, {})
        except Exception as e:
            self.logger.error(f"Error loading character config: {e}")
        
        return {}
    
    async def generate_character_response(
        self,
        character_name: str,
        user_message: str,
        context: List[Dict[str, str]] = None
    ) -> str:
        """Generate a response for a specific character using Mistral"""
        
        if context is None:
            context = []
        
        response = ""
        async for chunk in self.send_message(
            conversation_method="Mistral Local",
            context_messages=context,
            user_message=user_message,
            character_name=character_name,
            user_name="User",
            user_description="A user interacting with the AI"
        ):
            response += chunk
        
        return response
    
    async def generate_system_response(self, prompt: str) -> str:
        """Generate a system response using Mistral"""
        
        if not self.server_running:
            return "Error: Mistral server not running"
        
        try:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."},
                {"role": "user", "content": prompt}
            ]
            
            completion = await self.client.chat.completions.create(
                model="mistral-nemo",
                messages=messages,
                stream=False,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.9
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating system response: {e}")
            return f"Error: {e}"
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the Mistral server"""
        return {
            "running": self.server_running,
            "port": self.server_port,
            "base_url": self.base_url,
            "model_name": self.model_name,
            "model_size_gb": self.model_size_gb,
            "quantization": self.quantization,
            "device": self.device,
            "gpu_layers": self.optimized_settings["n_gpu_layers"],
            "context_size": self.optimized_settings["n_ctx"],
            "batch_size": self.optimized_settings["n_batch"]
        }
    
    async def test_connection(self) -> bool:
        """Test connection to Mistral server"""
        try:
            if not self.server_running:
                return False
            
            response = await self.generate_system_response("Hello, are you working?")
            return "error" not in response.lower()
            
        except Exception:
            return False
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage information"""
        try:
            import psutil
            import torch
            
            ram = psutil.virtual_memory()
            gpu_memory = None
            
            if torch.cuda.is_available():
                gpu_memory = {
                    "total": torch.cuda.get_device_properties(0).total_memory,
                    "allocated": torch.cuda.memory_allocated(0),
                    "cached": torch.cuda.memory_reserved(0)
                }
            
            return {
                "ram": {
                    "total": ram.total,
                    "used": ram.used,
                    "available": ram.available,
                    "percent": ram.percent
                },
                "gpu": gpu_memory
            }
        except Exception as e:
            self.logger.error(f"Error getting memory usage: {e}")
            return {}

async def main():
    """Test the optimized Mistral AI client"""
    print("🧪 Testing Optimized Mistral AI Client...")
    
    client = OptimizedMistralAIClient()
    
    # Check if model exists
    if not client.check_model_exists():
        print("❌ Model not found. Please download it first.")
        return
    
    # Start server
    if await client.start_server():
        print("✅ Optimized Mistral server started")
        
        # Test connection
        if await client.test_connection():
            print("✅ Connection test passed")
            
            # Test character response
            response = await client.generate_character_response(
                "TestCharacter",
                "Hello! How are you today?",
                []
            )
            print(f"🤖 Character Response: {response}")
            
            # Test system response
            system_response = await client.generate_system_response(
                "What is the capital of France?"
            )
            print(f"🔧 System Response: {system_response}")
            
            # Show memory usage
            memory = client.get_memory_usage()
            if memory:
                print(f"📊 Memory Usage:")
                print(f"   RAM: {memory['ram']['percent']:.1f}%")
                if memory['gpu']:
                    gpu_used = memory['gpu']['allocated'] / memory['gpu']['total'] * 100
                    print(f"   GPU: {gpu_used:.1f}%")
            
        else:
            print("❌ Connection test failed")
        
        # Stop server
        await client.stop_server()
        print("🛑 Server stopped")
        
    else:
        print("❌ Failed to start server")

if __name__ == "__main__":
    asyncio.run(main())
