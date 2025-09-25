#!/usr/bin/env python3
"""
Explore what models are available in Artificial Analysis database
"""

from artificial_analysis_integration import ArtificialAnalysisClient

def main():
    print("🔍 Exploring Artificial Analysis Model Database")
    print("=" * 60)
    
    client = ArtificialAnalysisClient()
    
    # Get all available models
    models_data = client.get_llm_models()
    
    if "error" in models_data:
        print(f"❌ Error: {models_data['error']}")
        return
    
    models = models_data.get("data", [])
    print(f"📊 Found {len(models)} models in database\n")
    
    # Look for models related to our testing
    relevant_families = ["mistral", "gemma", "qwen", "deepseek", "wizardlm", "dolphin", "gpt"]
    
    print("🎯 Models Relevant to Our Testing:")
    print("-" * 40)
    
    found_any = False
    for model in models:
        model_name = model.get("name", "").lower()
        for family in relevant_families:
            if family in model_name:
                found_any = True
                intelligence = model.get("artificial_analysis_intelligence_index", "N/A")
                coding = model.get("artificial_analysis_coding_index", "N/A")
                math = model.get("artificial_analysis_math_index", "N/A")
                
                print(f"\n🤖 {model.get('name', 'Unknown')}")
                print(f"   Intelligence: {intelligence}")
                print(f"   Coding: {coding}")
                print(f"   Math: {math}")
                break
    
    if not found_any:
        print("❌ No directly matching models found")
        print("\n📋 Sample of available models:")
        for i, model in enumerate(models[:10]):
            name = model.get("name", "Unknown")
            intelligence = model.get("artificial_analysis_intelligence_index", "N/A")
            print(f"   {i+1}. {name} (Intelligence: {intelligence})")
    
    print(f"\n🎯 Total models in database: {len(models)}")
    print("=" * 60)
    print("📈 This shows the gap: AA focuses on corporate/API models")
    print("🔥 We're testing community/abliterated models they don't cover!")

if __name__ == "__main__":
    main()
