"""
Image Renderer

Generates PNG and SVG images from templates using Pillow.
Optimized for social media posts, infographics, and standalone graphics.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from ..template_parser import ParsedTemplate, TemplateElement
from ..config import BrandConfig, load_brand_config


@dataclass
class ImageRenderOptions:
    """Options for image rendering."""
    format: str = "PNG"  # PNG, JPEG, SVG
    quality: int = 95    # JPEG quality
    dpi: int = 150
    background_color: str = "#FFFFFF"
    optimize: bool = True


class ImageRenderer:
    """
    Renders parsed templates to image files (PNG, JPEG).
    
    Ideal for:
    - Social media posts (Instagram, LinkedIn, Twitter)
    - Infographics
    - Individual slides or graphics
    
    Usage:
        renderer = ImageRenderer()
        renderer.render_image(
            template=social_post_template,
            output_path="output.png"
        )
    """
    
    def __init__(self, brand_config: BrandConfig = None, project_root: Path = None):
        """
        Initialize the image renderer.
        
        Args:
            brand_config: BrandConfig for font and color access.
            project_root: Project root for resolving asset paths.
        """
        self.brand_config = brand_config or load_brand_config()
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self._font_cache: Dict[str, ImageFont.FreeTypeFont] = {}
    
    def render_image(
        self,
        template: ParsedTemplate,
        output_path: Union[str, Path],
        options: ImageRenderOptions = None
    ) -> Path:
        """
        Render a single template to an image file.
        
        Args:
            template: ParsedTemplate to render.
            output_path: Path to save the output image.
            options: Optional render options.
            
        Returns:
            Path to the generated image file.
        """
        if not PILLOW_AVAILABLE:
            raise ImportError("Pillow is required for image rendering. Install with: pip install Pillow")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        options = options or ImageRenderOptions()
        
        # Get dimensions
        dims = template.dimensions
        width = dims.get("width", 816)
        height = dims.get("height", 1056)
        
        # Create image with background
        bg_color = self._parse_color(
            template.background.get("color", options.background_color)
        )
        image = Image.new("RGBA", (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Render elements
        for element in template.elements:
            self._render_element(image, draw, element)
        
        # Save image
        if options.format.upper() == "JPEG":
            # Convert to RGB for JPEG
            image = image.convert("RGB")
            image.save(output_path, "JPEG", quality=options.quality, optimize=options.optimize)
        else:
            image.save(output_path, "PNG", optimize=options.optimize)
        
        return output_path
    
    def render_batch(
        self,
        templates: List[ParsedTemplate],
        output_dir: Union[str, Path],
        name_pattern: str = "page_{:02d}.png",
        options: ImageRenderOptions = None
    ) -> List[Path]:
        """
        Render multiple templates as separate images.
        
        Args:
            templates: List of templates to render.
            output_dir: Directory to save images.
            name_pattern: Pattern for naming files (use {} for page number).
            options: Optional render options.
            
        Returns:
            List of paths to generated images.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        paths = []
        for i, template in enumerate(templates):
            filename = name_pattern.format(i)
            output_path = output_dir / filename
            self.render_image(template, output_path, options)
            paths.append(output_path)
        
        return paths
    
    def _render_element(
        self,
        image: 'Image.Image',
        draw: 'ImageDraw.Draw',
        element: TemplateElement
    ):
        """Render a single element to the image."""
        
        x = element.position.get("x", 0)
        y = element.position.get("y", 0)
        
        if element.element_type == "text":
            self._render_text(draw, element, x, y)
        elif element.element_type == "image":
            self._render_image_element(image, element, x, y)
        elif element.element_type == "rectangle":
            self._render_rectangle(draw, element, x, y)
        elif element.element_type == "graphic":
            self._render_graphic(image, element, x, y)
    
    def _render_text(
        self,
        draw: 'ImageDraw.Draw',
        element: TemplateElement,
        x: int,
        y: int
    ):
        """Render a text element."""
        content = element.content or ""
        if not content or content.startswith("{{"):
            return  # Skip unfilled variables
        
        # Get font
        font = self._get_font(element.font, element.font_size or 16, element.font_weight)
        
        # Get color
        color = self._parse_color(element.color or "#000000")
        
        # Handle max_width with text wrapping
        max_width = element.max_width
        if max_width:
            lines = self._wrap_text(content, font, max_width)
            line_height = (element.font_size or 16) * (element.line_height or 1.2)
            
            for i, line in enumerate(lines):
                draw.text((x, y + i * line_height), line, font=font, fill=color)
        else:
            draw.text((x, y), content, font=font, fill=color)
    
    def _render_image_element(
        self,
        image: 'Image.Image',
        element: TemplateElement,
        x: int,
        y: int
    ):
        """Render an image element."""
        source = element.source
        if not source or source.startswith("$"):
            return
        
        image_path = self.project_root / "brand" / source
        if not image_path.exists():
            return
        
        try:
            overlay = Image.open(image_path)
            
            # Resize if size specified
            size = element.size
            if size:
                width = size.get("width", overlay.width)
                height = size.get("height", overlay.height)
                overlay = overlay.resize((width, height), Image.Resampling.LANCZOS)
            
            # Handle transparency
            if overlay.mode == "RGBA":
                image.paste(overlay, (x, y), overlay)
            else:
                image.paste(overlay, (x, y))
        except Exception:
            pass
    
    def _render_rectangle(
        self,
        draw: 'ImageDraw.Draw',
        element: TemplateElement,
        x: int,
        y: int
    ):
        """Render a rectangle element."""
        size = element.size or {}
        width = size.get("width", 100)
        height = size.get("height", 100)
        
        bg = element.raw.get("background", "#CCCCCC")
        color = self._parse_color(bg)
        
        draw.rectangle([x, y, x + width, y + height], fill=color)
    
    def _render_graphic(
        self,
        image: 'Image.Image',
        element: TemplateElement,
        x: int,
        y: int
    ):
        """Render a graphic/SVG element (as PNG fallback)."""
        # For SVG graphics, we'd need cairosvg or similar
        # For now, try to load as regular image
        source = element.source
        if not source:
            return
        
        # Try PNG version first, then SVG
        for ext in [".png", ".svg", ""]:
            graphic_path = self.project_root / "brand" / source
            if not graphic_path.suffix:
                graphic_path = graphic_path.with_suffix(ext)
            
            if graphic_path.exists() and graphic_path.suffix == ".png":
                try:
                    overlay = Image.open(graphic_path)
                    size = element.size
                    if size:
                        overlay = overlay.resize(
                            (size.get("width", overlay.width), size.get("height", overlay.height)),
                            Image.Resampling.LANCZOS
                        )
                    if overlay.mode == "RGBA":
                        image.paste(overlay, (x, y), overlay)
                    else:
                        image.paste(overlay, (x, y))
                    return
                except Exception:
                    pass
    
    def _get_font(
        self,
        font_family: Optional[str],
        size: int,
        weight: Optional[int] = None
    ) -> 'ImageFont.FreeTypeFont':
        """Get or load a font."""
        # Create cache key
        cache_key = f"{font_family}_{size}_{weight}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Try to load custom font
        fonts_dir = self.project_root / "brand" / "fonts"
        
        font_files = {
            "Playfair Display": {
                400: "PlayfairDisplay-Regular.ttf",
                500: "PlayfairDisplay-Medium.ttf",
                600: "PlayfairDisplay-SemiBold.ttf",
            },
            "Inter": {
                400: "Inter-Regular.ttf",
                500: "Inter-Medium.ttf",
                600: "Inter-SemiBold.ttf",
            }
        }
        
        font = None
        weight = weight or 400
        
        # Try to find matching font file
        for family_name, weights in font_files.items():
            if font_family and family_name.lower() in str(font_family).lower():
                font_file = weights.get(weight, weights.get(400))
                font_path = fonts_dir / font_file
                if font_path.exists():
                    try:
                        font = ImageFont.truetype(str(font_path), size)
                        break
                    except Exception:
                        pass
        
        # Fallback to default font
        if font is None:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
            except Exception:
                font = ImageFont.load_default()
        
        self._font_cache[cache_key] = font
        return font
    
    def _wrap_text(
        self,
        text: str,
        font: 'ImageFont.FreeTypeFont',
        max_width: int
    ) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def _parse_color(self, color: Any) -> Tuple[int, int, int, int]:
        """Parse color to RGBA tuple."""
        if isinstance(color, (list, tuple)):
            if len(color) == 3:
                return tuple(color) + (255,)
            return tuple(color)
        
        if isinstance(color, str):
            if color.startswith("#"):
                hex_color = color.lstrip("#")
                if len(hex_color) == 6:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return (r, g, b, 255)
                elif len(hex_color) == 8:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    a = int(hex_color[6:8], 16)
                    return (r, g, b, a)
        
        return (255, 255, 255, 255)  # Default to white


# Convenience function
def render_image(
    template: ParsedTemplate,
    output_path: Union[str, Path],
    brand_config: BrandConfig = None
) -> Path:
    """
    Quick function to render a template to an image.
    
    Args:
        template: ParsedTemplate to render.
        output_path: Path to save the image.
        brand_config: Optional BrandConfig.
        
    Returns:
        Path to the generated image.
    """
    renderer = ImageRenderer(brand_config=brand_config)
    return renderer.render_image(template, output_path)
