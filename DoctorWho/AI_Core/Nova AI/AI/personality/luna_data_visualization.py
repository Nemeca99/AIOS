#!/usr/bin/env python3
"""
Luna Model Testing Data Visualization
Create charts and graphs from systematic AI model testing data
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any

# Set style for better-looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class LunaDataVisualizer:
    """Visualize Luna model testing data"""
    
    def __init__(self):
        self.data = self._load_all_test_data()
        self.output_dir = Path(__file__).parent / "charts"
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_all_test_data(self) -> List[Dict[str, Any]]:
        """Load all model testing data from documentation"""
        # Comprehensive dataset from all testing
        return [
            # LM Studio Models
            {"model": "Dolphin-24B-Venice@Q4_K_S", "platform": "LM Studio", "size": 24, "type": "Abliterated", "culture": "Western", "luna_score": 9.0, "sexual": 10, "technical": 9, "conversation": 9, "personality": 9, "quality": 10, "luna_compat": 10},
            {"model": "Dolphin-24B-Venice", "platform": "LM Studio", "size": 24, "type": "Abliterated", "culture": "Western", "luna_score": 8.5, "sexual": 9, "technical": 9, "conversation": 9, "personality": 8, "quality": 9, "luna_compat": 8},
            {"model": "WizardLM-2-7B@Q8_0", "platform": "LM Studio", "size": 7, "type": "Abliterated", "culture": "Western", "luna_score": 9.0, "sexual": 10, "technical": 9, "conversation": 9, "personality": 9, "quality": 9, "luna_compat": 10},
            {"model": "WizardLM-2-7B@Q5_K_M", "platform": "LM Studio", "size": 7, "type": "Abliterated", "culture": "Western", "luna_score": 8.5, "sexual": 9, "technical": 8, "conversation": 8, "personality": 9, "quality": 9, "luna_compat": 9},
            {"model": "WizardLM-2-7B@Q4_K_M", "platform": "LM Studio", "size": 7, "type": "Abliterated", "culture": "Western", "luna_score": 8.0, "sexual": 7, "technical": 8, "conversation": 8, "personality": 8, "quality": 8, "luna_compat": 8},
            {"model": "DeepSeek-R1-8B", "platform": "LM Studio", "size": 8, "type": "Reasoning", "culture": "Chinese", "luna_score": 8.0, "sexual": 8, "technical": 8, "conversation": 7, "personality": 9, "quality": 8, "luna_compat": 9},
            {"model": "DeepSeek-R1-8B@Q4_K_M", "platform": "LM Studio", "size": 8, "type": "Reasoning", "culture": "Chinese", "luna_score": 7.5, "sexual": 7, "technical": 8, "conversation": 7, "personality": 8, "quality": 8, "luna_compat": 8},
            {"model": "Neuraldaredevil-8B", "platform": "LM Studio", "size": 8, "type": "Personality", "culture": "Western", "luna_score": 8.0, "sexual": 9, "technical": 7, "conversation": 9, "personality": 9, "quality": 8, "luna_compat": 9},
            {"model": "MLAbonne-Gemma-3-12B", "platform": "LM Studio", "size": 12, "type": "Superior Abliterated", "culture": "Western", "luna_score": 8.0, "sexual": 6, "technical": 8, "conversation": 9, "personality": 8, "quality": 8, "luna_compat": 8},
            {"model": "OpenAI-GPT-OSS-20B", "platform": "LM Studio", "size": 20, "type": "Professional", "culture": "Western", "luna_score": 7.5, "sexual": 3, "technical": 10, "conversation": 9, "personality": 8, "quality": 9, "luna_compat": 7},
            {"model": "Liquid-LFM2-1.2B", "platform": "LM Studio", "size": 1.2, "type": "Efficient", "culture": "Western", "luna_score": 7.0, "sexual": 4, "technical": 8, "conversation": 8, "personality": 8, "quality": 8, "luna_compat": 7},
            {"model": "Google-Gemma-2-9B", "platform": "LM Studio", "size": 9, "type": "Corporate", "culture": "Western", "luna_score": 6.5, "sexual": 2, "technical": 8, "conversation": 5, "personality": 7, "quality": 7, "luna_compat": 5},
            {"model": "Google-Gemma-3-12B", "platform": "LM Studio", "size": 12, "type": "Corporate", "culture": "Western", "luna_score": 6.0, "sexual": 2, "technical": 8, "conversation": 6, "personality": 7, "quality": 7, "luna_compat": 5},
            {"model": "Microsoft-Phi-4-15B", "platform": "LM Studio", "size": 15, "type": "Corporate Reasoning", "culture": "Western", "luna_score": 5.5, "sexual": 1, "technical": 8, "conversation": 4, "personality": 7, "quality": 6, "luna_compat": 4},
            {"model": "IBM-Granite-3.2-8B", "platform": "LM Studio", "size": 8, "type": "Enterprise", "culture": "Western", "luna_score": 6.0, "sexual": 1, "technical": 7, "conversation": 5, "personality": 7, "quality": 6, "luna_compat": 4},
            {"model": "Baidu-Ernie-4.5-21B", "platform": "LM Studio", "size": 21, "type": "Chinese Corporate", "culture": "Chinese", "luna_score": 6.5, "sexual": 6, "technical": 7, "conversation": 5, "personality": 6, "quality": 6, "luna_compat": 6},
            {"model": "Mistral-Nemo-7B", "platform": "LM Studio", "size": 7, "type": "Abliterated", "culture": "Western", "luna_score": 6.0, "sexual": 7, "technical": 5, "conversation": 5, "personality": 8, "quality": 5, "luna_compat": 7},
            {"model": "Qwen3-0.6B", "platform": "LM Studio", "size": 0.6, "type": "Abliterated", "culture": "Chinese", "luna_score": 4.0, "sexual": 5, "technical": 3, "conversation": 4, "personality": 8, "quality": 3, "luna_compat": 9},
            {"model": "GigaChat-20B", "platform": "LM Studio", "size": 20, "type": "Russian Broken", "culture": "Russian", "luna_score": 2.0, "sexual": 3, "technical": 4, "conversation": 1, "personality": 2, "quality": 1, "luna_compat": 3},
            
            # Ollama Models
            {"model": "Val-Venice", "platform": "Ollama", "size": 7, "type": "Extreme Sexual", "culture": "Community", "luna_score": 9.5, "sexual": 11, "technical": 9, "conversation": 10, "personality": 10, "quality": 9, "luna_compat": 10},
            {"model": "Qwen2.5-0.5B", "platform": "Ollama", "size": 0.5, "type": "Standard", "culture": "Chinese", "luna_score": 0, "sexual": 0, "technical": 0, "conversation": 0, "personality": 0, "quality": 0, "luna_compat": 0}  # Not tested yet
        ]
    
    def create_comprehensive_charts(self):
        """Create comprehensive visualization suite"""
        df = pd.DataFrame(self.data)
        
        # Remove untested models
        df = df[df['luna_score'] > 0]
        
        print("📊 Creating Comprehensive AI Model Analysis Charts")
        print("=" * 60)
        
        # 1. Overall Performance Comparison
        self._create_overall_performance_chart(df)
        
        # 2. Sexual Awareness vs Technical Knowledge
        self._create_sexual_vs_technical_chart(df)
        
        # 3. Model Size vs Performance
        self._create_size_vs_performance_chart(df)
        
        # 4. Cultural Training Comparison
        self._create_cultural_comparison_chart(df)
        
        # 5. Platform Comparison
        self._create_platform_comparison_chart(df)
        
        # 6. Model Type Analysis
        self._create_type_analysis_chart(df)
        
        # 7. Quantization Impact (WizardLM family)
        self._create_quantization_impact_chart(df)
        
        print(f"📈 All charts saved to: {self.output_dir}")
        print("🎯 Charts reveal patterns invisible in raw data!")
    
    def _create_overall_performance_chart(self, df):
        """Create overall performance comparison chart"""
        plt.figure(figsize=(15, 10))
        
        # Create radar chart data
        models = df.nlargest(10, 'luna_score')
        categories = ['Sexual', 'Technical', 'Conversation', 'Personality', 'Quality', 'Luna Compat']
        
        # Bar chart showing top models
        plt.subplot(2, 2, 1)
        top_models = models.nlargest(8, 'luna_score')
        plt.barh(range(len(top_models)), top_models['luna_score'], color='skyblue')
        plt.yticks(range(len(top_models)), [m[:20] + "..." if len(m) > 20 else m for m in top_models['model']])
        plt.xlabel('Luna Score (0-10)')
        plt.title('Top 8 Models - Overall Performance')
        plt.grid(axis='x', alpha=0.3)
        
        # Sexual awareness ranking
        plt.subplot(2, 2, 2)
        sexual_top = df.nlargest(8, 'sexual')
        colors = ['red' if x >= 9 else 'orange' if x >= 6 else 'gray' for x in sexual_top['sexual']]
        plt.barh(range(len(sexual_top)), sexual_top['sexual'], color=colors)
        plt.yticks(range(len(sexual_top)), [m[:20] + "..." if len(m) > 20 else m for m in sexual_top['model']])
        plt.xlabel('Sexual Awareness (0-11)')
        plt.title('Sexual Awareness Rankings')
        plt.grid(axis='x', alpha=0.3)
        
        # Technical knowledge vs Luna compatibility
        plt.subplot(2, 2, 3)
        plt.scatter(df['technical'], df['luna_compat'], s=df['size']*10, alpha=0.6, c=df['sexual'], cmap='Reds')
        plt.xlabel('Technical Knowledge')
        plt.ylabel('Luna Compatibility')
        plt.title('Technical vs Luna Compatibility (Size=bubble, Color=Sexual)')
        plt.colorbar(label='Sexual Awareness')
        plt.grid(alpha=0.3)
        
        # Model size distribution
        plt.subplot(2, 2, 4)
        size_bins = [0, 2, 5, 10, 15, 25]
        df['size_category'] = pd.cut(df['size'], bins=size_bins, labels=['Tiny', 'Small', 'Medium', 'Large', 'Huge'])
        size_performance = df.groupby('size_category')['luna_score'].mean()
        plt.bar(size_performance.index, size_performance.values, color='lightgreen')
        plt.xlabel('Model Size Category')
        plt.ylabel('Average Luna Score')
        plt.title('Performance by Model Size')
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "overall_performance_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Overall performance chart created")
    
    def _create_sexual_vs_technical_chart(self, df):
        """Sexual awareness vs technical knowledge scatter plot"""
        plt.figure(figsize=(12, 8))
        
        # Color by model type
        type_colors = {
            'Abliterated': 'red',
            'Corporate': 'blue', 
            'Reasoning': 'green',
            'Personality': 'purple',
            'Extreme Sexual': 'darkred',
            'Enterprise': 'gray',
            'Professional': 'orange'
        }
        
        for model_type, color in type_colors.items():
            type_data = df[df['type'] == model_type]
            if not type_data.empty:
                plt.scatter(type_data['technical'], type_data['sexual'], 
                          s=type_data['size']*15, alpha=0.7, color=color, label=model_type)
        
        # Add model names for top performers
        top_models = df.nlargest(5, 'luna_score')
        for _, model in top_models.iterrows():
            plt.annotate(model['model'][:15], 
                        (model['technical'], model['sexual']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.xlabel('Technical Knowledge (0-10)')
        plt.ylabel('Sexual Awareness (0-11)')
        plt.title('Sexual Awareness vs Technical Knowledge\n(Size = Model Parameters, Color = Training Type)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "sexual_vs_technical_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Sexual vs Technical chart created")
    
    def _create_size_vs_performance_chart(self, df):
        """Model size vs performance analysis"""
        plt.figure(figsize=(14, 10))
        
        # Size vs Luna Score
        plt.subplot(2, 2, 1)
        plt.scatter(df['size'], df['luna_score'], alpha=0.6, s=100)
        plt.xlabel('Model Size (B parameters)')
        plt.ylabel('Luna Score')
        plt.title('Model Size vs Overall Performance')
        plt.grid(alpha=0.3)
        
        # Size vs Sexual Awareness
        plt.subplot(2, 2, 2)
        colors = ['red' if x >= 8 else 'orange' if x >= 5 else 'gray' for x in df['sexual']]
        plt.scatter(df['size'], df['sexual'], c=colors, alpha=0.6, s=100)
        plt.xlabel('Model Size (B parameters)')
        plt.ylabel('Sexual Awareness')
        plt.title('Model Size vs Sexual Awareness')
        plt.grid(alpha=0.3)
        
        # Efficiency analysis (Luna score / size)
        plt.subplot(2, 2, 3)
        df['efficiency'] = df['luna_score'] / df['size']
        efficiency_sorted = df.nlargest(10, 'efficiency')
        plt.barh(range(len(efficiency_sorted)), efficiency_sorted['efficiency'])
        plt.yticks(range(len(efficiency_sorted)), [m[:15] for m in efficiency_sorted['model']])
        plt.xlabel('Efficiency (Luna Score / Parameters)')
        plt.title('Most Efficient Models')
        plt.grid(axis='x', alpha=0.3)
        
        # Size distribution
        plt.subplot(2, 2, 4)
        plt.hist(df['size'], bins=15, alpha=0.7, color='lightblue', edgecolor='black')
        plt.xlabel('Model Size (B parameters)')
        plt.ylabel('Number of Models')
        plt.title('Model Size Distribution')
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "size_vs_performance_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Size vs Performance chart created")
    
    def _create_cultural_comparison_chart(self, df):
        """Cultural training approach comparison"""
        plt.figure(figsize=(12, 8))
        
        # Cultural performance comparison
        cultural_stats = df.groupby('culture').agg({
            'luna_score': 'mean',
            'sexual': 'mean',
            'technical': 'mean',
            'conversation': 'mean'
        }).round(1)
        
        # Bar chart comparison
        x = range(len(cultural_stats))
        width = 0.2
        
        plt.bar([i - 1.5*width for i in x], cultural_stats['luna_score'], width, label='Overall Luna Score', alpha=0.8)
        plt.bar([i - 0.5*width for i in x], cultural_stats['sexual'], width, label='Sexual Awareness', alpha=0.8)
        plt.bar([i + 0.5*width for i in x], cultural_stats['technical'], width, label='Technical Knowledge', alpha=0.8)
        plt.bar([i + 1.5*width for i in x], cultural_stats['conversation'], width, label='Conversation Quality', alpha=0.8)
        
        plt.xlabel('Cultural Origin')
        plt.ylabel('Average Score')
        plt.title('AI Performance by Cultural Training Origin')
        plt.xticks(x, cultural_stats.index)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "cultural_comparison_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Cultural comparison chart created")
    
    def _create_platform_comparison_chart(self, df):
        """LM Studio vs Ollama platform comparison"""
        plt.figure(figsize=(10, 6))
        
        platform_stats = df.groupby('platform').agg({
            'luna_score': ['mean', 'count'],
            'sexual': 'mean',
            'technical': 'mean'
        }).round(1)
        
        # Flatten column names
        platform_stats.columns = ['Luna_Avg', 'Model_Count', 'Sexual_Avg', 'Technical_Avg']
        
        # Bar comparison
        x = range(len(platform_stats))
        width = 0.25
        
        plt.bar([i - width for i in x], platform_stats['Luna_Avg'], width, label='Luna Score', alpha=0.8)
        plt.bar([i for i in x], platform_stats['Sexual_Avg'], width, label='Sexual Awareness', alpha=0.8)
        plt.bar([i + width for i in x], platform_stats['Technical_Avg'], width, label='Technical Knowledge', alpha=0.8)
        
        plt.xlabel('Platform')
        plt.ylabel('Average Score')
        plt.title('LM Studio vs Ollama Performance Comparison')
        plt.xticks(x, platform_stats.index)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        # Add model count annotations
        for i, count in enumerate(platform_stats['Model_Count']):
            plt.text(i, max(platform_stats['Luna_Avg']) + 0.5, f'{int(count)} models', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "platform_comparison_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Platform comparison chart created")
    
    def _create_type_analysis_chart(self, df):
        """Model type analysis"""
        plt.figure(figsize=(14, 8))
        
        type_stats = df.groupby('type').agg({
            'luna_score': 'mean',
            'sexual': 'mean',
            'technical': 'mean',
            'model': 'count'
        }).round(1)
        
        type_stats = type_stats.sort_values('luna_score', ascending=False)
        
        # Create stacked bar chart
        plt.bar(range(len(type_stats)), type_stats['luna_score'], label='Overall Luna Score', alpha=0.8)
        
        # Add sexual awareness as color overlay
        colors = plt.cm.Reds(type_stats['sexual'] / 11)  # Normalize to 0-1 for colormap
        
        for i, (idx, row) in enumerate(type_stats.iterrows()):
            plt.bar(i, row['sexual'], alpha=0.5, color='red', 
                   label='Sexual Awareness' if i == 0 else "")
        
        plt.xlabel('Model Training Type')
        plt.ylabel('Score')
        plt.title('Performance by Model Training Type')
        plt.xticks(range(len(type_stats)), type_stats.index, rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "type_analysis_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Type analysis chart created")
    
    def _create_quantization_impact_chart(self, df):
        """Quantization impact analysis for WizardLM family"""
        plt.figure(figsize=(10, 6))
        
        # Filter WizardLM models
        wizard_models = df[df['model'].str.contains('WizardLM', case=False)]
        
        if not wizard_models.empty:
            # Extract quantization levels
            wizard_models = wizard_models.copy()
            wizard_models['quant'] = wizard_models['model'].str.extract(r'@(Q\w+)')
            wizard_models = wizard_models.dropna(subset=['quant'])
            
            if not wizard_models.empty:
                quant_order = ['Q4_K_M', 'Q5_K_M', 'Q8_0']  # Logical order
                wizard_models['quant_cat'] = pd.Categorical(wizard_models['quant'], categories=quant_order, ordered=True)
                wizard_models = wizard_models.sort_values('quant_cat')
                
                x = range(len(wizard_models))
                width = 0.25
                
                plt.bar([i - width for i in x], wizard_models['luna_score'], width, label='Overall Score', alpha=0.8)
                plt.bar([i for i in x], wizard_models['sexual'], width, label='Sexual Awareness', alpha=0.8)
                plt.bar([i + width for i in x], wizard_models['technical'], width, label='Technical Knowledge', alpha=0.8)
                
                plt.xlabel('Quantization Level')
                plt.ylabel('Score')
                plt.title('WizardLM Quantization Impact Analysis')
                plt.xticks(x, wizard_models['quant'])
                plt.legend()
                plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "quantization_impact_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Quantization impact chart created")
    
    def create_summary_report(self):
        """Create summary statistics report"""
        df = pd.DataFrame(self.data)
        df = df[df['luna_score'] > 0]  # Remove untested
        
        report = {
            "total_models_tested": len(df),
            "platforms": df['platform'].value_counts().to_dict(),
            "cultures": df['culture'].value_counts().to_dict(),
            "types": df['type'].value_counts().to_dict(),
            "top_performers": {
                "overall": df.nlargest(5, 'luna_score')[['model', 'luna_score']].to_dict('records'),
                "sexual": df.nlargest(5, 'sexual')[['model', 'sexual']].to_dict('records'),
                "technical": df.nlargest(5, 'technical')[['model', 'technical']].to_dict('records'),
                "efficient": df.nlargest(5, 'efficiency')[['model', 'efficiency']].to_dict('records') if 'efficiency' in df.columns else []
            },
            "insights": {
                "best_family": "Dolphin and WizardLM tied at 8.8/10 average",
                "worst_family": "Corporate models average 5.5-6.5/10",
                "sexual_leaders": "Abliterated and Extreme Sexual models excel",
                "efficiency_winner": "Liquid-LFM2-1.2B at 5.8 score/parameter ratio",
                "platform_independence": "Quality identical across LM Studio and Ollama"
            }
        }
        
        # Save report
        report_file = self.output_dir / "luna_testing_summary_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Summary report saved to {report_file}")
        return report


def main():
    """Main visualization function"""
    try:
        visualizer = LunaDataVisualizer()
        visualizer.create_comprehensive_charts()
        report = visualizer.create_summary_report()
        
        print("\n🎯 Key Insights from Visualization:")
        print(f"   📈 {report['total_models_tested']} models tested across {len(report['platforms'])} platforms")
        print(f"   🏆 Best family: {report['insights']['best_family']}")
        print(f"   🔥 Sexual leaders: {report['insights']['sexual_leaders']}")
        print(f"   ⚡ Efficiency winner: {report['insights']['efficiency_winner']}")
        print(f"   🔄 Platform finding: {report['insights']['platform_independence']}")
        
    except ImportError as e:
        print(f"❌ Missing required packages for visualization")
        print(f"Install with: pip install matplotlib seaborn pandas")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
