"""
Model guide for the Easy AI Module - provides information about model capabilities and best use cases.
"""

MODEL_GUIDE = {
    "gemini-2.0-flash": {
        "description": "Most capable multi-modal model with great performance across all tasks",
        "context_window": "1 million tokens",
        "strengths": [
            "Great general-purpose model",
            "Strong reasoning abilities",
            "Can handle text, image, video, and audio inputs",
            "High-quality text generation",
            "Best for most everyday tasks"
        ],
        "best_for": [
            "Content generation",
            "Summarization",
            "Complex reasoning",
            "Multi-modal tasks (text + images)",
            "Building AI agents"
        ],
        "limitations": [
            "More expensive than Flash-Lite",
            "Slower than Flash-Lite for simple tasks"
        ],
        "pricing": {
            "input": "$0.10 per 1M tokens (text/image/video), $0.70 per 1M tokens (audio)",
            "output": "$0.40 per 1M tokens"
        }
    },
    "gemini-2.0-flash-lite": {
        "description": "Smallest and most cost-effective model, built for at-scale usage",
        "context_window": "1 million tokens",
        "strengths": [
            "Fast response times",
            "Cost-effective",
            "Good for high-volume applications",
            "Decent performance on straightforward tasks"
        ],
        "best_for": [
            "Simple Q&A",
            "Classification",
            "High-volume applications",
            "Applications with cost constraints",
            "When speed is more important than quality"
        ],
        "limitations": [
            "Lower reasoning capabilities than larger models",
            "Less creative output",
            "May struggle with complex or nuanced prompts"
        ],
        "pricing": {
            "input": "$0.075 per 1M tokens",
            "output": "$0.30 per 1M tokens"
        }
    },
    "gemini-1.5-flash": {
        "description": "Fastest Gemini 1.5 multi-modal model for diverse, repetitive tasks",
        "context_window": "1 million tokens",
        "strengths": [
            "Fast performance",
            "Good balance of quality and speed",
            "Multi-modal capabilities",
            "Great for production applications"
        ],
        "best_for": [
            "General purpose text generation",
            "When response speed matters",
            "Moderate complexity tasks",
            "Applications requiring decent performance at scale"
        ],
        "limitations": [
            "Not as advanced as Gemini 2.0 models",
            "Less creative than larger models"
        ],
        "pricing": {
            "input": "$0.075 per 1M tokens (≤128k tokens), $0.15 (>128k tokens)",
            "output": "$0.30 per 1M tokens (≤128k tokens), $0.60 (>128k tokens)"
        }
    },
    "gemma-3": {
        "description": "Lightweight, state-of-the-art open model built from Gemini technology",
        "context_window": "Unknown",
        "strengths": [
            "Open source",
            "Can be run locally",
            "Free to use",
            "Built from same technology as Gemini"
        ],
        "best_for": [
            "Local deployment",
            "Custom fine-tuning",
            "Privacy-sensitive applications",
            "Educational and research purposes"
        ],
        "limitations": [
            "Performance typically lower than cloud-hosted models",
            "Requires proper hardware for good performance"
        ],
        "pricing": {
            "input": "Free of charge",
            "output": "Free of charge"
        }
    }
}

def get_model_info(model_name=None):
    """
    Get information about a specific model or all models.
    
    Args:
        model_name: Optional name of model to get info for
                   If None, returns info for all models
    
    Returns:
        Dict containing model information
    """
    if model_name is not None:
        if model_name in MODEL_GUIDE:
            return MODEL_GUIDE[model_name]
        else:
            raise ValueError(f"Unknown model: {model_name}")
    return MODEL_GUIDE

def print_model_guide(model_name=None):
    """
    Print a formatted guide for a specific model or all models.
    
    Args:
        model_name: Optional name of model to print info for
                   If None, prints info for all models
    """
    if model_name is not None:
        if model_name not in MODEL_GUIDE:
            print(f"Unknown model: {model_name}")
            return
        
        models_to_show = {model_name: MODEL_GUIDE[model_name]}
    else:
        models_to_show = MODEL_GUIDE
    
    print("\n📚 GEMINI MODEL GUIDE 📚\n")
    
    for name, info in models_to_show.items():
        print(f"🤖 {name.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Context window: {info['context_window']}")
        
        print("\n   ✅ STRENGTHS:")
        for strength in info['strengths']:
            print(f"      • {strength}")
        
        print("\n   🎯 BEST FOR:")
        for use_case in info['best_for']:
            print(f"      • {use_case}")
        
        print("\n   ⚠️ LIMITATIONS:")
        for limitation in info['limitations']:
            print(f"      • {limitation}")
        
        print("\n   💰 PRICING:")
        print(f"      • Input: {info['pricing']['input']}")
        print(f"      • Output: {info['pricing']['output']}")
        
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gemini Model Guide")
    parser.add_argument("--model", "-m", type=str, help="Specific model to show information for")
    args = parser.parse_args()
    
    print_model_guide(args.model) 