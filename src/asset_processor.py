"""
Process assets: resizing, aspect ratios, text overlays
"""

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from pathlib import Path
from typing import Tuple, Optional


class AssetProcessor:
    """Process and transform images for different aspect ratios"""
    
    # Aspect ratios: (width, height)
    ASPECT_RATIOS = {
        "1-1": (1080, 1080),      # Square
        "9-16": (1080, 1920),     # Portrait (Stories, Reels)
        "16-9": (1920, 1080),     # Landscape (Feed)
    }
    
    @staticmethod
    def download_image(url: str) -> Image.Image:
        """Download image from URL and return PIL Image"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    
    @classmethod
    def create_aspect_ratios(
        cls,
        image: Image.Image,
        text_overlay: str,
        output_dir: Path,
        filename_base: str
    ) -> dict:
        """
        Create versions of image in all required aspect ratios with text overlay
        
        Args:
            image: PIL Image object
            text_overlay: Campaign message to add to image
            output_dir: Directory to save outputs
            filename_base: Base filename (without extension)
        
        Returns:
            Dictionary of created files {aspect_ratio: filepath}
        """
        
        results = {}
        
        for ratio_name, (width, height) in cls.ASPECT_RATIOS.items():
            # Resize image to aspect ratio
            resized = cls._resize_to_aspect_ratio(image, width, height)
            
            # Add text overlay
            with_text = cls._add_text_overlay(resized, text_overlay)
            
            # Save
            output_path = output_dir / ratio_name / f"{filename_base}_{ratio_name}.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with_text.save(output_path, "PNG")
            
            results[ratio_name] = str(output_path)
            print(f"  ✓ Created {ratio_name}: {output_path.name}")
        
        return results
    
    @staticmethod
    def _resize_to_aspect_ratio(
        image: Image.Image,
        target_width: int,
        target_height: int
    ) -> Image.Image:
        """Resize image to target aspect ratio (center crop)"""
        
        img_aspect = image.width / image.height
        target_aspect = target_width / target_height
        
        if img_aspect > target_aspect:
            # Image is wider than target, crop width
            new_width = int(image.height * target_aspect)
            left = (image.width - new_width) // 2
            image = image.crop((left, 0, left + new_width, image.height))
        else:
            # Image is taller than target, crop height
            new_height = int(image.width / target_aspect)
            top = (image.height - new_height) // 2
            image = image.crop((0, top, image.width, top + new_height))
        
        # Resize to exact dimensions
        return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def _add_text_overlay(
        image: Image.Image,
        text: str,
        font_size: int = 60,
        opacity: int = 200
    ) -> Image.Image:
        """Add semi-transparent text overlay to bottom of image"""
        
        # Create a copy with overlay
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Semi-transparent dark background for text
        text_height = font_size + 40
        draw.rectangle(
            [(0, image.height - text_height), (image.width, image.height)],
            fill=(0, 0, 0, int(opacity * 0.8))
        )
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Draw text centered at bottom
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (image.width - text_width) // 2
        text_y = image.height - text_height + 20
        
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
        
        # Composite overlay onto image
        image = image.convert("RGBA")
        image = Image.alpha_composite(image, overlay)
        return image.convert("RGB")
