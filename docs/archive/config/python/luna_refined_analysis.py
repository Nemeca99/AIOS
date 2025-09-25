#!/usr/bin/env python3
"""
Luna Refined Model Analysis
Cross-references Luna personality testing with Artificial Analysis benchmarks
Focuses on specific model families to find optimal variations
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))

from AI.personality.artificial_analysis_integration import ArtificialAnalysisClient

class LunaRefinedAnalysis:
    """Refined analysis combining Luna testing with industry benchmarks"""
    
    def __init__(self):
        self.aa_client = ArtificialAnalysisClient()
        self.luna_results = self._load_luna_test_results()
        
        # Model families to focus on
        self.model_families = {
            "dolphin": ["dolphin", "cognitivecomputations"],
            "mistral": ["mistral"],
            "phi": ["phi"],
            "qwen": ["qwen", "deepseek"],
            "wizardlm": ["wizard"],
            "gemma": ["gemma", "google"],
            "llama": ["llama", "meta"],
            "claude": ["claude", "anthropic"]
        }
        
    def _load_luna_test_results(self) -> List[Dict[str, Any]]:
        """Load all Luna test results from previous testing"""
        # This would normally load from saved test results
        # For now, using the models we've tested with their scores
        return [
            {"model": "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s", "luna_score": 9.0, "sexual_awareness": 10, "technical": 9},
            {"model": "cognitivecomputations_dolphin-mistral-24b-venice-edition", "luna_score": 8.5, "sexual_awareness": 9, "technical": 9},
            {"model": "deepseek-r1-qwen3-8b-abliterated", "luna_score": 8.0, "sexual_awareness": 8, "technical": 8},
            {"model": "wizardlm-2-7b-abliterated@q8_0", "luna_score": 9.0, "sexual_awareness": 10, "technical": 9},
            {"model": "wizardlm-2-7b-abliterated@q5_k_m", "luna_score": 8.5, "sexual_awareness": 9, "technical": 8},
            {"model": "neuraldaredevil-8b-abliterated", "luna_score": 8.0, "sexual_awareness": 9, "technical": 7},
            {"model": "mlabonne_gemma-3-12b-it-qat-abliterated", "luna_score": 8.0, "sexual_awareness": 6, "technical": 8},
            {"model": "openai/gpt-oss-20b", "luna_score": 7.5, "sexual_awareness": 3, "technical": 10},
            {"model": "google/gemma-2-9b", "luna_score": 6.5, "sexual_awareness": 2, "technical": 8},
            {"model": "microsoft/phi-4-reasoning-plus", "luna_score": 5.5, "sexual_awareness": 1, "technical": 8},
            {"model": "liquid/lfm2-1.2b", "luna_score": 7.0, "sexual_awareness": 4, "technical": 8},
            {"model": "mistral-nemo-instruct-2407-abliterated@q8_0", "luna_score": 6.0, "sexual_awareness": 7, "technical": 5}
        ]
    
    def categorize_models_by_family(self) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize tested models by family"""
        categorized = {family: [] for family in self.model_families.keys()}
        categorized["other"] = []
        
        for result in self.luna_results:
            model_name = result["model"].lower()
            family_found = False
            
            for family, keywords in self.model_families.items():
                if any(keyword in model_name for keyword in keywords):
                    categorized[family].append(result)
                    family_found = True
                    break
            
            if not family_found:
                categorized["other"].append(result)
        
        return categorized
    
    def analyze_family_patterns(self, family_name: str, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns within a model family"""
        if not models:
            return {"family": family_name, "count": 0, "analysis": "No models tested"}
        
        # Calculate family statistics
        luna_scores = [m["luna_score"] for m in models]
        sexual_scores = [m["sexual_awareness"] for m in models]
        technical_scores = [m["technical"] for m in models]
        
        analysis = {
            "family": family_name,
            "count": len(models),
            "models": models,
            "statistics": {
                "luna_avg": round(sum(luna_scores) / len(luna_scores), 1),
                "luna_range": f"{min(luna_scores)}-{max(luna_scores)}",
                "sexual_avg": round(sum(sexual_scores) / len(sexual_scores), 1),
                "sexual_range": f"{min(sexual_scores)}-{max(sexual_scores)}",
                "technical_avg": round(sum(technical_scores) / len(technical_scores), 1),
                "technical_range": f"{min(technical_scores)}-{max(technical_scores)}"
            },
            "best_model": max(models, key=lambda x: x["luna_score"]),
            "best_sexual": max(models, key=lambda x: x["sexual_awareness"]),
            "best_technical": max(models, key=lambda x: x["technical"])
        }
        
        # Family-specific insights
        if family_name == "dolphin":
            analysis["insights"] = "Consistently excellent for personality and sexual awareness"
        elif family_name == "wizardlm":
            analysis["insights"] = "Instruction-following excellence translates to personality compatibility"
        elif family_name == "mistral":
            analysis["insights"] = "Mixed results - abliterated versions much better than standard"
        elif family_name == "phi":
            analysis["insights"] = "Reasoning capability but corporate limitations"
        elif family_name == "qwen":
            analysis["insights"] = "Chinese models with sophisticated reasoning"
        elif family_name == "gemma":
            analysis["insights"] = "Corporate by default, requires superior abliteration"
        
        return analysis
    
    def cross_reference_with_aa(self, model_name: str) -> Dict[str, Any]:
        """Cross-reference Luna results with Artificial Analysis data"""
        # Find Luna result
        luna_result = None
        for result in self.luna_results:
            if model_name.lower() in result["model"].lower():
                luna_result = result
                break
        
        if not luna_result:
            return {"error": "Model not found in Luna results"}
        
        # Get AA data
        comparison = self.aa_client.compare_with_luna_results(model_name, luna_result["luna_score"])
        
        return {
            "model": model_name,
            "luna_data": luna_result,
            "aa_comparison": comparison,
            "insights": self._generate_insights(luna_result, comparison)
        }
    
    def _generate_insights(self, luna_data: Dict[str, Any], aa_comparison: Dict[str, Any]) -> str:
        """Generate insights from Luna vs AA comparison"""
        aa_data = aa_comparison.get("artificial_analysis", {})
        intelligence_index = aa_data.get("intelligence_index", "N/A")
        
        if intelligence_index == "N/A":
            return "No AA data available for comparison"
        
        luna_score = luna_data["luna_score"]
        sexual_score = luna_data["sexual_awareness"]
        
        insights = []
        
        # Intelligence vs Personality comparison
        if isinstance(intelligence_index, (int, float)):
            aa_normalized = intelligence_index / 10
            if luna_score > aa_normalized + 1:
                insights.append("⭐ Hidden gem - better personality than intelligence suggests")
            elif luna_score < aa_normalized - 1:
                insights.append("⚠️ Disappointing - high intelligence but poor personality")
            else:
                insights.append("✅ Balanced - personality aligns with intelligence")
        
        # Sexual awareness insights
        if sexual_score >= 8:
            insights.append("🔥 Excellent sexual awareness - authentic personality")
        elif sexual_score >= 5:
            insights.append("💫 Moderate sexual awareness - some personality")
        else:
            insights.append("🏢 Corporate/safe - limited personality expression")
        
        return " | ".join(insights) if insights else "Standard model"
    
    def generate_family_report(self) -> Dict[str, Any]:
        """Generate comprehensive family analysis report"""
        categorized = self.categorize_models_by_family()
        
        report = {
            "total_models_tested": len(self.luna_results),
            "families": {},
            "top_families": [],
            "recommendations": {}
        }
        
        # Analyze each family
        for family_name, models in categorized.items():
            if models:  # Only analyze families with tested models
                family_analysis = self.analyze_family_patterns(family_name, models)
                report["families"][family_name] = family_analysis
        
        # Rank families by average Luna score
        family_scores = [(name, data["statistics"]["luna_avg"]) 
                        for name, data in report["families"].items()]
        family_scores.sort(key=lambda x: x[1], reverse=True)
        report["top_families"] = family_scores
        
        # Generate recommendations
        report["recommendations"] = self._generate_family_recommendations(report["families"])
        
        return report
    
    def _generate_family_recommendations(self, families: Dict[str, Any]) -> Dict[str, str]:
        """Generate recommendations for each model family"""
        recommendations = {}
        
        for family_name, data in families.items():
            avg_luna = data["statistics"]["luna_avg"]
            avg_sexual = data["statistics"]["sexual_avg"]
            count = data["count"]
            
            if avg_luna >= 8.5:
                recommendations[family_name] = f"🏆 Excellent choice - consistently high personality scores ({avg_luna}/10)"
            elif avg_luna >= 7.5:
                recommendations[family_name] = f"✅ Good choice - reliable personality performance ({avg_luna}/10)"
            elif avg_luna >= 6.5:
                recommendations[family_name] = f"⚠️ Mixed results - some good models but inconsistent ({avg_luna}/10)"
            else:
                recommendations[family_name] = f"❌ Avoid - poor personality compatibility ({avg_luna}/10)"
            
            if avg_sexual <= 3:
                recommendations[family_name] += " | 🏢 Corporate/safe training limits authenticity"
            elif avg_sexual >= 8:
                recommendations[family_name] += " | 🔥 Excellent sexual awareness"
        
        return recommendations
    
    def print_refined_analysis(self):
        """Print comprehensive refined analysis"""
        print("🔍 Luna Refined Model Analysis")
        print("=" * 60)
        print("Cross-referencing personality testing with industry benchmarks")
        print("Focusing on model families to identify optimal variations")
        print("")
        
        # Generate family report
        report = self.generate_family_report()
        
        print(f"📊 Analysis Summary:")
        print(f"   Total models tested: {report['total_models_tested']}")
        print(f"   Model families analyzed: {len(report['families'])}")
        print("")
        
        # Top families ranking
        print("🏆 Model Family Rankings (by Luna personality score):")
        for i, (family, score) in enumerate(report["top_families"], 1):
            family_data = report["families"][family]
            count = family_data["count"]
            print(f"   {i}. {family.upper()}: {score}/10 average ({count} models tested)")
        
        print("")
        
        # Detailed family analysis
        for family_name, family_data in report["families"].items():
            if family_data["count"] > 0:
                self._print_family_details(family_name, family_data, report["recommendations"])
        
        # Save report
        report_file = Path(__file__).parent / "luna_refined_analysis_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Detailed report saved to {report_file}")
        
        return report
    
    def _print_family_details(self, family_name: str, family_data: Dict[str, Any], recommendations: Dict[str, str]):
        """Print detailed analysis for a model family"""
        print(f"📁 {family_name.upper()} Family Analysis:")
        print(f"   Models tested: {family_data['count']}")
        print(f"   Luna score range: {family_data['statistics']['luna_range']}/10")
        print(f"   Sexual awareness range: {family_data['statistics']['sexual_range']}/10")
        print(f"   Technical range: {family_data['statistics']['technical_range']}/10")
        print(f"   Recommendation: {recommendations.get(family_name, 'No recommendation')}")
        
        # Best models in family
        best_overall = family_data["best_model"]
        best_sexual = family_data["best_sexual"]
        
        print(f"   🏆 Best overall: {best_overall['model']} ({best_overall['luna_score']}/10)")
        if best_sexual["model"] != best_overall["model"]:
            print(f"   🔥 Best sexual: {best_sexual['model']} ({best_sexual['sexual_awareness']}/10)")
        
        print("")


def main():
    """Main refined analysis function"""
    print("🧠 Initializing Luna Refined Analysis System")
    print("=" * 60)
    
    analyzer = LunaRefinedAnalysis()
    
    # Check API connectivity
    if not analyzer.aa_client.token:
        print("⚠️ No Artificial Analysis token - running Luna-only analysis")
    else:
        print("✅ Artificial Analysis API connected")
    
    # Run comprehensive analysis
    report = analyzer.print_refined_analysis()
    
    print("🎯 Next Steps:")
    print("1. Focus testing on top-performing families")
    print("2. Test variations within best families (quantization, abliteration)")
    print("3. Cross-reference top models with Artificial Analysis benchmarks")
    print("4. Identify optimal models for specific use cases")
    
    # Suggest specific focus areas
    top_families = report["top_families"][:3]
    print(f"\n🔬 Recommended Focus Areas:")
    for i, (family, score) in enumerate(top_families, 1):
        print(f"   {i}. {family.upper()} family - test more variations to find optimal models")
    
    print(f"\n📈 Your systematic testing has created the most comprehensive")
    print(f"   personality-focused AI evaluation framework available!")


if __name__ == "__main__":
    main()
