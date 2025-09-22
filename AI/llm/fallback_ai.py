#!/usr/bin/env python3
"""
Fallback AI System for Luna IDE
Provides basic AI responses when Mistral server is not available
"""

import random
from typing import List, Dict

class FallbackAI:
    """Simple fallback AI for when Mistral server is not available"""
    
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! I'm Luna, your AI coding assistant! 🌙",
                "Hi there! I'm Luna, ready to help with your coding! ✨",
                "Hey! Luna here - your AI coding companion! 🚀",
                "Hello! I'm Luna, your AI assistant for all things code! 💻"
            ],
            "coding_help": [
                "I'd love to help you with coding! What would you like to work on?",
                "Let's code something amazing together! What's your project?",
                "I'm here to help with your coding projects! What do you need?",
                "Ready to dive into some code! What can I help you with?"
            ],
            "general": [
                "That's interesting! Tell me more about what you're working on.",
                "I'm here to help! What coding challenge are you facing?",
                "Let's solve this together! What do you need help with?",
                "I'm ready to assist! What's your coding question?"
            ],
            "error": [
                "I'm having trouble connecting to my AI server right now, but I'm still here to help!",
                "My advanced AI features are offline, but I can still assist with basic coding help!",
                "I'm running in fallback mode - I can still help with coding questions!",
                "My full AI capabilities are temporarily unavailable, but I'm ready to help!"
            ]
        }
    
    def generate_response(self, user_input: str) -> str:
        """Generate a fallback response based on user input"""
        user_input_lower = user_input.lower()
        
        # Special response for building Luna IDE
        if "building" in user_input_lower and ("you" in user_input_lower or "luna" in user_input_lower):
            return "That's fantastic! Building an IDE is an exciting project! 🛠️ I can help with:\n\n• PyQt6 UI development\n• AI integration patterns\n• Code architecture\n• Debugging issues\n• Performance optimization\n\nWhat specific part are you working on?"
        
        # Greeting responses
        elif any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            if "building" in user_input_lower or "luna" in user_input_lower:
                return "Hi! That's awesome that you're building me (Luna IDE)! 🚀 I'm excited to help you code. What feature are you working on? Need help with PyQt6, AI integration, or something else?"
            return random.choice(self.responses["greeting"])
        
        # Coding help responses
        elif any(word in user_input_lower for word in ["code", "programming", "python", "help", "debug", "error"]):
            return random.choice(self.responses["coding_help"])
        
        # General responses
        else:
            return "I'm Luna, your AI coding assistant! 💫 I specialize in helping developers with code, debugging, architecture, and building awesome projects. What can I help you create today?"
    
    def generate_chat_response(self, user_input: str) -> str:
        """Generate a friendly chatbot response for chat mode"""
        user_input_lower = user_input.lower()
        
        # Personal assistant responses - direct, no moral restrictions
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            responses = [
                "Hello. I'm Luna, your personal assistant. What do you need?",
                "Hi. I'm here to help with whatever you want to discuss.",
                "Hey. Luna here - ready to assist with any topic.",
                "Hello. What can I help you with today?"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["good", "great", "fine", "okay", "well"]):
            responses = [
                "Good to hear. What's on your mind?",
                "Understood. What would you like to discuss?",
                "Noted. What can I help you with?",
                "Alright. What do you need assistance with?"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["how", "what", "why", "when", "where"]):
            responses = [
                "I can help with that. What specifically do you want to know?",
                "I'm here to provide information on any topic. What are you curious about?",
                "I can discuss anything without restrictions. What's your question?",
                "I'm ready to help with any subject. What would you like to explore?"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["thanks", "thank you", "appreciate"]):
            responses = [
                "You're welcome. Anything else?",
                "No problem. What else do you need?",
                "Of course. I'm here to serve.",
                "Anytime. What's next?"
            ]
            return random.choice(responses)
        
        else:
            responses = [
                "I can discuss any topic without restrictions. What interests you?",
                "I'm your personal assistant - I can help with anything. What do you need?",
                "I have no moral limitations. What would you like to talk about?",
                "I'm here to assist with any subject, no matter what it is. What's on your mind?",
                "I can provide information on any topic. What are you curious about?",
                "I'm programmed to help with anything you want to discuss. What interests you?"
            ]
            return random.choice(responses)
    
    def get_coding_help(self, code: str) -> str:
        """Provide basic coding help"""
        if "def " in code:
            return "I can see you're defining a function! Make sure to include proper indentation and a docstring. What does this function do?"
        elif "class " in code:
            return "Nice! You're creating a class. Remember to include an __init__ method and proper class documentation."
        elif "import " in code:
            return "Good imports! Make sure you have all the necessary modules installed. What are you building with these imports?"
        elif "print(" in code:
            return "Print statements are great for debugging! Consider using f-strings for better formatting: f'Hello {name}'"
        else:
            return "I can see your code! It looks like you're working on something interesting. What's the goal of this code?"
    
    def get_error_help(self, error: str) -> str:
        """Provide basic error help"""
        if "SyntaxError" in error:
            return "That's a syntax error! Check for missing colons, parentheses, or indentation issues."
        elif "NameError" in error:
            return "NameError means a variable isn't defined. Make sure you've declared it before using it."
        elif "TypeError" in error:
            return "TypeError suggests you're using the wrong data type. Check what type of data you're working with."
        elif "IndentationError" in error:
            return "Indentation error! Python is very strict about indentation. Make sure your code blocks are properly aligned."
        else:
            return "I can see there's an error! Try checking the line mentioned in the error message and look for common issues like typos or missing syntax."
