"""
PDF Renderer

Generates PDF documents from parsed templates using ReportLab.
Supports multi-page documents with consistent branding, text wrapping,
and complex element types (checklists, numbered lists, charts, etc.).
"""

import io
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, Color
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.ticker import PercentFormatter
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from ..template_parser import ParsedTemplate, TemplateElement
from ..config import BrandConfig, load_brand_config


@dataclass
class RenderOptions:
    """Options for PDF rendering."""
    output_path: Path
    dpi: int = 150
    embed_fonts: bool = True
    compress: bool = True
    author: str = "Content Harness"
    subject: str = ""
    keywords: List[str] = None


class PDFRenderer:
    """
    Renders parsed templates to PDF documents.
    
    Supports:
    - Multi-line text with automatic wrapping
    - Paragraph rendering with line height
    - Checkbox lists for checklists
    - Numbered and bullet lists
    - Images with proper scaling
    - Charts (placeholder or matplotlib integration)
    
    Usage:
        renderer = PDFRenderer()
        renderer.render_document(
            templates=[cover_template, content_template, chart_template],
            output_path="output.pdf"
        )
    """
    
    def __init__(self, brand_config: BrandConfig = None, project_root: Path = None):
        """
        Initialize the PDF renderer.
        
        Args:
            brand_config: BrandConfig for font and color access.
            project_root: Project root for resolving asset paths.
        """
        self.brand_config = brand_config or load_brand_config()
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self._fonts_registered = False
        self._font_map = {}
    
    def render_document(
        self,
        templates: List[ParsedTemplate],
        output_path: Union[str, Path],
        options: RenderOptions = None
    ) -> Path:
        """
        Render multiple templates as a multi-page PDF document.
        
        Args:
            templates: List of ParsedTemplate objects (one per page).
            output_path: Path to save the output PDF.
            options: Optional render options.
            
        Returns:
            Path to the generated PDF file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for PDF rendering. Install with: pip install reportlab")
        
        # Register fonts
        self._register_fonts()
        
        # Get page dimensions from first template
        dims = templates[0].dimensions if templates else {"width": 816, "height": 1056}
        page_width = dims.get("width", 816)
        page_height = dims.get("height", 1056)
        
        # Create PDF canvas
        c = canvas.Canvas(
            str(output_path),
            pagesize=(page_width, page_height)
        )
        
        # Set document metadata
        c.setAuthor(options.author if options else "Content Harness")
        c.setTitle(templates[0].template_name if templates else "Document")
        
        # Render each template as a page
        for i, template in enumerate(templates):
            if i > 0:
                c.showPage()
            self._render_page(c, template, page_width, page_height)
        
        c.save()
        return output_path
    
    def render_single_page(
        self,
        template: ParsedTemplate,
        output_path: Union[str, Path]
    ) -> Path:
        """Render a single template to a PDF page."""
        return self.render_document([template], output_path)
    
    def _render_page(
        self,
        canvas_obj: 'canvas.Canvas',
        template: ParsedTemplate,
        page_width: int,
        page_height: int
    ):
        """Render a single template to the canvas."""
        
        # Draw main page background
        bg = template.background
        if bg.get("type") == "solid":
            color = bg.get("color", "#FFFFFF")
            if isinstance(color, str) and color.startswith("#"):
                canvas_obj.setFillColor(HexColor(color))
                canvas_obj.rect(0, 0, page_width, page_height, fill=1, stroke=0)
        
        # Draw section backgrounds (if template has sections)
        sections = template.raw.get("sections", [])
        for section in sections:
            self._render_section_background(canvas_obj, section, page_height)
        
        # Draw elements
        for element in template.elements:
            self._render_element(canvas_obj, element, page_height, page_width)
    
    def _render_section_background(
        self,
        canvas_obj: 'canvas.Canvas',
        section: Dict,
        page_height: int
    ):
        """Render a section's background."""
        bg = section.get("background", {})
        if not bg:
            return
        
        position = section.get("position", {"x": 0, "y": 0})
        size = section.get("size", {"width": 816, "height": 100})
        
        # Convert from top-left origin to bottom-left origin (PDF standard)
        x = position.get("x", 0)
        y = page_height - position.get("y", 0) - size.get("height", 100)
        width = size.get("width", 816)
        height = size.get("height", 100)
        
        if bg.get("type") == "solid":
            color = bg.get("color", "#FFFFFF")
            if isinstance(color, str) and color.startswith("#"):
                canvas_obj.setFillColor(HexColor(color))
                canvas_obj.rect(x, y, width, height, fill=1, stroke=0)
    
    def _render_element(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        page_height: int,
        page_width: int = 816
    ):
        """Render a single element to the canvas."""
        
        # Check visibility - skip elements that are explicitly hidden
        visible = element.raw.get("visible", True)
        # Handle boolean False
        if visible is False:
            return
        # Handle string representations of false
        if isinstance(visible, str):
            if visible.lower() in ("false", "0", "no", "none"):
                return
            # Skip if visible is an unfilled variable reference
            if visible.startswith("{{"):
                return
        # Handle numeric 0
        if visible == 0:
            return
        
        # Convert from top-left origin to bottom-left origin (PDF standard)
        x = element.position.get("x", 0)
        y = page_height - element.position.get("y", 0)
        
        element_type = element.element_type
        
        if element_type == "text":
            self._render_text(canvas_obj, element, x, y, page_height)
        elif element_type == "image":
            self._render_image(canvas_obj, element, x, y, page_height)
        elif element_type == "rectangle":
            self._render_rectangle(canvas_obj, element, x, y, page_height)
        elif element_type == "chart":
            self._render_chart(canvas_obj, element, x, y, page_height)
        elif element_type == "numbered_list":
            self._render_numbered_list(canvas_obj, element, x, y, page_height)
        elif element_type == "bullet_list":
            self._render_bullet_list(canvas_obj, element, x, y, page_height)
        elif element_type == "checklist_groups":
            self._render_checklist_groups(canvas_obj, element, x, y, page_height)
        elif element_type == "key_value_list":
            self._render_key_value_list(canvas_obj, element, x, y, page_height)
        elif element_type == "metric_grid":
            self._render_metric_grid(canvas_obj, element, x, y, page_height)
        elif element_type == "legend":
            self._render_legend(canvas_obj, element, x, y, page_height)
        elif element_type == "graphic":
            self._render_graphic(canvas_obj, element, x, y, page_height)
        elif element_type == "component":
            # Components should be resolved earlier; skip if not
            pass
    
    def _get_font_name(self, font_family: str, weight: int = 400) -> str:
        """Get the registered font name for a font family and weight."""
        if not font_family:
            return "Helvetica"
        
        font_family_str = str(font_family)
        
        if "Playfair" in font_family_str:
            if weight >= 600:
                return self._font_map.get("PlayfairDisplay-SemiBold", "Times-Bold")
            elif weight >= 500:
                return self._font_map.get("PlayfairDisplay-Medium", "Times-Roman")
            else:
                return self._font_map.get("PlayfairDisplay-Regular", "Times-Roman")
        elif "Inter" in font_family_str:
            if weight >= 600:
                return self._font_map.get("Inter-SemiBold", "Helvetica-Bold")
            elif weight >= 500:
                return self._font_map.get("Inter-Medium", "Helvetica")
            else:
                return self._font_map.get("Inter-Regular", "Helvetica")
        else:
            return "Helvetica"
    
    def _render_text(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ) -> int:
        """
        Render a text element with support for multi-line wrapping and markdown bold.
        
        Returns:
            The total height consumed by the rendered text.
        """
        content = element.content or ""
        if not content or content.startswith("{{"):
            return 0  # Skip unfilled variables
        
        # Get styling
        font_family = element.font or "Helvetica"
        font_weight = element.font_weight or 400
        font_size = element.font_size or 16
        line_height = element.line_height or 1.4
        max_width = element.max_width or 600
        color = element.color or "#000000"
        text_align = element.raw.get("text_align", "left")
        
        # Get max_height constraint if specified (prevents overflow into other elements)
        max_height = element.raw.get("max_height", None)
        
        # Check if content has markdown bold markers
        has_bold_markers = '**' in content
        
        # Get the appropriate font
        font_name = self._get_font_name(font_family, font_weight)
        bold_font_name = self._get_font_name(font_family, 600)  # For bold segments
        
        try:
            canvas_obj.setFont(font_name, font_size)
        except:
            canvas_obj.setFont("Helvetica", font_size)
            font_name = "Helvetica"
            bold_font_name = "Helvetica-Bold"
        
        # Set color
        if isinstance(color, str) and color.startswith("#"):
            canvas_obj.setFillColor(HexColor(color))
        
        # Calculate line spacing
        line_spacing = font_size * line_height
        
        # Handle multi-line content with word wrapping
        paragraphs = content.split('\n\n')
        current_y = y - font_size
        start_y = current_y
        height_consumed = 0
        
        for para_idx, paragraph in enumerate(paragraphs):
            if para_idx > 0:
                paragraph_spacing = font_size * 0.5
                current_y -= paragraph_spacing
                height_consumed += paragraph_spacing
            
            # For markdown bold, strip the markers for wrapping calculation
            plain_paragraph = paragraph.replace('**', '') if has_bold_markers else paragraph
            
            # Wrap text to max_width (using plain text for measurement)
            lines = self._wrap_text(canvas_obj, plain_paragraph, font_name, font_size, max_width)
            
            # If we have bold markers, we need to render with mixed fonts
            if has_bold_markers:
                # Re-wrap the original with markers to preserve positions
                self._render_lines_with_bold(
                    canvas_obj, paragraph, lines, x, current_y, 
                    font_name, bold_font_name, font_size, 
                    max_width, text_align, color, line_spacing
                )
                current_y -= len(lines) * line_spacing
                height_consumed += len(lines) * line_spacing
            else:
                for line in lines:
                    # Check if we would exceed max_height
                    if max_height is not None:
                        projected_height = height_consumed + line_spacing
                        if projected_height > max_height:
                            # Stop rendering - we've hit the height limit
                            return int(height_consumed)
                    
                    if text_align == "center":
                        canvas_obj.drawCentredString(x + max_width / 2, current_y, line)
                    elif text_align == "right":
                        canvas_obj.drawRightString(x + max_width, current_y, line)
                    else:
                        canvas_obj.drawString(x, current_y, line)
                    
                    current_y -= line_spacing
                    height_consumed += line_spacing
        
        return int(height_consumed)
    
    def _render_lines_with_bold(
        self,
        canvas_obj: 'canvas.Canvas',
        original_text: str,
        wrapped_lines: List[str],
        x: int,
        start_y: int,
        font_name: str,
        bold_font_name: str,
        font_size: int,
        max_width: int,
        text_align: str,
        color: str,
        line_spacing: float
    ):
        """
        Render text lines with markdown **bold** markers rendered as bold text.
        """
        import re
        
        # Parse the original text into segments (bold and non-bold)
        # Pattern matches **text** and captures the text inside
        pattern = r'\*\*([^*]+)\*\*'
        
        # Get all bold segments
        bold_segments = set(re.findall(pattern, original_text))
        
        # For each wrapped line, render with mixed fonts
        current_y = start_y
        
        for line in wrapped_lines:
            current_x = x
            
            # Split line into words and render each with appropriate font
            words = line.split(' ')
            
            for i, word in enumerate(words):
                # Check if this word or part of it is in a bold segment
                is_bold = any(word in seg or seg in word for seg in bold_segments)
                
                # Choose font
                if is_bold:
                    canvas_obj.setFont(bold_font_name, font_size)
                else:
                    canvas_obj.setFont(font_name, font_size)
                
                # Set color
                if isinstance(color, str) and color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(color))
                
                # Add space before word (except first word)
                if i > 0:
                    current_x += canvas_obj.stringWidth(' ', font_name, font_size)
                
                # Draw the word
                if text_align == "left" or text_align != "center":
                    canvas_obj.drawString(current_x, current_y, word)
                
                # Move x position
                current_font = bold_font_name if is_bold else font_name
                current_x += canvas_obj.stringWidth(word, current_font, font_size)
            
            current_y -= line_spacing
    
    def _wrap_text(
        self,
        canvas_obj: 'canvas.Canvas',
        text: str,
        font_name: str,
        font_size: int,
        max_width: int
    ) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.replace('\n', ' ').split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            try:
                width = canvas_obj.stringWidth(test_line, font_name, font_size)
            except:
                width = len(test_line) * font_size * 0.5
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else ['']
    
    def _calculate_text_height(
        self,
        canvas_obj: 'canvas.Canvas',
        content: str,
        font_name: str,
        font_size: int,
        line_height: float,
        max_width: int
    ) -> int:
        """Calculate the total height a text block will occupy after wrapping."""
        if not content:
            return 0
        
        paragraphs = content.split('\n\n')
        total_height = 0
        line_spacing = font_size * line_height
        
        for para_idx, paragraph in enumerate(paragraphs):
            if para_idx > 0:
                total_height += font_size * 0.5  # Paragraph spacing
            
            lines = self._wrap_text(canvas_obj, paragraph, font_name, font_size, max_width)
            total_height += len(lines) * line_spacing
        
        return int(total_height)
    
    def _calculate_element_height(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement
    ) -> int:
        """
        Calculate the height an element will consume when rendered.
        
        This is useful for dynamic layouts where subsequent elements need
        to be positioned based on actual content height.
        
        Args:
            canvas_obj: The canvas for text measurement.
            element: The element to calculate height for.
            
        Returns:
            The height in points/pixels the element will consume.
        """
        element_type = element.element_type
        
        if element_type == "text":
            return self._calculate_text_element_height(canvas_obj, element)
        elif element_type == "numbered_list":
            return self._calculate_numbered_list_height(canvas_obj, element)
        elif element_type == "bullet_list":
            return self._calculate_bullet_list_height(canvas_obj, element)
        elif element_type == "rectangle":
            size = element.size or {}
            return size.get("height", 0)
        elif element_type == "image":
            size = element.size or {}
            return size.get("height", 0)
        elif element_type == "chart":
            size = element.size or {}
            return size.get("height", 300)
        else:
            return 0
    
    def _calculate_text_element_height(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement
    ) -> int:
        """Calculate the height a text element will consume."""
        content = element.content or ""
        if not content or content.startswith("{{"):
            return 0
        
        font_family = element.font or "Helvetica"
        font_weight = element.font_weight or 400
        font_size = element.font_size or 16
        line_height = element.line_height or 1.4
        max_width = element.max_width or 600
        
        font_name = self._get_font_name(font_family, font_weight)
        
        return self._calculate_text_height(
            canvas_obj, content, font_name, font_size, line_height, max_width
        )
    
    def _calculate_numbered_list_height(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement
    ) -> int:
        """Calculate the height a numbered list will consume."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return 0
        
        styling = element.styling or {}
        item_spacing = element.raw.get("item_spacing", 20)
        max_width = element.max_width or 500
        
        text_font = self._get_font_name(
            styling.get("text_font", "Inter"),
            styling.get("text_weight", 400)
        )
        text_size = styling.get("text_size", 16)
        line_height = styling.get("line_height", 1.5)
        line_spacing = text_size * line_height
        num_indent = 35
        
        total_height = 0
        
        for item in items:
            if isinstance(item, dict):
                label = item.get("label", "")
                summary = item.get("summary", "")
                item_text = label + ": " + summary if label and summary else label or summary
            else:
                item_text = str(item)
            
            lines = self._wrap_text(canvas_obj, item_text, text_font, text_size, max_width - num_indent)
            total_height += len(lines) * line_spacing + item_spacing
        
        return int(total_height)
    
    def _calculate_bullet_list_height(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement
    ) -> int:
        """Calculate the height a bullet list will consume."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return 0
        
        styling = element.styling or {}
        item_spacing = element.raw.get("item_spacing", 16)
        max_width = element.max_width or 500
        
        bullet_size = styling.get("bullet_size", 8)
        text_font = self._get_font_name(styling.get("text_font", "Inter"), 400)
        text_size = styling.get("text_size", 16)
        line_height = styling.get("line_height", 1.5)
        line_spacing = text_size * line_height
        bullet_indent = bullet_size + 12
        
        total_height = 0
        
        for item in items:
            item_text = str(item)
            lines = self._wrap_text(canvas_obj, item_text, text_font, text_size, max_width - bullet_indent)
            total_height += len(lines) * line_spacing + item_spacing
        
        return int(total_height)
    
    def _render_numbered_list(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a numbered list."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return
        
        styling = element.styling or {}
        item_spacing = element.raw.get("item_spacing", 20)
        max_width = element.max_width or 500
        
        # Font settings
        num_font = self._get_font_name(
            styling.get("number_font", "Inter"),
            styling.get("number_weight", 600)
        )
        num_size = styling.get("number_size", 16)
        num_color = styling.get("number_color", "#1E2428")
        
        text_font = self._get_font_name(
            styling.get("text_font", "Inter"),
            styling.get("text_weight", 400)
        )
        text_size = styling.get("text_size", 16)
        text_color = styling.get("text_color", "#1E2428")
        
        # Use consistent line height for proper spacing
        line_height = styling.get("line_height", 1.5)
        line_spacing = text_size * line_height
        
        # Number column width - enough for "10." plus some margin
        num_indent = 35
        
        current_y = y - text_size
        
        for i, item in enumerate(items, 1):
            # Handle different item formats
            if isinstance(item, dict):
                label = item.get("label", "")
                summary = item.get("summary", "")
                if label and summary:
                    item_text = label + ": " + summary
                else:
                    item_text = label or summary
            else:
                item_text = str(item)
            
            # Wrap text first to know how many lines we'll have
            text_x = x + num_indent
            lines = self._wrap_text(canvas_obj, item_text, text_font, text_size, max_width - num_indent)
            
            # Draw number aligned with first line of text
            canvas_obj.setFont(num_font, num_size)
            if isinstance(num_color, str) and num_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(num_color))
            canvas_obj.drawString(x, current_y, f"{i}.")
            
            # Draw text lines
            canvas_obj.setFont(text_font, text_size)
            if isinstance(text_color, str) and text_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(text_color))
            
            for line_idx, line in enumerate(lines):
                line_y = current_y - (line_idx * line_spacing)
                canvas_obj.drawString(text_x, line_y, line)
            
            # Move to next item: account for all lines plus spacing between items
            total_text_height = len(lines) * line_spacing
            current_y -= total_text_height + item_spacing
    
    def _render_bullet_list(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a bullet list."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return
        
        styling = element.styling or {}
        item_spacing = element.raw.get("item_spacing", 16)
        max_width = element.max_width or 500
        
        bullet_color = styling.get("bullet_color", "#B08D57")
        bullet_size = styling.get("bullet_size", 8)
        text_font = self._get_font_name(styling.get("text_font", "Inter"), 400)
        text_size = styling.get("text_size", 16)
        text_color = styling.get("text_color", "#FFFFFF")
        
        # Use consistent line height for proper spacing
        line_height = styling.get("line_height", 1.5)
        line_spacing = text_size * line_height
        
        # Calculate bullet indent
        bullet_indent = bullet_size + 12
        
        current_y = y - text_size
        
        for item in items:
            item_text = str(item)
            
            # Wrap text first to know dimensions
            text_x = x + bullet_indent
            lines = self._wrap_text(canvas_obj, item_text, text_font, text_size, max_width - bullet_indent)
            
            # Draw bullet aligned with first line of text
            if isinstance(bullet_color, str) and bullet_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(bullet_color))
            # Center bullet vertically with first line
            bullet_y = current_y + text_size / 3
            canvas_obj.circle(x + bullet_size/2, bullet_y, bullet_size/2, fill=1, stroke=0)
            
            # Draw text lines
            canvas_obj.setFont(text_font, text_size)
            if isinstance(text_color, str) and text_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(text_color))
            
            for line_idx, line in enumerate(lines):
                line_y = current_y - (line_idx * line_spacing)
                canvas_obj.drawString(text_x, line_y, line)
            
            # Move to next item: account for all lines plus spacing between items
            total_text_height = len(lines) * line_spacing
            current_y -= total_text_height + item_spacing
    
    def _render_checklist_groups(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render grouped checkbox items with smart column balancing."""
        groups = element.raw.get("groups", [])
        if isinstance(groups, str) and groups.startswith("{{"):
            return
        
        styling = element.styling or {}
        columns = element.raw.get("columns", 2)
        column_gap = element.raw.get("column_gap", 40)
        max_width = element.max_width or 656
        column_width = (max_width - column_gap * (columns - 1)) / columns
        group_spacing = element.raw.get("group_spacing", 30)
        
        # Styling
        header_font = self._get_font_name(
            styling.get("group_header_font", "Inter"),
            styling.get("group_header_weight", 600)
        )
        header_size = styling.get("group_header_size", 14)
        header_color = styling.get("group_header_color", "#B08D57")
        
        checkbox_size = styling.get("checkbox_size", 16)
        checkbox_border_color = styling.get("checkbox_border_color", "#5F7483")
        
        item_font = self._get_font_name(styling.get("item_font", "Inter"), 400)
        item_size = styling.get("item_size", 14)
        item_color = styling.get("item_color", "#1E2428")
        item_spacing = styling.get("item_spacing", 10)
        
        # Consistent line height
        line_height = styling.get("line_height", 1.4)
        line_spacing = item_size * line_height
        
        # Calculate column positions and track heights
        col_positions = [x + i * (column_width + column_gap) for i in range(columns)]
        col_y = [y - header_size] * columns  # Current y position for each column
        
        # Pre-calculate group heights for smart column assignment
        def calculate_group_height(group):
            """Calculate the total height a group will consume."""
            header = group.get("header", "")
            items = group.get("items", [])
            height = header_size + styling.get("group_header_spacing", 12)
            
            for item in items:
                item_text = str(item)
                # Estimate lines needed
                lines = self._wrap_text(canvas_obj, item_text, item_font, item_size, column_width - checkbox_size - 12)
                height += len(lines) * line_spacing + item_spacing
            
            return height + group_spacing
        
        # Process groups with smart column assignment
        for group in groups:
            if isinstance(group, str):
                continue
            
            header = group.get("header", "")
            items = group.get("items", [])
            
            # Find the column with the most available space (highest y value)
            current_col = col_y.index(max(col_y))
            col_x = col_positions[current_col]
            current_y = col_y[current_col]
            
            # Draw group header
            canvas_obj.setFont(header_font, header_size)
            if isinstance(header_color, str) and header_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(header_color))
            canvas_obj.drawString(col_x, current_y, header.upper())
            current_y -= header_size + styling.get("group_header_spacing", 12)
            
            # Draw items
            canvas_obj.setFont(item_font, item_size)
            
            for item in items:
                item_text = str(item)
                
                # Wrap text first to know dimensions
                text_x = col_x + checkbox_size + 8
                lines = self._wrap_text(canvas_obj, item_text, item_font, item_size, column_width - checkbox_size - 12)
                
                # Draw checkbox aligned with first line
                if isinstance(checkbox_border_color, str) and checkbox_border_color.startswith("#"):
                    canvas_obj.setStrokeColor(HexColor(checkbox_border_color))
                canvas_obj.setLineWidth(styling.get("checkbox_border_width", 2))
                canvas_obj.rect(
                    col_x, current_y - checkbox_size + item_size/2,
                    checkbox_size, checkbox_size,
                    fill=0, stroke=1
                )
                
                # Draw item text
                if isinstance(item_color, str) and item_color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(item_color))
                
                for line_idx, line in enumerate(lines):
                    line_y = current_y - (line_idx * line_spacing)
                    canvas_obj.drawString(text_x, line_y, line)
                
                # Move down by total text height plus item spacing
                total_text_height = len(lines) * line_spacing
                current_y -= total_text_height + item_spacing
            
            # Update column tracking with group spacing
            col_y[current_col] = current_y - group_spacing
    
    def _render_key_value_list(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a key-value list (for profile sidebars)."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return
        
        styling = element.styling or {}
        item_spacing = element.raw.get("item_spacing", 20)
        
        key_font = self._get_font_name(styling.get("key_font", "Inter"), styling.get("key_weight", 600))
        key_size = styling.get("key_size", 11)
        key_color = styling.get("key_color", "#9AA3A8")
        
        value_font = self._get_font_name(styling.get("value_font", "Inter"), styling.get("value_weight", 500))
        value_size = styling.get("value_size", 15)
        value_color = styling.get("value_color", "#1E2428")
        
        current_y = y - key_size
        
        for item in items:
            if isinstance(item, dict):
                key = item.get("key", "")
                value = item.get("value", "")
                
                # Draw key
                canvas_obj.setFont(key_font, key_size)
                if isinstance(key_color, str) and key_color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(key_color))
                canvas_obj.drawString(x, current_y, key.upper())
                
                # Draw value
                canvas_obj.setFont(value_font, value_size)
                if isinstance(value_color, str) and value_color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(value_color))
                canvas_obj.drawString(x, current_y - key_size - 4, str(value))
                
                current_y -= key_size + value_size + item_spacing
    
    def _render_metric_grid(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a grid of metrics (value + label pairs)."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return
        
        styling = element.styling or {}
        columns = element.raw.get("columns", 2)
        column_width = element.raw.get("column_width", 210)
        row_height = element.raw.get("row_height", 60)
        
        value_font = self._get_font_name(
            styling.get("value_font", "Playfair Display"),
            styling.get("value_weight", 600)
        )
        value_size = styling.get("value_size", 28)
        value_color = styling.get("value_color", "#FFFFFF")
        
        label_font = self._get_font_name(styling.get("label_font", "Inter"), 400)
        label_size = styling.get("label_size", 12)
        label_color = styling.get("label_color", "#9AA3A8")
        
        for i, item in enumerate(items):
            if isinstance(item, dict):
                value = item.get("value", "")
                label = item.get("label", "")
                
                col = i % columns
                row = i // columns
                
                item_x = x + col * column_width
                item_y = y - row * row_height - value_size
                
                # Draw value
                canvas_obj.setFont(value_font, value_size)
                if isinstance(value_color, str) and value_color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(value_color))
                canvas_obj.drawString(item_x, item_y, str(value))
                
                # Draw label
                canvas_obj.setFont(label_font, label_size)
                if isinstance(label_color, str) and label_color.startswith("#"):
                    canvas_obj.setFillColor(HexColor(label_color))
                canvas_obj.drawString(item_x, item_y - value_size/2 - 8, str(label))
    
    def _render_image(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render an image element with proper transparency support."""
        source = element.source
        if not source or source.startswith("$") or source.startswith("{{"):
            return  # Skip unresolved sources
        
        # Try multiple paths for the image
        possible_paths = [
            self.project_root / "brand" / source,
            self.project_root / source,
            Path(source)
        ]
        
        image_path = None
        for p in possible_paths:
            if p.exists():
                image_path = p
                break
        
        if not image_path:
            return  # Skip missing images
        
        size = element.size or {}
        width = size.get("width", 100)
        height = size.get("height", width)  # Default to square
        
        try:
            # Use ImageReader for better PNG transparency handling
            img_reader = ImageReader(str(image_path))
            
            # Check if image has transparency (alpha channel)
            # PIL Image mode 'RGBA' or 'LA' indicates alpha channel
            pil_image = img_reader._image
            has_alpha = pil_image.mode in ('RGBA', 'LA') or \
                       (pil_image.mode == 'P' and 'transparency' in pil_image.info)
            
            canvas_obj.drawImage(
                img_reader,
                x, y - height,
                width=width,
                height=height,
                preserveAspectRatio=True,
                mask='auto' if has_alpha else None
            )
        except Exception as e:
            # Try without transparency as fallback
            try:
                canvas_obj.drawImage(
                    str(image_path),
                    x, y - height,
                    width=width,
                    height=height,
                    preserveAspectRatio=True
                )
            except Exception:
                pass  # Skip failed image loads
    
    def _render_rectangle(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a rectangle element."""
        size = element.size or {}
        width = size.get("width", 100)
        height = size.get("height", 100)
        border_radius = element.raw.get("border_radius", 0)
        
        bg = element.raw.get("background", "#CCCCCC")
        if isinstance(bg, str) and bg.startswith("#"):
            canvas_obj.setFillColor(HexColor(bg))
        
        if border_radius:
            canvas_obj.roundRect(x, y - height, width, height, border_radius, fill=1, stroke=0)
        else:
            canvas_obj.rect(x, y - height, width, height, fill=1, stroke=0)
    
    def _render_chart(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a chart element using matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            self._render_chart_placeholder(canvas_obj, element, x, y, page_height)
            return
        
        chart_type = element.raw.get("chart_type", "line")
        data = element.raw.get("data", {})
        
        # Skip if data is still a variable reference or empty
        if isinstance(data, str):
            if data.startswith("{{") or data.startswith("$"):
                self._render_chart_placeholder(canvas_obj, element, x, y, page_height)
                return
        
        # Ensure data is a dict with proper structure
        if not isinstance(data, dict):
            self._render_chart_placeholder(canvas_obj, element, x, y, page_height)
            return
        
        size = element.size or {}
        width = size.get("width", 400)
        height = size.get("height", 300)
        styling = element.raw.get("styling", {})
        
        # Get brand colors for charts (resolve any remaining references)
        chart_colors = self._get_chart_colors(styling)
        
        try:
            if chart_type == "line":
                chart_image = self._create_line_chart(data, width, height, styling, chart_colors)
            elif chart_type == "bar_stacked_horizontal":
                chart_image = self._create_stacked_bar_chart(data, width, height, styling, chart_colors)
            elif chart_type == "bar_grouped_vertical":
                chart_image = self._create_grouped_bar_chart(data, width, height, styling, chart_colors)
            else:
                # Fallback to placeholder for unsupported types
                self._render_chart_placeholder(canvas_obj, element, x, y, page_height)
                return
            
            # Draw the chart image
            if chart_image:
                canvas_obj.drawImage(
                    chart_image,
                    x, y - height,
                    width=width,
                    height=height,
                    preserveAspectRatio=True,
                    mask='auto'
                )
        except Exception as e:
            # Fall back to placeholder on error
            import traceback
            print(f"Chart rendering error for {chart_type}: {e}")
            traceback.print_exc()
            self._render_chart_placeholder(canvas_obj, element, x, y, page_height)
    
    def _get_chart_colors(self, styling: Dict) -> List[str]:
        """Get chart colors from styling or brand config."""
        # Default brand chart colors (from brand_config.json chart_colors.series)
        default_colors = ["#5F7483", "#243A4B", "#B08D57", "#9AA3A8"]
        
        # Try bar_colors first
        if "bar_colors" in styling:
            colors = styling["bar_colors"]
            if isinstance(colors, list) and len(colors) > 0:
                # Ensure all items are valid hex colors
                if all(isinstance(c, str) and c.startswith("#") for c in colors):
                    return colors
            # If it's an unresolved reference, use defaults
        
        # Try line_colors
        if "line_colors" in styling:
            colors = styling["line_colors"]
            if isinstance(colors, list) and len(colors) > 0:
                if all(isinstance(c, str) and c.startswith("#") for c in colors):
                    return colors
        
        # Use brand config if available
        if self.brand_config and self.brand_config.chart_colors:
            return self.brand_config.chart_colors
        
        return default_colors
    
    def _create_line_chart(
        self,
        data: Dict,
        width: int,
        height: int,
        styling: Dict,
        colors: List[str]
    ) -> Optional[str]:
        """Create a line chart and return path to temp image file."""
        labels = data.get("labels", [])
        series = data.get("series", [])
        
        if not labels or not series:
            return None
        
        # Convert dimensions to inches (assume 96 DPI)
        fig_width = width / 96
        fig_height = height / 96
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Apply brand styling
        ax.set_facecolor('#F6F7F5')
        fig.patch.set_facecolor('#F6F7F5')
        
        # Plot each series
        for i, s in enumerate(series):
            color = colors[i % len(colors)]
            values = s.get("values", [])
            name = s.get("name", f"Series {i+1}")
            
            ax.plot(labels, values, marker='o', color=color, linewidth=2, 
                    markersize=6, label=name)
        
        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#9AA3A8')
        ax.spines['bottom'].set_color('#9AA3A8')
        ax.tick_params(colors='#1E2428', labelsize=10)
        ax.grid(axis='y', linestyle='-', alpha=0.3, color='#9AA3A8')
        
        # Legend if multiple series
        if len(series) > 1:
            ax.legend(loc='upper left', frameon=False, fontsize=9)
        
        plt.tight_layout()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name, dpi=150, facecolor='#F6F7F5', 
                    edgecolor='none', bbox_inches='tight')
        plt.close(fig)
        
        return temp_file.name
    
    def _create_stacked_bar_chart(
        self,
        data: Dict,
        width: int,
        height: int,
        styling: Dict,
        colors: List[str]
    ) -> Optional[str]:
        """Create a horizontal stacked bar chart matching the example style."""
        categories = data.get("categories", [])
        series = data.get("series", [])
        
        if not categories or not series:
            return None
        
        # Convert dimensions to inches
        fig_width = width / 96
        fig_height = height / 96
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Apply brand styling
        ax.set_facecolor('#F6F7F5')
        fig.patch.set_facecolor('#F6F7F5')
        
        # Prepare data for stacked bars
        y_positions = np.arange(len(categories))
        bar_height = 0.6
        
        # Calculate left positions for stacking
        left = np.zeros(len(categories))
        
        for i, s in enumerate(series):
            color = colors[i % len(colors)]
            values = s.get("values", [])
            name = s.get("name", f"Series {i+1}")
            
            bars = ax.barh(y_positions, values, bar_height, left=left, 
                          color=color, label=name)
            
            # Add percentage labels inside bars
            for j, (bar, val) in enumerate(zip(bars, values)):
                if val > 5:  # Only show label if bar is wide enough
                    text_x = left[j] + val / 2
                    ax.text(text_x, bar.get_y() + bar.get_height()/2, 
                           f'{val}%', ha='center', va='center', 
                           color='white', fontweight='bold', fontsize=11)
            
            left += np.array(values)
        
        # Styling
        ax.set_yticks(y_positions)
        ax.set_yticklabels(categories, fontsize=11, fontweight='bold', color='#1E2428')
        ax.invert_yaxis()  # Top to bottom
        
        # X-axis as percentage
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 20, 40, 60, 80, 100])
        ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], 
                          fontsize=10, color='#1E2428')
        
        # Remove spines except bottom
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#9AA3A8')
        ax.tick_params(left=False)
        
        plt.tight_layout()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name, dpi=150, facecolor='#F6F7F5', 
                    edgecolor='none', bbox_inches='tight')
        plt.close(fig)
        
        return temp_file.name
    
    def _create_grouped_bar_chart(
        self,
        data: Dict,
        width: int,
        height: int,
        styling: Dict,
        colors: List[str]
    ) -> Optional[str]:
        """Create a vertical grouped bar chart."""
        categories = data.get("categories", [])
        series = data.get("series", [])
        
        if not categories or not series:
            return None
        
        # Convert dimensions to inches
        fig_width = width / 96
        fig_height = height / 96
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Apply brand styling
        ax.set_facecolor('#F6F7F5')
        fig.patch.set_facecolor('#F6F7F5')
        
        # Prepare bar positions
        x = np.arange(len(categories))
        n_series = len(series)
        bar_width = 0.8 / n_series
        
        for i, s in enumerate(series):
            color = colors[i % len(colors)]
            values = s.get("values", [])
            name = s.get("name", f"Series {i+1}")
            
            offset = (i - n_series / 2 + 0.5) * bar_width
            ax.bar(x + offset, values, bar_width, color=color, label=name)
        
        # Styling
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=10, color='#1E2428')
        ax.tick_params(colors='#1E2428', labelsize=10)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#9AA3A8')
        ax.spines['bottom'].set_color('#9AA3A8')
        ax.grid(axis='y', linestyle='-', alpha=0.3, color='#9AA3A8')
        
        # Legend
        if len(series) > 1:
            ax.legend(loc='upper left', frameon=False, fontsize=9)
        
        plt.tight_layout()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name, dpi=150, facecolor='#F6F7F5', 
                    edgecolor='none', bbox_inches='tight')
        plt.close(fig)
        
        return temp_file.name
    
    def _render_chart_placeholder(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a placeholder for chart elements when matplotlib is unavailable."""
        size = element.size or {}
        width = size.get("width", 400)
        height = size.get("height", 300)
        
        # Draw placeholder box
        canvas_obj.setStrokeColor(HexColor("#CCCCCC"))
        canvas_obj.setFillColor(HexColor("#F5F5F5"))
        canvas_obj.rect(x, y - height, width, height, fill=1, stroke=1)
        
        # Draw placeholder text
        canvas_obj.setFillColor(HexColor("#999999"))
        canvas_obj.setFont("Helvetica", 14)
        chart_type = element.raw.get("chart_type", "chart")
        canvas_obj.drawCentredString(
            x + width/2,
            y - height/2,
            f"[{chart_type.upper()} CHART]"
        )
    
    def _render_legend(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a chart legend with colored dots and labels."""
        items = element.raw.get("items", [])
        if isinstance(items, str) and items.startswith("{{"):
            return
        
        styling = element.styling or {}
        orientation = element.raw.get("orientation", "horizontal")
        dot_size = styling.get("dot_size", 12)
        label_font = self._get_font_name(styling.get("label_font", "Inter"), 400)
        label_size = styling.get("label_size", 14)
        label_color = styling.get("label_color", "#1E2428")
        item_spacing = styling.get("item_spacing", 40)
        
        # Get chart colors for legend dots
        chart_colors = ["#5F7483", "#243A4B", "#B08D57", "#9AA3A8"]
        
        current_x = x
        current_y = y - dot_size
        
        for i, item in enumerate(items):
            item_text = str(item)
            color = chart_colors[i % len(chart_colors)]
            
            # Draw colored dot
            if isinstance(color, str) and color.startswith("#"):
                canvas_obj.setFillColor(HexColor(color))
            canvas_obj.circle(current_x + dot_size/2, current_y + label_size/3, 
                            dot_size/2, fill=1, stroke=0)
            
            # Draw label
            canvas_obj.setFont(label_font, label_size)
            if isinstance(label_color, str) and label_color.startswith("#"):
                canvas_obj.setFillColor(HexColor(label_color))
            
            text_x = current_x + dot_size + 6
            canvas_obj.drawString(text_x, current_y, item_text)
            
            # Calculate text width for spacing
            try:
                text_width = canvas_obj.stringWidth(item_text, label_font, label_size)
            except:
                text_width = len(item_text) * label_size * 0.5
            
            if orientation == "horizontal":
                current_x += dot_size + 6 + text_width + item_spacing
            else:
                current_y -= label_size + item_spacing
    
    def _render_graphic(
        self,
        canvas_obj: 'canvas.Canvas',
        element: TemplateElement,
        x: int,
        y: int,
        page_height: int
    ):
        """Render a decorative graphic element (placeholder for SVG graphics)."""
        # Graphics like node networks are decorative SVGs
        # For now, skip them gracefully (they're visual enhancements)
        # In a full implementation, we'd use svglib or similar
        pass
    
    def _register_fonts(self):
        """Register custom fonts with ReportLab."""
        if self._fonts_registered:
            return
        
        fonts_dir = self.project_root / "brand" / "fonts"
        if not fonts_dir.exists():
            self._fonts_registered = True
            return
        
        # Font files to register
        font_files = {
            "PlayfairDisplay-Regular": "PlayfairDisplay-Regular.ttf",
            "PlayfairDisplay-Medium": "PlayfairDisplay-Medium.ttf",
            "PlayfairDisplay-SemiBold": "PlayfairDisplay-SemiBold.ttf",
            "Inter-Regular": "Inter-Regular.ttf",
            "Inter-Medium": "Inter-Medium.ttf",
            "Inter-SemiBold": "Inter-SemiBold.ttf",
        }
        
        for font_name, filename in font_files.items():
            font_path = fonts_dir / filename
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    self._font_map[font_name] = font_name
                except Exception:
                    pass
        
        self._fonts_registered = True


# Convenience function
def render_pdf(
    templates: List[ParsedTemplate],
    output_path: Union[str, Path],
    brand_config: BrandConfig = None
) -> Path:
    """
    Quick function to render templates to PDF.
    
    Args:
        templates: List of ParsedTemplate objects.
        output_path: Path to save the PDF.
        brand_config: Optional BrandConfig.
        
    Returns:
        Path to the generated PDF.
    """
    renderer = PDFRenderer(brand_config=brand_config)
    return renderer.render_document(templates, output_path)
