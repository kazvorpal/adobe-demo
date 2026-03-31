"""
Generate creative assets using GenAI (OpenAI DALL-E)
"""

import os
from typing import Optional
from openai import OpenAI


class AssetGenerator:
    """Generates images using OpenAI DALL-E 3"""
    
    def __init__(self):
        """Initialize OpenAI client with API key from environment"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
    
    def generate_image(
        self, 
        product_name: str,
        product_description: str,
        campaign_message: str,
        target_region: str,
        style: Optional[str] = None
    ) -> str:
        """
        Generate an image for a product using DALL-E 3
        
        Args:
            product_name: Name of the product
            product_description: Description of the product
            campaign_message: Campaign message/tagline
            target_region: Target region for cultural relevance
            style: Style/mood for the image
        
        Returns:
            URL of generated image
        """
        
        prompt = self._build_prompt(
            product_name,
            product_description,
            campaign_message,
            target_region,
            style
        )
        
        print(f"[DEBUG] Generating image for {product_name}...")
        print(f"[DEBUG] Prompt: {prompt[:100]}...")
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"[DEBUG] Image generated: {image_url[:50]}...")
        return image_url
    
    def _build_prompt(
        self,
        product_name: str,
        product_description: str,
        campaign_message: str,
        target_region: str,
        style: Optional[str] = None
    ) -> str:
        """Build optimized prompt for DALL-E 3"""
        
        prompt = f"""
        Create a vibrant, professional social media advertising image for:
        
        Product: {product_name}
        Description: {product_description}
        Campaign Message: {campaign_message}
        Target Region: {target_region}
        {f'Style: {style}' if style else ''}
        
        Requirements:
        - Modern, professional design
        - Culturally relevant to {target_region}
        - High contrast, eye-catching colors
        - Suitable for social media ads
        - Professional quality suitable for global brand
        """
        
        return prompt.strip()
