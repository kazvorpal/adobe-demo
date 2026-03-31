"""
Parse and validate campaign briefs in JSON format
"""

import json
from typing import Dict, Any
from pathlib import Path


class BriefValidator:
    """Validates campaign brief structure and content"""
    
    REQUIRED_FIELDS = {
        'campaign_id': str,
        'campaign_name': str,
        'target_region': str,
        'target_audience': str,
        'campaign_message': str,
        'products': list,
    }
    
    @classmethod
    def validate(cls, brief: Dict[str, Any]) -> bool:
        """Validate brief has all required fields"""
        for field, expected_type in cls.REQUIRED_FIELDS.items():
            if field not in brief:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(brief[field], expected_type):
                raise TypeError(f"Field '{field}' must be {expected_type.__name__}")
        
        # Validate products
        if len(brief['products']) < 2:
            raise ValueError("Campaign must include at least 2 products")
        
        for product in brief['products']:
            if 'name' not in product or 'description' not in product:
                raise ValueError("Each product must have 'name' and 'description'")
        
        return True


def load_brief(file_path: str) -> Dict[str, Any]:
    """Load and validate campaign brief from JSON file"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Brief file not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        brief = json.load(f)
    
    BriefValidator.validate(brief)
    return brief
