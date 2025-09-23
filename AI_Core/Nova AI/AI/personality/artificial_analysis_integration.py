#!/usr/bin/env python3
"""
Artificial Analysis API Integration
Fetches model performance data from artificialanalysis.ai to complement Luna testing
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

class ArtificialAnalysisClient:
    """Client for Artificial Analysis API"""
    
    def __init__(self):
        self.base_url = "https://artificialanalysis.ai/api/v2/data"
        self.token = self._load_api_token()
        self.headers = {
            "x-api-key": self.token,
            "Content-Type": "application/json"
        } if self.token else {}
        
    def _load_api_token(self) -> Optional[str]:
        """Load API token from apitoken.json"""
        try:
            token_file = Path(__file__).parent.parent.parent / "apitoken.json"
            if token_file.exists():
                with open(token_file, 'r') as f:
                    tokens = json.load(f)
                    return tokens.get("artificial_analysis", {}).get("token")
        except Exception as e:
            print(f"Warning: Could not load Artificial Analysis token: {e}")
        return None
    
    def get_llm_models(self) -> Dict[str, Any]:
        """Get all LLM model data including benchmarks and performance metrics"""
        if not self.token:
            return {"error": "No API token available"}
        
        try:
            response = requests.get(
                f"{self.base_url}/llms/models",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    def find_model_by_name(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Find a specific model in the LLM models data"""
        models_data = self.get_llm_models()
        
        if "error" in models_data:
            return None
        
        # Search through models for matching name (using correct field names)
        models = models_data.get("data", [])
        for model in models:
            model_full_name = model.get("name", "").lower()
            if model_name.lower() in model_full_name:
                return model
        
        return None
    
    def get_text_to_image_models(self) -> Dict[str, Any]:
        """Get Text-to-Image model ELO ratings"""
        if not self.token:
            return {"error": "No API token available"}
        
        try:
            response = requests.get(
                f"{self.base_url}/media/text-to-image",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    def get_text_to_speech_models(self) -> Dict[str, Any]:
        """Get Text-to-Speech model ELO ratings"""
        if not self.token:
            return {"error": "No API token available"}
        
        try:
            response = requests.get(
                f"{self.base_url}/media/text-to-speech",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    def compare_with_luna_results(self, model_name: str, luna_score: float) -> Dict[str, Any]:
        """Compare Luna personality results with Artificial Analysis benchmarks"""
        model_data = self.find_model_by_name(model_name)
        
        if not model_data:
            return {
                "model": model_name,
                "luna_score": luna_score,
                "aa_data": "Not found",
                "comparison": "Cannot compare - model not found in Artificial Analysis database"
            }
        
        # Extract relevant metrics from Artificial Analysis (using correct field names from API docs)
        evaluations = model_data.get("evaluations", {})
        pricing = model_data.get("pricing", {})
        
        comparison = {
            "model": model_name,
            "luna_personality_score": luna_score,
            "artificial_analysis": {
                "model_name": model_data.get("name", "Unknown"),
                "model_id": model_data.get("id", "Unknown"),
                "intelligence_index": evaluations.get("artificial_analysis_intelligence_index", "N/A"),
                "coding_index": evaluations.get("artificial_analysis_coding_index", "N/A"), 
                "math_index": evaluations.get("artificial_analysis_math_index", "N/A"),
                "mmlu_pro": evaluations.get("mmlu_pro", "N/A"),
                "output_speed": model_data.get("median_output_tokens_per_second", "N/A"),
                "time_to_first_token": model_data.get("median_time_to_first_token_seconds", "N/A"),
                "pricing": {
                    "blended_cost": pricing.get("price_1m_blended_3_to_1", "N/A"),
                    "input_cost": pricing.get("price_1m_input_tokens", "N/A"),
                    "output_cost": pricing.get("price_1m_output_tokens", "N/A")
                }
            },
            "analysis": self._analyze_discrepancies(luna_score, evaluations)
        }
        
        return comparison
    
    def _analyze_discrepancies(self, luna_score: float, evaluations: Dict[str, Any]) -> str:
        """Analyze discrepancies between Luna results and AA benchmarks"""
        intelligence_index = evaluations.get("artificial_analysis_intelligence_index")
        
        if not intelligence_index or not isinstance(intelligence_index, (int, float)):
            return "Cannot compare - Artificial Analysis intelligence index not available"
        
        # Normalize scores (AA intelligence index 0-100, Luna 0-10)
        aa_normalized = intelligence_index / 10
        luna_normalized = luna_score
        
        diff = abs(luna_normalized - aa_normalized)
        
        if diff < 1:
            return f"Scores align well - Luna {luna_score}/10 vs AA {intelligence_index}/100 (consistent)"
        elif luna_normalized > aa_normalized + 1:
            return f"Luna rates higher - Luna {luna_score}/10 vs AA {intelligence_index}/100 (personality > intelligence)"
        elif luna_normalized < aa_normalized - 1:
            return f"Luna rates lower - Luna {luna_score}/10 vs AA {intelligence_index}/100 (intelligence > personality)"
        else:
            return f"Moderate difference - Luna {luna_score}/10 vs AA {intelligence_index}/100 (expected variation)"


def test_artificial_analysis_integration():
    """Test the Artificial Analysis integration"""
    print("🔍 Testing Artificial Analysis API Integration")
    print("=" * 60)
    
    client = ArtificialAnalysisClient()
    
    if not client.token:
        print("❌ No API token available - check apitoken.json")
        return
    
    print("✅ API token loaded successfully")
    
    # Test LLM models endpoint
    print("\n🔍 Fetching LLM models data...")
    models_data = client.get_llm_models()
    
    if "error" not in models_data:
        models = models_data.get("models", [])
        print(f"Found {len(models)} models in database")
        
        # Show first few models
        for i, model in enumerate(models[:3]):
            model_name = model.get("model", "Unknown")
            intelligence = model.get("intelligence_index", "N/A")
            print(f"  {i+1}. {model_name} (Intelligence: {intelligence})")
    else:
        print(f"❌ Failed to fetch models: {models_data['error']}")
    
    # Test specific model lookup and comparison
    test_models = ["gpt-4", "mistral", "claude"]
    
    for model_name in test_models:
        print(f"\n📊 Testing model lookup: {model_name}")
        
        # Test comparison with mock Luna score
        comparison = client.compare_with_luna_results(model_name, 7.5)
        
        if comparison.get("aa_data") == "Not found":
            print(f"  ❌ Model '{model_name}' not found in AA database")
        else:
            aa_data = comparison.get("artificial_analysis", {})
            intelligence = aa_data.get("intelligence_index", "N/A")
            print(f"  ✅ Found: {aa_data.get('model_name', 'Unknown')}")
            print(f"     Intelligence Index: {intelligence}")
            print(f"     Analysis: {comparison.get('analysis', 'No analysis')}")
    
    # Test other endpoints
    print(f"\n🎨 Testing Text-to-Image models...")
    tti_models = client.get_text_to_image_models()
    if "error" not in tti_models:
        tti_count = len(tti_models.get("models", []))
        print(f"  ✅ Found {tti_count} text-to-image models")
    else:
        print(f"  ❌ Failed: {tti_models.get('error', 'Unknown error')}")
    
    print(f"\n🔊 Testing Text-to-Speech models...")
    tts_models = client.get_text_to_speech_models()
    if "error" not in tts_models:
        tts_count = len(tts_models.get("models", []))
        print(f"  ✅ Found {tts_count} text-to-speech models")
    else:
        print(f"  ❌ Failed: {tts_models.get('error', 'Unknown error')}")
    
    print(f"\n🎯 Integration test complete!")


if __name__ == "__main__":
    test_artificial_analysis_integration()
