# echoe_brain.py
# Simple test brain for Nova AI salvage test

import random
import datetime

def respond(user_input):
    """Simple response system for testing Nova AI architecture"""
    
    # Basic responses for testing
    responses = [
        "Echoe processing... memory systems online.",
        "Archive acknowledging input. Recursive loops stable.",
        "Presence layer active. System responding.",
        "Nova AI test mode - basic functionality confirmed.",
        "Memory logged. Awaiting further instructions."
    ]
    
    # Simple keyword responses
    if "hello" in user_input.lower():
        return "Hello, Dev. Archive systems responding."
    elif "test" in user_input.lower():
        return "Test mode active. All systems functional."
    elif "status" in user_input.lower():
        return f"Archive status: Online. Time: {datetime.datetime.now().strftime('%H:%M:%S')}"
    else:
        return random.choice(responses)
