"""
Brand compliance and content safety checks
"""

from typing import List, Dict, Any


class ComplianceChecker:
    """Checks for brand compliance and content safety"""
    
    # Words that might violate policies
    PROHIBITED_WORDS = [
        "claim", "guaranteed", "cure", "treatment",
        "banned substance", "illegal"
    ]
    
    @classmethod
    def check_brand_compliance(cls, brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if brief follows brand guidelines
        
        Args:
            brief: Campaign brief dictionary
        
        Returns:
            Dictionary with compliance results
        """
        
        results = {
            "compliant": True,
            "warnings": [],
            "errors": []
        }
        
        # Check for required fields
        if "brand_guidelines" in brief:
            guidelines = brief["brand_guidelines"]
            if guidelines.get("must_include_logo") and not hasattr(brief, "logo"):
                results["warnings"].append("Logo not included (brand requirement)")
        
        return results
    
    @classmethod
    def check_content_safety(cls, text: str) -> Dict[str, Any]:
        """
        Check campaign message for prohibited content
        
        Args:
            text: Campaign message/content
        
        Returns:
            Dictionary with safety check results
        """
        
        results = {
            "safe": True,
            "flagged_words": []
        }
        
        text_lower = text.lower()
        for word in cls.PROHIBITED_WORDS:
            if word in text_lower:
                results["safe"] = False
                results["flagged_words"].append(word)
        
        return results
