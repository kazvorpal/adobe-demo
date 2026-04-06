# Creative Automation Pipeline for Social Ad Campaigns

A proof-of-concept creative automation solution that leverages GenAI to generate localized social ad campaign assets at scale.

## Overview

This pipeline automates the creation of social media campaign assets by:
- Accepting campaign briefs with product details and messaging
- Generating or reusing creative assets using OpenAI DALL-E 3
- Creating variants for multiple aspect ratios (1:1, 9:16, 16:9)
- Adding localized campaign messages as text overlays
- Performing brand compliance and content safety checks

Perfect for global brands managing hundreds of localized campaigns across multiple markets.

## Features

✅ **GenAI-powered image generation** - Creates original hero images using DALL-E 3  
✅ **Multi-aspect ratio support** - Generates square (1:1), portrait (9:16), and landscape (16:9) variants  
✅ **Asset reuse** - Checks for existing assets before generating new ones  
✅ **Text overlays** - Adds campaign messages to final images  
✅ **Brand compliance** - Optional checks for brand guidelines and content safety  
✅ **Structured output** - Organizes assets by product and aspect ratio  
✅ **Comprehensive logging** - JSON report of all generated/reused assets  

## Prerequisites

- Python 3.8+
- OpenAI API key (for DALL-E 3 image generation)
- ~$1-2 budget for image generation (~20-30 images)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/adobe-demo.git
   cd adobe-demo
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```
   On Windows (PowerShell):
   ```powershell
   $env:OPENAI_API_KEY="sk-your-key-here"
   ```

## Usage

### Basic Usage

```bash
python main.py campaign_brief.json
```

### With Compliance Checks Disabled

```bash
python main.py campaign_brief.json --skip-compliance
```

### Example Campaign Brief

See `campaign_brief.json` for a complete example. Minimum required fields:

```json
{
  "campaign_id": "SUMMER_24_LATAM",
  "campaign_name": "Summer Campaign - LATAM",
  "target_region": "Brazil",
  "target_audience": "18-35, urban, mobile-first",
  "campaign_message": "Your campaign tagline here",
  "products": [
    {
      "name": "Product_Name",
      "description": "What is this product?",
      "style": "visual style guidance (optional)"
    }
  ]
}
```

## Output Structure

```
output/
├── SportDrink_Blue/
│   ├── 1-1/
│   │   └── SportDrink_Blue_1-1_SUMMER_24_LATAM.png
│   ├── 9-16/
│   │   └── SportDrink_Blue_9-16_SUMMER_24_LATAM.png
│   └── 16-9/
│       └── SportDrink_Blue_16-9_SUMMER_24_LATAM.png
├── Snack_Energy_Bar/
│   ├── 1-1/
│   ├── 9-16/
│   └── 16-9/
└── report.json  # Execution summary
```

## Architecture & Design Decisions

### Modular Design
- **brief_parser.py** - Validates campaign briefs against required schema
- **asset_generator.py** - Interfaces with OpenAI DALL-E 3 for image generation
- **asset_processor.py** - Handles image resizing, aspect ratio conversion, and text overlays
- **storage.py** - Mock storage layer for managing local assets
- **compliance.py** - Brand compliance and content safety checks
- **logger.py** - Structured logging and JSON reporting

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| GenAI Provider | OpenAI DALL-E 3 | Easiest API, good quality, fastest iteration |
| Image Format | PNG | Lossless quality for professional ads (JPG used for size optimization) |
| Text Overlay | PIL/Pillow | Simple, no external dependencies, sufficient for MVP |
| Storage | Local folders | Fast, works offline, good for proof-of-concept |
| Aspect Ratios | 1:1, 9:16, 16:9 | Covers major social platforms (Instagram, TikTok, YouTube) |

### Scalability Considerations

For production scaling:
- **Batch processing** - Process multiple briefs in parallel
- **Cloud storage** - Replace local storage with Azure Blob Storage or AWS S3
- **Caching** - Avoid regenerating identical assets
- **API optimization** - Use batch APIs for faster image generation
- **Queue system** - Async task queue for long-running generations

## Assumptions & Limitations

### Assumptions
- Campaign briefs are in valid JSON format
- OpenAI API is accessible (rate limits may apply)
- Generated images will be approved by brand teams (no automated approval endpoint)
- Text overlay font preference is default/system font

### Limitations
- Single-image generation per product (could enhance with multiple variations)
- Text overlay positioning is bottom-center (could be customized)
- No automatic brand logo insertion (manual requirement)
- Compliance checks are basic (production would need more sophisticated checks)
- The most important check might be to generate a description of the image and check it to see if any generated text matches, optionally re-running...this could even be passed to an LLM to judge.
- No support for dynamic content personalization beyond text overlay

## Example Run

```bash
$ python main.py campaign_brief.json

============================================================
Campaign: Summer Campaign - LATAM (SUMMER_24_LATAM)
============================================================

Loading campaign brief...
Running compliance checks...
Processing product: SportDrink_Blue
  Generating new asset...
  [DEBUG] Generating image for SportDrink_Blue...
  [DEBUG] Image generated: https://oaidalleapiprodw...
  ✓ Created 1-1: SportDrink_Blue_1-1_SUMMER_24_LATAM.png
  ✓ Created 9-16: SportDrink_Blue_9-16_SUMMER_24_LATAM.png
  ✓ Created 16-9: SportDrink_Blue_16-9_SUMMER_24_LATAM.png
Processing product: Snack_Energy_Bar
  Generating new asset...
  ✓ Created 1-1: Snack_Energy_Bar_1-1_SUMMER_24_LATAM.png
  ✓ Created 9-16: Snack_Energy_Bar_9-16_SUMMER_24_LATAM.png
  ✓ Created 16-9: Snack_Energy_Bar_16-9_SUMMER_24_LATAM.png

============================================================
Report saved: ./output/report.json
Total assets created: 6
============================================================

✅ Pipeline completed successfully!
```

## Testing

Example test data is included in `campaign_brief.json`. To test:

```bash
python main.py campaign_brief.json
ls -la output/  # View generated assets
cat output/report.json  # View execution report
```

## Cost Estimation

- DALL-E 3: $0.04 per 1024x1024 image (or $0.02 for smaller)
- Example campaign (2 products × 3 ratios = 6 total images): ~$0.24
- Full campaign suite (50 campaigns): ~$12

## Future Enhancements

- [ ] Generative check of image by image generator in tandem with LLM
- [ ] Support for video asset generation
- [ ] Integration with brand DAM systems
- [ ] Advanced content personalization (dynamic text, faces, etc.)
- [ ] A/B testing variant generation
- [ ] Performance analytics integration
- [ ] Web UI for campaign management
- [ ] Multi-language support for localization

## Troubleshooting

**"OPENAI_API_KEY not set"**
```bash
# Make sure your API key is exported:
export OPENAI_API_KEY="sk-..."
# Verify:
echo $OPENAI_API_KEY
```

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
```

**"Image generation failed"**
- Check OpenAI API account status and rate limits
- Verify API key is valid and has sufficient credits
- Check internet connectivity

## Contributing

Contributions welcome! Please create a branch and submit a PR.

## License

This project is provided as-is for the Adobe FDE take-home exercise.

## Contact

For questions, reach out to your Adobe Talent Partner.
