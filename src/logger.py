"""
Logging and reporting utilities
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class PipelineLogger:
    """Logs and reports pipeline execution"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.report: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": None,
            "products_processed": [],
            "assets_generated": [],
            "total_assets": 0,
            "errors": []
        }
    
    def log_campaign_start(self, campaign_id: str, campaign_name: str):
        """Log start of campaign processing"""
        self.report["campaign_id"] = campaign_id
        self.report["campaign_name"] = campaign_name
        print(f"\n{'='*60}")
        print(f"Campaign: {campaign_name} ({campaign_id})")
        print(f"{'='*60}\n")
    
    def log_product_processing(self, product_name: str):
        """Log start of product processing"""
        print(f"Processing product: {product_name}")
    
    def log_asset_created(
        self,
        product_name: str,
        aspect_ratio: str,
        filepath: str,
        source: str = "generated"
    ):
        """Log creation of an asset"""
        self.report["assets_generated"].append({
            "product": product_name,
            "aspect_ratio": aspect_ratio,
            "filepath": filepath,
            "source": source  # "generated" or "reused"
        })
        self.report["total_assets"] += 1
    
    def log_error(self, error_message: str):
        """Log an error"""
        self.report["errors"].append(error_message)
        print(f"❌ ERROR: {error_message}")
    
    def save_report(self):
        """Save report to JSON file"""
        report_path = self.output_dir / "report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        print(f"\n{'='*60}")
        print(f"Report saved: {report_path}")
        print(f"Total assets created: {self.report['total_assets']}")
        print(f"{'='*60}\n")
