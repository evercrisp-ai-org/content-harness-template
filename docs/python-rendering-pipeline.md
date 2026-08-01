# Content Harness: Python Rendering Pipeline

A Python-based brand asset management and document generation system for creating consistent, on-brand lead magnets, reports, social media posts, and marketing materials.

## Overview

This system provides:

- **JSON-based templates** for consistent layouts and design
- **Brand configuration** that centralizes colors, typography, logos, and spacing
- **Variable substitution** for dynamic content generation
- **PDF rendering** for multi-page reports and lead magnets
- **Image rendering** for social media and infographics

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate a Report

```python
from src import TemplateParser, load_brand_config
from src.renderers import render_pdf

# Load brand configuration
config = load_brand_config()

# Initialize parser
parser = TemplateParser(brand_config=config)

# Load and fill a template
template = parser.load_template("pdf-page-templates/lead_magnets/report/cover_dark.json")
filled = parser.fill_variables(template, {
    "title": "Your Report Title",
    "subtitle": "Subtitle Here",
    "date": "January 2026"
})

# Render to PDF
render_pdf([filled], "outputs/final/report.pdf")
```

## Folder Structure

```
capable_wealth/
├── brand/
│   ├── brand_config.json     # Master brand settings
│   ├── fonts/                # Font files (.ttf, .otf)
│   ├── logos/                # Logo variants
│   ├── graphics/             # Node networks, icons, patterns
│   └── assets/               # Other reusable graphics
│
├── pdf-page-templates/
│   ├── lead_magnets/
│   │   ├── report/           # Report page templates
│   │   │   ├── _manifest.json
│   │   │   ├── cover_light.json
│   │   │   ├── cover_dark.json
│   │   │   ├── chart_line.json
│   │   │   └── ...
│   │   └── checklist/        # Checklist templates (future)
│   │
│   ├── social_media/
│   │   ├── instagram/
│   │   ├── linkedin/
│   │   └── twitter/
│   │
│   └── infographics/
│
├── outputs/
│   ├── drafts/
│   └── final/
│
├── src/
│   ├── config.py             # Brand configuration loader
│   ├── template_parser.py    # Template parsing and variable substitution
│   └── renderers/
│       ├── pdf_renderer.py   # PDF generation
│       └── image_renderer.py # PNG/JPEG generation
│
├── examples/
│   └── sample_report_content.json
│
├── requirements.txt
└── README.md
```

## Template System

### Template Structure

Each template is a JSON file with:

```json
{
  "template_id": "cover_light",
  "template_name": "Cover Page - Light Background",
  "dimensions": { "width": 816, "height": 1056, "unit": "px" },
  "background": {
    "type": "solid",
    "color": "$colors.neutral_light"
  },
  "elements": [
    {
      "id": "title",
      "type": "text",
      "content": "{{title}}",
      "font": "$typography.heading.family",
      "font_size": 64,
      "color": "$colors.primary.hex",
      "position": { "x": 40, "y": 280 }
    }
  ],
  "variables": {
    "title": { "type": "string", "required": true }
  }
}
```

### Reference Syntax

- **`$brand.*`** - References to `brand_config.json` values
  - `$colors.primary.hex` → `"#243A4B"`
  - `$typography.heading.family` → `"Playfair Display"`
  
- **`{{variable}}`** - Content placeholders filled at runtime
  - `{{title}}` → Your provided title text
  - `{{chart_data}}` → Your chart data object

## Brand Configuration

The `brand/brand_config.json` file defines:

### Colors
```json
{
  "colors": {
    "primary": { "name": "Deep Muted Blue", "hex": "#243A4B" },
    "secondary": { "name": "Blue Slate", "hex": "#5F7483" },
    "accent": { "name": "Antique Gold", "hex": "#B08D57" },
    "neutral_light": { "name": "Off-White", "hex": "#F6F7F5" },
    "neutral_dark": { "name": "Charcoal", "hex": "#1E2428" },
    "neutral_mid": { "name": "Warm Gray", "hex": "#9AA3A8" }
  }
}
```

### Typography
```json
{
  "typography": {
    "heading": { "family": "Playfair Display", "weights": [400, 500, 600] },
    "body": { "family": "Inter", "weights": [400, 500, 600] }
  }
}
```

### Chart Colors
```json
{
  "chart_colors": {
    "series": ["#5F7483", "#243A4B", "#B08D57", "#9AA3A8"]
  }
}
```

## Available Templates

### Report Templates

| Template | Description |
|----------|-------------|
| `cover_light.json` | Light background cover page |
| `cover_dark.json` | Dark background cover page |
| `quote_key_findings.json` | Quote + numbered findings list |
| `introduction.json` | Drop cap introduction page |
| `chart_line.json` | Line chart with section header |
| `chart_bar_stacked.json` | Horizontal stacked bars |
| `chart_bar_grouped.json` | Vertical grouped bars |
| `chart_dot.json` | Dot/strip plot |
| `chart_area_dual.json` | Dual stacked area charts |
| `chart_with_sidebar.json` | Chart + dark sidebar callout |
| `expert_quote.json` | Expert photo + pull quote |
| `quote_network.json` | Pull quote + node network |

## Usage Examples

### Render a Complete Report

```python
import json
from src import TemplateParser
from src.renderers import PDFRenderer

# Load content
with open("examples/sample_report_content.json") as f:
    content = json.load(f)

# Initialize
parser = TemplateParser()
renderer = PDFRenderer()

# Build pages
pages = []
for page_config in content["pages"]:
    template = parser.load_template(
        f"pdf-page-templates/lead_magnets/report/{page_config['template']}.json"
    )
    filled = parser.fill_variables(template, page_config["content"])
    pages.append(filled)

# Render PDF
renderer.render_document(pages, "outputs/final/report.pdf")
```

### Generate Social Media Image

```python
from src import TemplateParser
from src.renderers import ImageRenderer

parser = TemplateParser()
renderer = ImageRenderer()

template = parser.load_template("pdf-page-templates/social_media/instagram/post_square.json")
filled = parser.fill_variables(template, {
    "headline": "5 Tax Strategies",
    "subheadline": "Every Surgeon Should Know"
})

renderer.render_image(filled, "outputs/final/social_post.png")
```

## Adding New Templates

1. Create a new JSON file in the appropriate template directory
2. Define `template_id`, `dimensions`, `background`, `elements`, and `variables`
3. Use `$` references for brand values and `{{}}` for content variables
4. Add the template to the `_manifest.json` for discoverability

## Font Setup

Place your font files in `brand/fonts/`:

- `PlayfairDisplay-Regular.ttf`
- `PlayfairDisplay-Medium.ttf`
- `PlayfairDisplay-SemiBold.ttf`
- `Inter-Regular.ttf`
- `Inter-Medium.ttf`
- `Inter-SemiBold.ttf`

Fonts can be downloaded from Google Fonts:
- [Playfair Display](https://fonts.google.com/specimen/Playfair+Display)
- [Inter](https://fonts.google.com/specimen/Inter)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
```

## License

Proprietary - [ORG_NAME]

## Support

For questions or support, contact your content harness administrator.
