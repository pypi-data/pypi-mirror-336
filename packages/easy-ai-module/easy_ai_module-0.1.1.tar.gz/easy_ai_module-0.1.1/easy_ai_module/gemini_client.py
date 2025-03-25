import os
import json
import requests
from typing import Dict, List, Optional, Union

class GeminiAI:
    """
    A simple client for making requests to the Google Gemini AI API.
    The API key is hardcoded for personal use only.
    """
    
    # Hardcoded API key (for personal use only)
    API_KEY = "AIzaSyB_gK8LdN9fWPnCY3MzJLLKLRys1bmsBJ8"
    
    # Base URL for the Gemini API
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    
    # Default model to use
    DEFAULT_MODEL = "gemini-2.0-flash"
    
    # Available models
    AVAILABLE_MODELS = {
        "gemini-1.5-flash": "Gemini 1.5 Flash",
        "gemma-3": "Gemma 3",
        "gemini-2.0-flash": "Gemini 2.0 Flash",
        "gemini-2.0-flash-lite": "Gemini 2.0 Flash-Lite"
    }
    
    # Model use cases
    MODEL_USE_CASES = {
        "general": "gemini-2.0-flash",  # Best all-around model
        "speed": "gemini-2.0-flash-lite",  # Fastest model
        "budget": "gemini-2.0-flash-lite",  # Most cost-effective 
        "reasoning": "gemini-2.0-flash",  # Best for complex reasoning
        "local": "gemma-3",  # Can be run locally
        "creative": "gemini-2.0-flash",  # Best for creative content
        "image": "gemini-2.0-flash"  # Best for image analysis
    }
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the Gemini AI client.
        
        Args:
            model: The model name to use. Defaults to gemini-2.0-flash.
                  Available options: gemini-1.5-flash, gemma-3, 
                  gemini-2.0-flash, gemini-2.0-flash-lite
        """
        self.model = model or self.DEFAULT_MODEL
        
        # Validate model name
        if self.model not in self.AVAILABLE_MODELS:
            valid_models = ", ".join(self.AVAILABLE_MODELS.keys())
            raise ValueError(f"Invalid model: {self.model}. Available models are: {valid_models}")
    
    def generate_text(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate text using the Gemini model.
        
        Args:
            prompt: The text prompt to generate from
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more creative, lower = more focused)
            
        Returns:
            The generated text as a string
        """
        url = f"{self.BASE_URL}/models/{self.model}:generateContent?key={self.API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the generated text from the response
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            if "error" in result:
                raise Exception(f"API Error: {result['error'].get('message', 'Unknown error')}")
            raise Exception("Failed to parse API response")
    
    def generate_with_image(self, prompt: str, image_url: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate text based on an image and text prompt.
        
        Args:
            prompt: The text prompt to accompany the image
            image_url: URL of the image to analyze
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            
        Returns:
            The generated text response
        """
        url = f"{self.BASE_URL}/models/{self.model}:generateContent?key={self.API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inlineData": {
                                "mimeType": "image/jpeg",
                                "data": self._get_base64_image(image_url)
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the generated text from the response
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            if "error" in result:
                raise Exception(f"API Error: {result['error'].get('message', 'Unknown error')}")
            raise Exception("Failed to parse API response")
    
    def _get_base64_image(self, image_url: str) -> str:
        """
        Get base64 encoded image data from a URL.
        
        Args:
            image_url: URL of the image
            
        Returns:
            Base64 encoded image data
        """
        import base64
        import requests
        
        response = requests.get(image_url)
        response.raise_for_status()
        
        return base64.b64encode(response.content).decode("utf-8")
    
    @classmethod
    def help(cls, use_case: Optional[str] = None):
        """
        Print help information about available models or recommend a model for a specific use case.
        
        Args:
            use_case: Optional use case to get model recommendation for.
                     If None, shows information about all use cases and models.
        """
        if use_case is not None:
            if use_case in cls.MODEL_USE_CASES:
                recommended_model = cls.MODEL_USE_CASES[use_case]
                print(f"\n🔍 RECOMMENDATION FOR '{use_case.upper()}' USE CASE:")
                print(f"   → Recommended model: {recommended_model}")
                print(f"   → Description: {cls.AVAILABLE_MODELS[recommended_model]}")
                print("\nFor detailed information about this model, use:")
                print(f"   from easy_ai_module import print_model_guide")
                print(f"   print_model_guide('{recommended_model}')")
            else:
                print(f"\n❌ Unknown use case: {use_case}")
                print("Available use cases:", ", ".join(cls.MODEL_USE_CASES.keys()))
        else:
            print("\n🤖 EASY AI MODULE - MODEL RECOMMENDATIONS 🤖\n")
            print("Choose a model based on your specific needs:\n")
            
            for use_case, model in cls.MODEL_USE_CASES.items():
                print(f"• For {use_case}: {model} - {cls.AVAILABLE_MODELS[model]}")
            
            print("\nTo get a detailed guide about all models:")
            print("   from easy_ai_module import print_model_guide")
            print("   print_model_guide()")
            
            print("\nTo see a recommendation for a specific use case:")
            print("   from easy_ai_module import GeminiAI")
            print("   GeminiAI.help('use_case')")
            
            print("\nAvailable use cases:", ", ".join(cls.MODEL_USE_CASES.keys())) 