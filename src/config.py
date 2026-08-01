"""
Brand Configuration Loader

Loads and validates the brand_config.json file, providing easy access
to brand colors, typography, logos, and spacing values.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field


@dataclass
class ColorDef:
    """Color definition with hex value and usage notes."""
    name: str
    hex: str
    rgb: List[int] = field(default_factory=list)
    usage: str = ""


@dataclass
class FontDef:
    """Font definition with family, weights, and file references."""
    family: str
    weights: List[int]
    style: str = "sans-serif"
    files: Dict[str, str] = field(default_factory=dict)


@dataclass
class TypeScale:
    """Typography scale definition."""
    font: str
    weight: int
    size_px: List[int]
    size_rem: List[float] = field(default_factory=list)
    usage: str = ""


@dataclass
class LogoDef:
    """Logo definition with file path and usage context."""
    file: str
    usage: str = ""


@dataclass 
class BrandConfig:
    """
    Complete brand configuration loaded from brand_config.json.
    
    Provides easy access to all brand values with dot notation:
        config.colors.primary.hex  -> "#243A4B"
        config.typography.heading.family -> "Playfair Display"
    """
    brand_name: str
    tagline: str
    version: str
    
    # Colors
    colors: Dict[str, ColorDef]
    color_ratio: Dict[str, int]
    chart_colors: List[str]
    
    # Typography
    typography: Dict[str, FontDef]
    type_scale: Dict[str, TypeScale]
    
    # Logos
    logos: Dict[str, LogoDef]
    
    # Spacing
    spacing: Dict[str, Any]
    
    # Raw config for direct access
    _raw: Dict[str, Any] = field(default_factory=dict)
    
    def get_color(self, name: str) -> str:
        """Get a color hex value by name."""
        if name in self.colors:
            return self.colors[name].hex
        return name  # Return as-is if not found (might be a literal hex)
    
    def get_font_family(self, font_type: str) -> str:
        """Get font family name."""
        if font_type in self.typography:
            return self.typography[font_type].family
        return font_type
    
    def resolve_reference(self, ref: str) -> Any:
        """
        Resolve a $brand.* reference to its actual value.
        
        Examples:
            $colors.primary.hex -> "#243A4B"
            $typography.heading.family -> "Playfair Display"
            $spacing.page_margin -> 40
        """
        if not ref.startswith("$"):
            return ref
            
        # Remove $ prefix and split path
        path = ref[1:].split(".")
        
        # Navigate through the raw config
        value = self._raw
        for key in path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return ref  # Return original if path not found
                
        return value


def load_brand_config(config_path: Union[str, Path] = None) -> BrandConfig:
    """
    Load brand configuration from JSON file.
    
    Args:
        config_path: Path to brand_config.json. If None, uses default location.
        
    Returns:
        BrandConfig object with all brand values loaded.
    """
    if config_path is None:
        # Default to brand/brand_config.json relative to project root
        config_path = Path(__file__).parent.parent / "brand" / "brand_config.json"
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Brand config not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = json.load(f)
    
    # Parse colors
    colors = {}
    for name, data in raw_config.get("colors", {}).items():
        colors[name] = ColorDef(
            name=data.get("name", name),
            hex=data.get("hex", ""),
            rgb=data.get("rgb", []),
            usage=data.get("usage", "")
        )
    
    # Parse typography
    typography = {}
    for name, data in raw_config.get("typography", {}).items():
        typography[name] = FontDef(
            family=data.get("family", ""),
            weights=data.get("weights", []),
            style=data.get("style", "sans-serif"),
            files=data.get("files", {})
        )
    
    # Parse type scale
    type_scale = {}
    for name, data in raw_config.get("type_scale", {}).items():
        type_scale[name] = TypeScale(
            font=data.get("font", "body"),
            weight=data.get("weight", 400),
            size_px=data.get("size_px", [16, 16]),
            size_rem=data.get("size_rem", [1.0, 1.0]),
            usage=data.get("usage", "")
        )
    
    # Parse logos
    logos = {}
    for name, data in raw_config.get("logos", {}).items():
        logos[name] = LogoDef(
            file=data.get("file", ""),
            usage=data.get("usage", "")
        )
    
    # Parse chart colors
    chart_colors_data = raw_config.get("chart_colors", {})
    chart_colors = chart_colors_data.get("series", []) if isinstance(chart_colors_data, dict) else []
    
    return BrandConfig(
        brand_name=raw_config.get("brand_name", ""),
        tagline=raw_config.get("tagline", ""),
        version=raw_config.get("version", "1.0"),
        colors=colors,
        color_ratio=raw_config.get("color_ratio", {}),
        chart_colors=chart_colors,
        typography=typography,
        type_scale=type_scale,
        logos=logos,
        spacing=raw_config.get("spacing", {}),
        _raw=raw_config
    )


# Convenience function for quick access
def get_brand_value(path: str, config: BrandConfig = None) -> Any:
    """
    Quick access to brand values using dot notation.
    
    Args:
        path: Dot-notation path like "colors.primary.hex"
        config: Optional BrandConfig. Loads default if not provided.
        
    Returns:
        The value at the specified path.
    """
    if config is None:
        config = load_brand_config()
    
    return config.resolve_reference(f"${path}")
