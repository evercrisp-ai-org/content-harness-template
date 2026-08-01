"""
Color Utilities

Provides color manipulation, conversion, and accessibility helpers.
"""

from typing import Tuple, Union, List
import colorsys


class ColorUtils:
    """
    Utility class for color manipulation and conversion.
    
    Supports:
    - Hex to RGB conversion
    - RGB to Hex conversion
    - Color lightening/darkening
    - Contrast ratio calculation
    - Accessibility checking
    """
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple.
        
        Args:
            hex_color: Hex color string (e.g., "#243A4B" or "243A4B")
            
        Returns:
            Tuple of (R, G, B) values (0-255)
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """
        Convert RGB values to hex color.
        
        Args:
            r, g, b: RGB values (0-255)
            
        Returns:
            Hex color string with # prefix
        """
        return f"#{r:02X}{g:02X}{b:02X}"
    
    @staticmethod
    def lighten(hex_color: str, factor: float = 0.1) -> str:
        """
        Lighten a color by a factor.
        
        Args:
            hex_color: Original hex color
            factor: Amount to lighten (0.0 to 1.0)
            
        Returns:
            Lightened hex color
        """
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        
        # Convert to HLS and increase lightness
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        l = min(1.0, l + factor)
        
        # Convert back
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return ColorUtils.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    @staticmethod
    def darken(hex_color: str, factor: float = 0.1) -> str:
        """
        Darken a color by a factor.
        
        Args:
            hex_color: Original hex color
            factor: Amount to darken (0.0 to 1.0)
            
        Returns:
            Darkened hex color
        """
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        
        # Convert to HLS and decrease lightness
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        l = max(0.0, l - factor)
        
        # Convert back
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return ColorUtils.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    @staticmethod
    def get_luminance(hex_color: str) -> float:
        """
        Calculate relative luminance of a color.
        
        Uses the WCAG formula for perceived brightness.
        
        Args:
            hex_color: Hex color string
            
        Returns:
            Luminance value (0.0 to 1.0)
        """
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        
        # Normalize and apply gamma correction
        def adjust(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = adjust(r), adjust(g), adjust(b)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def contrast_ratio(color1: str, color2: str) -> float:
        """
        Calculate contrast ratio between two colors.
        
        Args:
            color1, color2: Hex color strings
            
        Returns:
            Contrast ratio (1.0 to 21.0)
        """
        l1 = ColorUtils.get_luminance(color1)
        l2 = ColorUtils.get_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def is_accessible(
        foreground: str,
        background: str,
        level: str = "AA",
        large_text: bool = False
    ) -> bool:
        """
        Check if a color combination meets WCAG accessibility standards.
        
        Args:
            foreground: Text color (hex)
            background: Background color (hex)
            level: "AA" or "AAA"
            large_text: Whether text is large (18pt+ or 14pt+ bold)
            
        Returns:
            True if the combination is accessible
        """
        ratio = ColorUtils.contrast_ratio(foreground, background)
        
        thresholds = {
            ("AA", False): 4.5,
            ("AA", True): 3.0,
            ("AAA", False): 7.0,
            ("AAA", True): 4.5,
        }
        
        threshold = thresholds.get((level, large_text), 4.5)
        return ratio >= threshold
    
    @staticmethod
    def suggest_text_color(background: str) -> str:
        """
        Suggest optimal text color (black or white) for a background.
        
        Args:
            background: Background hex color
            
        Returns:
            "#000000" or "#FFFFFF"
        """
        luminance = ColorUtils.get_luminance(background)
        return "#000000" if luminance > 0.5 else "#FFFFFF"
    
    @staticmethod
    def create_palette(
        base_color: str,
        variations: int = 5
    ) -> List[str]:
        """
        Create a palette of color variations from a base color.
        
        Args:
            base_color: Base hex color
            variations: Number of variations to generate
            
        Returns:
            List of hex colors from light to dark
        """
        palette = []
        step = 1.0 / (variations + 1)
        
        for i in range(variations):
            factor = (i + 1) * step - 0.5
            if factor < 0:
                color = ColorUtils.lighten(base_color, abs(factor))
            else:
                color = ColorUtils.darken(base_color, factor)
            palette.append(color)
        
        return palette


# Convenience functions
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB tuple."""
    return ColorUtils.hex_to_rgb(hex_color)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return ColorUtils.rgb_to_hex(r, g, b)
