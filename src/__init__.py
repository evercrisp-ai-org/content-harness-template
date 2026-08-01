"""
Content Harness Template System

A Python-based brand asset management and document generation system
for creating consistent, on-brand lead magnets, reports, and marketing materials.
"""

__version__ = "1.0.0"
__author__ = "Content Harness"

from .config import BrandConfig, load_brand_config
from .template_parser import TemplateParser, parse_template

__all__ = [
    "BrandConfig",
    "load_brand_config", 
    "TemplateParser",
    "parse_template",
]
