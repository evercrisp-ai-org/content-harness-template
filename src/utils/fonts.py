"""
Font Utilities

Handles font loading, caching, and fallback management.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple, Any


class FontManager:
    """
    Manages font loading and caching for the template system.
    
    Handles:
    - Loading fonts from the brand/fonts directory
    - Providing fallbacks for missing fonts
    - Caching loaded fonts for performance
    """
    
    # Standard fallback fonts by platform
    FALLBACKS = {
        "serif": ["Times New Roman", "Georgia", "Times", "serif"],
        "sans-serif": ["Helvetica", "Arial", "sans-serif"],
        "monospace": ["Courier New", "Courier", "monospace"],
    }
    
    # Brand font mappings
    BRAND_FONTS = {
        "heading": {
            "family": "Playfair Display",
            "style": "serif",
            "files": {
                400: "PlayfairDisplay-Regular.ttf",
                500: "PlayfairDisplay-Medium.ttf",
                600: "PlayfairDisplay-SemiBold.ttf",
            }
        },
        "body": {
            "family": "Inter",
            "style": "sans-serif",
            "files": {
                400: "Inter-Regular.ttf",
                500: "Inter-Medium.ttf",
                600: "Inter-SemiBold.ttf",
            }
        }
    }
    
    def __init__(self, fonts_dir: Path = None):
        """
        Initialize the font manager.
        
        Args:
            fonts_dir: Path to the fonts directory. Defaults to brand/fonts.
        """
        if fonts_dir is None:
            fonts_dir = Path(__file__).parent.parent.parent / "brand" / "fonts"
        self.fonts_dir = fonts_dir
        self._cache: Dict[str, Any] = {}
    
    def get_font_path(self, font_type: str, weight: int = 400) -> Optional[Path]:
        """
        Get the path to a font file.
        
        Args:
            font_type: "heading" or "body"
            weight: Font weight (400, 500, 600)
            
        Returns:
            Path to the font file, or None if not found.
        """
        if font_type not in self.BRAND_FONTS:
            return None
        
        font_info = self.BRAND_FONTS[font_type]
        files = font_info.get("files", {})
        
        # Try exact weight, then fallback to closest
        filename = files.get(weight)
        if not filename:
            filename = files.get(400)  # Fallback to regular
        
        if not filename:
            return None
        
        font_path = self.fonts_dir / filename
        return font_path if font_path.exists() else None
    
    def get_font_family(self, font_type: str) -> str:
        """Get the font family name for a font type."""
        if font_type in self.BRAND_FONTS:
            return self.BRAND_FONTS[font_type]["family"]
        return font_type
    
    def get_fallback_stack(self, font_type: str) -> str:
        """
        Get a CSS-style font stack with fallbacks.
        
        Args:
            font_type: "heading" or "body"
            
        Returns:
            Font stack string like "'Playfair Display', Georgia, serif"
        """
        if font_type not in self.BRAND_FONTS:
            return "sans-serif"
        
        font_info = self.BRAND_FONTS[font_type]
        family = font_info["family"]
        style = font_info.get("style", "sans-serif")
        fallbacks = self.FALLBACKS.get(style, ["sans-serif"])
        
        # Build font stack
        stack = [f"'{family}'"] + fallbacks
        return ", ".join(stack)
    
    def list_available_fonts(self) -> Dict[str, bool]:
        """
        List all brand fonts and their availability.
        
        Returns:
            Dict mapping font names to availability status.
        """
        available = {}
        for font_type, info in self.BRAND_FONTS.items():
            for weight, filename in info.get("files", {}).items():
                key = f"{info['family']} ({weight})"
                font_path = self.fonts_dir / filename
                available[key] = font_path.exists()
        return available


def load_font(font_type: str, weight: int = 400, fonts_dir: Path = None) -> Optional[Path]:
    """
    Convenience function to load a font path.
    
    Args:
        font_type: "heading" or "body"
        weight: Font weight
        fonts_dir: Optional fonts directory
        
    Returns:
        Path to font file or None.
    """
    manager = FontManager(fonts_dir)
    return manager.get_font_path(font_type, weight)
