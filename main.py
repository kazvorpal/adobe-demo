"""
Creative Automation Pipeline - Main entry point
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

from src.brief_parser import load_brief
from src.asset_generator import AssetGenerator
from src.asset_processor import AssetProcessor
from src.storage import MockStorage
from src.compliance import ComplianceChecker
from src.logger import PipelineLogger


def main():
    """Main pipeline execution"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Creative Automation Pipeline for Social Ad Campaigns"
    )
    parser.add_argument(
        "brief_file",
        help="Path to campaign brief JSON file"
    )
    parser.add_argument(
        "--skip-compliance",
        action="store_true",
        help="Skip Brand/content compliance checks"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize components
        logger = PipelineLogger()
        storage = MockStorage()
        generator = AssetGenerator()
        
        # Load and validate brief
        print("Loading campaign brief...")
        brief = load_brief(args.brief_file)
        
        logger.log_campaign_start(
            brief["campaign_id"],
            brief["campaign_name"]
        )
        
        # Compliance checks (optional)
        if not args.skip_compliance:
            print("Running compliance checks...")
            compliance = ComplianceChecker.check_brand_compliance(brief)
            content_safety = ComplianceChecker.check_content_safety(
                brief["campaign_message"]
            )
            
            if content_safety["flagged_words"]:
                logger.log_error(
                    f"Content safety flagged words: {content_safety['flagged_words']}"
                )
            
            for warning in compliance["warnings"]:
                print(f"⚠️  {warning}")
        
        # Process each product
        output_dir = storage.output_path
        def process(image, brief, existing_asset, text):
            product_dir = output_dir / product_name
            product_dir.mkdir(parents=True, exist_ok=True)
            # Create aspect ratio versions with text overlay
            results = AssetProcessor.create_aspect_ratios(
                image,
                brief["campaign_message"],
                product_dir,
                f"{product_name}_{brief['campaign_id']}_{'text' if text else 'backup'}"
            )
            # Log created assets
            for ratio, filepath in results.items():
                source = "reused" if existing_asset else "generated"
                logger.log_asset_created(
                    product_name,
                    ratio,
                    filepath,
                    source
                )

        for product in brief["products"]:
            product_name = product["name"]
            logger.log_product_processing(product_name)
            
            try:

                # Check for existing asset
                existing_asset = storage.get_existing_asset(product_name)
                images = {
                    'text': None,
                    'backup': None
                }
                
                if existing_asset:
                    print(f"  ✓ Using existing asset: {existing_asset}")
                    images['text'] = AssetProcessor.download_image(f"file://{existing_asset}")
                    process(images['text'], brief, existing_asset, text=True)
                else:
                    # Generate new asset
                    for with_text in [False, True]:
                        image_key = "text" if with_text else "backup"
                        print(f"  Generating new asset...")
                        image_url = generator.generate_image(
                            product_name=product_name,
                            product_description=product.get("description", ""),
                            campaign_message=brief["campaign_message"] if with_text else "",
                            target_region=brief["target_region"],
                            style=product.get("style", None)
                        )
                        
                        # Download image
                        images[image_key] = AssetProcessor.download_image(image_url)
                        process(images[image_key], brief, existing_asset=False, text=with_text)
                
            except Exception as e:
                logger.log_error(f"Failed to process {product_name}: {str(e)}")
                continue
        
        # Save report
        logger.save_report()
        print("✅ Pipeline completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
