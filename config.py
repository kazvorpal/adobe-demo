"""
Configuration and constants
"""

import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "dall-e-3"

# Asset Configuration
ASPECT_RATIOS = {
    "1-1": (1080, 1080),      # Square
    "9-16": (1080, 1920),     # Portrait
    "16-9": (1920, 1080),     # Landscape
}

# Storage Configuration
INPUT_ASSET_PATH = "./assets/input"
OUTPUT_ASSET_PATH = "./output"

# Compliance
ENABLE_COMPLIANCE_CHECKS = True
ENABLE_CONTENT_SAFETY = True
