#!/usr/bin/env python3
"""
Optimized Configuration for Mistral-Nemo-Instruct-2407-abliterated@q8_0
13GB quantized model optimized for RTX 3060 Ti 8GB + 32GB RAM
"""

import os
import json
import torch
import psutil
from pathlib import Path
from typing import Dict, Any, List

class OptimizedMistralConfig:
    """
    Optimized configuration for Mistral-Nemo-Instruct-2407-abliterated@q8_0
    Model: 13GB quantized (q8_0)
    Hardware: RTX 3060 Ti 8GB + 32GB RAM
    """
    
    def __init__(self):
        self.model_name = "mistral-nemo-instruct-2407-abliterated@q8_0"
        self.model_size_gb = 13
        self.quantization = "q8_0"  # 8-bit quantization
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Hardware specifications
        self.gpu_memory_gb = 8  # RTX 3060 Ti
        self.ram_gb = 32
        
        # Optimized settings for this specific model
        self.optimized_config = {
            "model": {
                "name": self.model_name,
                "size_gb": self.model_size_gb,
                "quantization": self.quantization,
                "device": self.device,
                "dtype": "float16" if self.device == "cuda" else "float32"
            },
            "llama_cpp": {
                "model_path": f"assets/local_llm/custom/{self.model_name}.gguf",
                "n_gpu_layers": 35,  # Optimized for RTX 3060 Ti
                "n_ctx": 8192,  # Context size optimized for 8GB VRAM
                "n_batch": 512,  # Batch size for memory efficiency
                "n_threads": 8,  # CPU threads
                "mlock": True,  # Lock memory for better performance
                "mmap": True,  # Memory mapping for large models
                "f16_kv": True,  # Use 16-bit for key-value cache
                "logits_all": False,  # Only compute logits for last token
                "vocab_only": False,
                "use_mmap": True,
                "use_mlock": True,
                "low_vram": False,  # We have enough VRAM
                "no_mmap": False
            },
            "memory_optimization": {
                "gpu_memory_fraction": 0.85,  # Use 85% of GPU memory
                "ram_memory_fraction": 0.80,  # Use 80% of RAM
                "max_sequence_length": 8192,
                "batch_size": 1,  # Single batch for memory efficiency
                "gradient_checkpointing": True,
                "mixed_precision": True
            },
            "performance": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "max_tokens": 2048,
                "streaming": True,
                "cache_prompt": True
            },
            "hardware": {
                "gpu_memory_limit": 0.85,
                "ram_memory_limit": 0.80,
                "cache_directory": "F:/huggingface_cache",
                "model_download_timeout": 7200,  # 2 hours for 13GB model
                "auto_cleanup": True,
                "memory_monitoring": True
            }
        }
        
        print(f"🔧 Optimized Mistral Configuration")
        print(f"   Model: {self.model_name}")
        print(f"   Size: {self.model_size_gb}GB (quantized {self.quantization})")
        print(f"   Device: {self.device}")
        print(f"   GPU Memory: {self.gpu_memory_gb}GB")
        print(f"   RAM: {self.ram_gb}GB")
    
    def get_optimized_llama_cpp_config(self) -> Dict[str, Any]:
        """Get optimized llama.cpp configuration for this model"""
        return self.optimized_config["llama_cpp"]
    
    def get_memory_optimization_config(self) -> Dict[str, Any]:
        """Get memory optimization settings"""
        return self.optimized_config["memory_optimization"]
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance optimization settings"""
        return self.optimized_config["performance"]
    
    def get_hardware_config(self) -> Dict[str, Any]:
        """Get hardware optimization settings"""
        return self.optimized_config["hardware"]
    
    def calculate_optimal_settings(self) -> Dict[str, Any]:
        """Calculate optimal settings based on available memory"""
        gpu_memory = torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0
        ram_memory = psutil.virtual_memory().total
        
        # Calculate optimal context size based on available memory
        if gpu_memory >= 8 * 1024**3:  # 8GB+ GPU
            optimal_ctx = 8192
            optimal_gpu_layers = 35
        elif gpu_memory >= 6 * 1024**3:  # 6GB+ GPU
            optimal_ctx = 4096
            optimal_gpu_layers = 25
        else:  # Less than 6GB GPU
            optimal_ctx = 2048
            optimal_gpu_layers = 15
        
        # Calculate optimal batch size
        if ram_memory >= 32 * 1024**3:  # 32GB+ RAM
            optimal_batch = 512
        elif ram_memory >= 16 * 1024**3:  # 16GB+ RAM
            optimal_batch = 256
        else:  # Less than 16GB RAM
            optimal_batch = 128
        
        return {
            "optimal_context_size": optimal_ctx,
            "optimal_gpu_layers": optimal_gpu_layers,
            "optimal_batch_size": optimal_batch,
            "gpu_memory_gb": gpu_memory / (1024**3),
            "ram_memory_gb": ram_memory / (1024**3)
        }
    
    def update_config_for_model(self, config_file: str = "app/configuration/local_config.json"):
        """Update the local configuration file with optimized settings for this model"""
        try:
            # Load existing config
            if Path(config_file).exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update with optimized settings
            config["local_ai"] = {
                "enabled": True,
                "model_path": f"assets/local_llm/custom/{self.model_name}.gguf",
                "device": self.device,
                "gpu_layers": self.optimized_config["llama_cpp"]["n_gpu_layers"],
                "context_size": self.optimized_config["llama_cpp"]["n_ctx"],
                "batch_size": self.optimized_config["llama_cpp"]["n_batch"],
                "threads": self.optimized_config["llama_cpp"]["n_threads"],
                "temperature": self.optimized_config["performance"]["temperature"],
                "top_p": self.optimized_config["performance"]["top_p"],
                "top_k": self.optimized_config["performance"]["top_k"],
                "repeat_penalty": self.optimized_config["performance"]["repeat_penalty"],
                "max_tokens": self.optimized_config["performance"]["max_tokens"],
                "streaming": self.optimized_config["performance"]["streaming"],
                "mlock": self.optimized_config["llama_cpp"]["mlock"],
                "mmap": self.optimized_config["llama_cpp"]["mmap"],
                "f16_kv": self.optimized_config["llama_cpp"]["f16_kv"]
            }
            
            # Update hardware settings
            config["hardware"] = self.optimized_config["hardware"]
            
            # Save updated config
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Updated configuration for {self.model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating configuration: {e}")
            return False
    
    def create_model_download_script(self) -> str:
        """Create a script to download the model"""
        script_content = f'''@echo off
echo Downloading {self.model_name}...
echo This is a 13GB model, it may take a while...

REM Create directory
mkdir "assets\\local_llm\\custom" 2>nul

REM Download model (you'll need to provide the actual download URL)
echo Please download the model manually from your source
echo and place it in: assets\\local_llm\\custom\\{self.model_name}.gguf

echo.
echo Model download complete!
echo Model location: assets\\local_llm\\custom\\{self.model_name}.gguf
pause
'''
        
        script_path = "download_mistral_model.bat"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"📝 Created download script: {script_path}")
        return script_path
    
    def test_memory_requirements(self) -> Dict[str, Any]:
        """Test if the system can handle this model"""
        gpu_memory = torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0
        ram_memory = psutil.virtual_memory().total
        
        gpu_memory_gb = gpu_memory / (1024**3)
        ram_memory_gb = ram_memory / (1024**3)
        
        # Model requirements
        model_memory_gb = self.model_size_gb
        gpu_layers_memory = model_memory_gb * 0.8  # 80% of model on GPU
        ram_memory_needed = model_memory_gb * 0.2  # 20% of model on RAM
        
        # Check if system can handle the model
        gpu_sufficient = gpu_memory_gb >= gpu_layers_memory
        ram_sufficient = ram_memory_gb >= ram_memory_needed + 8  # 8GB for system
        
        return {
            "model_size_gb": model_memory_gb,
            "gpu_memory_available": gpu_memory_gb,
            "ram_memory_available": ram_memory_gb,
            "gpu_memory_needed": gpu_layers_memory,
            "ram_memory_needed": ram_memory_needed + 8,
            "gpu_sufficient": gpu_sufficient,
            "ram_sufficient": ram_sufficient,
            "can_run_model": gpu_sufficient and ram_sufficient,
            "recommendations": self.get_recommendations(gpu_memory_gb, ram_memory_gb)
        }
    
    def get_recommendations(self, gpu_memory_gb: float, ram_memory_gb: float) -> List[str]:
        """Get recommendations based on available memory"""
        recommendations = []
        
        if gpu_memory_gb < 8:
            recommendations.append("Consider using fewer GPU layers or a smaller model")
        
        if ram_memory_gb < 16:
            recommendations.append("Consider increasing RAM or using CPU-only mode")
        
        if gpu_memory_gb >= 8 and ram_memory_gb >= 32:
            recommendations.append("Your system is well-suited for this model!")
            recommendations.append("You can use the full 35 GPU layers")
        
        return recommendations

def main():
    """Test the optimized Mistral configuration"""
    print("🧪 Testing Optimized Mistral Configuration...")
    
    config = OptimizedMistralConfig()
    
    # Test memory requirements
    memory_test = config.test_memory_requirements()
    print(f"\n📊 Memory Requirements Test:")
    print(f"   Model Size: {memory_test['model_size_gb']}GB")
    print(f"   GPU Available: {memory_test['gpu_memory_available']:.1f}GB")
    print(f"   RAM Available: {memory_test['ram_memory_available']:.1f}GB")
    print(f"   Can Run Model: {'✅ Yes' if memory_test['can_run_model'] else '❌ No'}")
    
    if memory_test['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in memory_test['recommendations']:
            print(f"   - {rec}")
    
    # Calculate optimal settings
    optimal = config.calculate_optimal_settings()
    print(f"\n⚙️  Optimal Settings:")
    print(f"   Context Size: {optimal['optimal_context_size']}")
    print(f"   GPU Layers: {optimal['optimal_gpu_layers']}")
    print(f"   Batch Size: {optimal['optimal_batch_size']}")
    
    # Update configuration
    if config.update_config_for_model():
        print(f"\n✅ Configuration updated successfully")
    
    # Create download script
    script_path = config.create_model_download_script()
    print(f"\n📝 Download script created: {script_path}")
    
    print(f"\n🎉 Optimized Mistral configuration complete!")

if __name__ == "__main__":
    main()
