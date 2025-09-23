#!/usr/bin/env python3
"""
Luna Resilient System
Graceful degradation when components fail - ensures Luna always responds
"""

import sys
import os
import time
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "Data" / "processing"))
sys.path.append(str(aios_root / "Data" / "database"))
sys.path.append(str(aios_root / "AI" / "personality"))
sys.path.append(str(aios_root / "Core"))

class LunaResilientSystem:
    """
    Luna system with graceful degradation and component failure handling
    """
    
    def __init__(self):
        # Component availability flags
        self.components = {
            "rag_search": self._test_rag_search(),
            "secure_rag": self._test_secure_rag(),
            "personality_system": self._test_personality_system(),
            "lm_studio": self._test_lm_studio(),
            "error_recovery": self._test_error_recovery()
        }
        
        # Fallback responses for different failure modes
        self.fallback_responses = {
            "no_rag": "I don't have access to my memory right now, but I can still help based on my training.",
            "no_lm_studio": "My language processing is limited right now, but I'm still here to assist.",
            "no_personality": "I'm running in basic mode, but I can still provide helpful responses.",
            "minimal_mode": "I'm running with minimal functionality, but I'm still operational.",
            "emergency_mode": "I'm in emergency mode - basic responses only, but I'm still here."
        }
        
        # Determine operational mode
        self.operational_mode = self._determine_operational_mode()
        
        print(f"SUCCESS: Luna Resilient System initialized - {self.operational_mode} mode")
    
    def _test_rag_search(self) -> bool:
        """Test RAG search availability"""
        try:
            from Data.processing.rag_search import RAGSearcher
            db_path = "Data/AIOS_Database/database/conversations.db"
            if Path(db_path).exists():
                searcher = RAGSearcher(db_path)
                searcher.close()
                return True
        except:
            pass
        return False
    
    def _test_secure_rag(self) -> bool:
        """Test secure RAG search availability"""
        try:
            from secure_rag_search import SecureRAGSearcher
            searcher = SecureRAGSearcher()
            searcher.close()
            return True
        except:
            pass
        return False
    
    def _test_personality_system(self) -> bool:
        """Test personality system availability"""
        try:
            from luna_personality_integration import LunaPersonalityIntegration
            luna = LunaPersonalityIntegration()
            return len(luna.personality_modes) > 0
        except:
            pass
        return False
    
    def _test_lm_studio(self) -> bool:
        """Test LM Studio availability"""
        try:
            response = requests.get("http://localhost:1234", timeout=3)
            return response.status_code == 200
        except:
            pass
        return False
    
    def _test_error_recovery(self) -> bool:
        """Test error recovery system availability"""
        try:
            from error_recovery_system import AIOSErrorRecoverySystem
            return True
        except:
            pass
        return False
    
    def _determine_operational_mode(self) -> str:
        """Determine Luna's operational mode based on available components"""
        available_count = sum(1 for available in self.components.values() if available)
        total_count = len(self.components)
        
        if available_count == total_count:
            return "Full"
        elif available_count >= 4:
            return "High"
        elif available_count >= 3:
            return "Standard"
        elif available_count >= 2:
            return "Limited"
        elif available_count >= 1:
            return "Minimal"
        else:
            return "Emergency"
    
    def generate_resilient_response(self, user_query: str) -> Dict[str, Any]:
        """
        Generate response with graceful degradation based on available components
        """
        response_data = {
            "user_query": user_query,
            "operational_mode": self.operational_mode,
            "components_used": [],
            "fallbacks_used": [],
            "response": "",
            "success": True
        }
        
        try:
            # Try full functionality first
            if self.operational_mode in ["Full", "High"]:
                response_data = self._full_functionality_response(user_query, response_data)
            
            # Degrade gracefully if needed
            elif self.operational_mode == "Standard":
                response_data = self._standard_functionality_response(user_query, response_data)
            
            elif self.operational_mode == "Limited":
                response_data = self._limited_functionality_response(user_query, response_data)
            
            elif self.operational_mode == "Minimal":
                response_data = self._minimal_functionality_response(user_query, response_data)
            
            else:  # Emergency mode
                response_data = self._emergency_mode_response(user_query, response_data)
            
        except Exception as e:
            # Ultimate fallback
            response_data.update({
                "response": f"I encountered an error but I'm still here. Error: {str(e)[:100]}",
                "success": False,
                "error": str(e),
                "fallbacks_used": ["emergency_fallback"]
            })
        
        return response_data
    
    def _full_functionality_response(self, user_query: str, response_data: Dict) -> Dict:
        """Full functionality with all components"""
        try:
            # Use personality system + RAG + LM Studio
            if self.components["personality_system"] and self.components["lm_studio"]:
                from luna_personality_integration import LunaPersonalityIntegration
                luna = LunaPersonalityIntegration()
                
                result = luna.generate_response(user_query, use_rag_context=self.components["rag_search"])
                
                response_data.update({
                    "response": result["response"],
                    "components_used": ["personality_system", "lm_studio"] + (["rag_search"] if self.components["rag_search"] else []),
                    "personality_mode": result.get("personality_mode", "Unknown"),
                    "rag_context_used": result.get("rag_context_used", False)
                })
            
        except Exception as e:
            response_data["fallbacks_used"].append("full_functionality_failed")
            response_data = self._standard_functionality_response(user_query, response_data)
        
        return response_data
    
    def _standard_functionality_response(self, user_query: str, response_data: Dict) -> Dict:
        """Standard functionality without some components"""
        try:
            # Basic personality detection + simple response
            if self.components["personality_system"]:
                from luna_personality_integration import LunaPersonalityIntegration
                luna = LunaPersonalityIntegration()
                
                detected_mood = luna.detect_user_mood(user_query)
                personality_config = luna.personality_modes[detected_mood]
                
                response_data.update({
                    "response": f"I detected you're in {detected_mood} mode. {personality_config['name']} response: I'm here to help with whatever you need.",
                    "components_used": ["personality_system"],
                    "personality_mode": personality_config["name"],
                    "fallbacks_used": response_data["fallbacks_used"] + ["no_lm_studio"]
                })
            
        except Exception as e:
            response_data["fallbacks_used"].append("standard_functionality_failed")
            response_data = self._limited_functionality_response(user_query, response_data)
        
        return response_data
    
    def _limited_functionality_response(self, user_query: str, response_data: Dict) -> Dict:
        """Limited functionality - basic responses only"""
        response_data.update({
            "response": f"I'm running in limited mode. You asked: '{user_query[:50]}...' I'm here but with reduced capabilities.",
            "components_used": ["basic_response"],
            "fallbacks_used": response_data["fallbacks_used"] + ["limited_mode"]
        })
        return response_data
    
    def _minimal_functionality_response(self, user_query: str, response_data: Dict) -> Dict:
        """Minimal functionality - acknowledge only"""
        response_data.update({
            "response": "I'm in minimal mode but still operational. I received your message and I'm here.",
            "components_used": ["minimal_response"],
            "fallbacks_used": response_data["fallbacks_used"] + ["minimal_mode"]
        })
        return response_data
    
    def _emergency_mode_response(self, user_query: str, response_data: Dict) -> Dict:
        """Emergency mode - basic acknowledgment"""
        response_data.update({
            "response": "Emergency mode active. Basic functionality only. I'm still here.",
            "components_used": ["emergency_response"],
            "fallbacks_used": response_data["fallbacks_used"] + ["emergency_mode"]
        })
        return response_data
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and component health"""
        return {
            "operational_mode": self.operational_mode,
            "component_status": self.components,
            "available_components": sum(1 for available in self.components.values() if available),
            "total_components": len(self.components),
            "health_percentage": (sum(1 for available in self.components.values() if available) / len(self.components)) * 100,
            "consciousness_database_status": "Protected" if self.components.get("rag_search") else "Limited Access"
        }


def test_resilient_system():
    """Test Luna's resilient system under various failure conditions"""
    print("🛡️ Testing Luna Resilient System")
    print("=" * 60)
    
    luna = LunaResilientSystem()
    
    # Test 1: System status
    status = luna.get_system_status()
    print(f"📊 System Status:")
    print(f"  Operational Mode: {status['operational_mode']}")
    print(f"  Health: {status['health_percentage']:.1f}%")
    print(f"  Available Components: {status['available_components']}/{status['total_components']}")
    print(f"  Consciousness Database: {status['consciousness_database_status']}")
    
    # Test 2: Response generation under current conditions
    test_queries = [
        "Hello Luna",
        "I'm frustrated with development", 
        "Help me understand AIOS"
    ]
    
    print(f"\n🔍 Testing Responses in {status['operational_mode']} Mode:")
    
    for query in test_queries:
        print(f"\n  Query: {query}")
        result = luna.generate_resilient_response(query)
        
        print(f"  Response: {result['response'][:100]}...")
        print(f"  Components Used: {result['components_used']}")
        if result['fallbacks_used']:
            print(f"  Fallbacks: {result['fallbacks_used']}")
    
    print(f"\n✅ Luna Resilient System test completed")
    print("🛡️ Luna will respond gracefully even when components fail")


if __name__ == "__main__":
    test_resilient_system()
