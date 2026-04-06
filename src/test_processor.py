# tests/test_asset_processor.py
import pytest
from PIL import Image
from io import BytesIO
from pathlib import Path
from src.asset_processor import AssetProcessor

class TestAssetProcessor:
    
    @pytest.fixture
    def sample_image(self):
        """Create a test image"""
        img = Image.new('RGB', (2000, 2000), color='red')
        return img
    
    def test_resize_to_aspect_ratio_square(self, sample_image):
        """Test 1-1 resizing preserves aspect"""
        result = AssetProcessor._resize_to_aspect_ratio(sample_image, 1080, 1080)
        assert result.size == (1080, 1080)
    
    def test_resize_to_aspect_ratio_portrait(self, sample_image):
        """Test 9-16 portrait resizing"""
        result = AssetProcessor._resize_to_aspect_ratio(sample_image, 1080, 1920)
        assert result.size == (1080, 1920)
        # No dimensions should exceed target
        assert result.width <= 1080 and result.height <= 1920
    
    def test_text_overlay_dimensions(self, sample_image):
        """Test text overlay doesn't change dimensions"""
        with_text = AssetProcessor._add_text_overlay(sample_image, "Test Message")
        assert with_text.size == sample_image.size
    
    def test_text_overlay_empty_string(self, sample_image):
        """Test overlay with empty text doesn't error"""
        result = AssetProcessor._add_text_overlay(sample_image, "")
        assert result is not None
    
    @pytest.mark.parametrize("ratio_name", ["1-1", "9-16", "16-9"])
    def test_create_aspect_ratios_all_ratios(self, sample_image, ratio_name, tmp_path):
        """Test all aspect ratios are created"""
        results = AssetProcessor.create_aspect_ratios(
            sample_image,
            "Test",
            tmp_path,
            "test_base"
        )
        assert ratio_name in results
        # Check file exists
        assert Path(results[ratio_name]).exists()

# tests/test_asset_generator.py
from unittest.mock import MagicMock, patch
from src.asset_generator import AssetGenerator

def test_prompt_building_with_message():
    """Test prompt includes campaign message"""
    generator = AssetGenerator.__new__(AssetGenerator)  # Skip __init__
    prompt = generator._build_prompt(
        "Product X",
        "Description Y",
        "Buy Now!",
        "USA",
        "vibrant"
    )
    assert "Buy Now!" in prompt
    assert "Product X" in prompt

def test_prompt_building_without_message():
    """Test prompt excludes text when message is empty"""
    generator = AssetGenerator.__new__(AssetGenerator)
    prompt = generator._build_prompt(
        "Product X",
        "Description Y",
        "",  # Empty campaign message
        "USA",
        None
    )
    assert "NO TEXT" in prompt
    assert "NO WORDS" in prompt

@patch('openai.OpenAI')
def test_generate_image_calls_dalle(mock_openai):
    """Mock DALL-E call"""
    mock_client = MagicMock()
    mock_client.images.generate.return_value.data[0].url = "http://fake-url.com/image.png"
    
    generator = AssetGenerator.__new__(AssetGenerator)
    generator.client = mock_client
    
    url = generator.generate_image("Prod", "Desc", "Msg", "USA")
    
    assert url == "http://fake-url.com/image.png"
    mock_client.images.generate.assert_called_once()