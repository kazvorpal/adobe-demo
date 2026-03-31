"""
Mock storage for managing input and output assets
"""

from pathlib import Path
from typing import Optional


class MockStorage:
    """Manages local storage for input/output assets"""
    
    def __init__(self, base_path: str = "./assets"):
        self.base_path = Path(base_path)
        self.input_path = self.base_path / "input"
        self.output_path = Path("./output")
        
        # Ensure directories exist
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def get_existing_asset(
        self,
        product_name: str,
        asset_type: str = "image"
    ) -> Optional[str]:
        """
        Check if an asset already exists locally
        
        Args:
            product_name: Name of the product
            asset_type: Type of asset (image, etc.)
        
        Returns:
            Path to existing asset or None if not found
        """
        
        # Look for PNG or JPG files matching product name
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            matches = list(self.input_path.glob(f"*{product_name}*{ext}"))
            if matches:
                return str(matches[0])
        
        return None
    
    def save_asset(
        self,
        data: bytes,
        product_name: str,
        aspect_ratio: str,
        campaign_id: str
    ) -> str:
        """
        Save downloaded asset locally
        
        Args:
            data: Binary image data
            product_name: Product name
            aspect_ratio: Aspect ratio identifier
            campaign_id: Campaign identifier
        
        Returns:
            Path where asset was saved
        """
        
        # Create product-specific directory
        product_dir = self.output_path / product_name / aspect_ratio
        product_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{product_name}_{aspect_ratio}_{campaign_id}.png"
        filepath = product_dir / filename
        
        with open(filepath, "wb") as f:
            f.write(data)
        
        return str(filepath)
    
    def get_output_path(self) -> Path:
        """Get the output directory path"""
        return self.output_path
