"""
Template Parser

Parses JSON template files, resolves $brand.* references to actual values,
and substitutes {{variable}} placeholders with provided content.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

from .config import BrandConfig, load_brand_config


@dataclass
class TemplateVariable:
    """Definition of a template variable."""
    name: str
    var_type: str
    required: bool = False
    default: Any = None
    description: str = ""
    max_length: Optional[int] = None
    schema: Optional[Dict] = None


@dataclass
class TemplateElement:
    """A single element within a template (text, image, chart, etc.)."""
    id: str
    element_type: str
    position: Dict[str, int]
    size: Optional[Dict[str, int]] = None
    content: Optional[str] = None
    source: Optional[str] = None
    font: Optional[str] = None
    font_weight: Optional[int] = None
    font_size: Optional[int] = None
    color: Optional[str] = None
    max_width: Optional[int] = None
    line_height: Optional[float] = None
    styling: Optional[Dict] = None
    description: Optional[str] = None
    raw: Dict = field(default_factory=dict)


@dataclass
class ParsedTemplate:
    """A fully parsed and resolved template ready for rendering."""
    template_id: str
    template_name: str
    template_type: str
    dimensions: Dict[str, int]
    background: Dict[str, Any]
    elements: List[TemplateElement]
    variables: Dict[str, TemplateVariable]
    raw: Dict[str, Any] = field(default_factory=dict)


class TemplateParser:
    """
    Parses JSON templates and resolves brand references.
    
    Usage:
        parser = TemplateParser()
        template = parser.load_template("pdf-page-templates/lead_magnets/report/cover_light.json")
        filled = parser.fill_variables(template, {"title": "My Report", "subtitle": "2024 Edition"})
    """
    
    # Regex patterns
    BRAND_REF_PATTERN = re.compile(r'\$([a-zA-Z_][a-zA-Z0-9_.]*)')
    VARIABLE_PATTERN = re.compile(r'\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}')
    
    def __init__(self, brand_config: BrandConfig = None, project_root: Path = None):
        """
        Initialize the template parser.
        
        Args:
            brand_config: BrandConfig object. Loads default if not provided.
            project_root: Project root directory for resolving relative paths.
        """
        self.brand_config = brand_config or load_brand_config()
        self.project_root = project_root or Path(__file__).parent.parent
        self._current_template_dir = self.project_root
    
    def load_template(self, template_path: Union[str, Path]) -> ParsedTemplate:
        """
        Load and parse a template JSON file.
        
        Args:
            template_path: Path to the template JSON file.
            
        Returns:
            ParsedTemplate with all $brand.* references resolved.
        """
        template_path = self._resolve_path(template_path)
        self._current_template_dir = template_path.parent
        
        with open(template_path, "r", encoding="utf-8") as f:
            raw_template = json.load(f)
        
        # Expand component references before parsing
        raw_template = self._expand_components(raw_template)
        
        return self._parse_template(raw_template)
    
    def _expand_components(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Expand component references into inline elements."""
        result = dict(raw)
        
        # Expand components in top-level elements
        if "elements" in result:
            result["elements"] = self._expand_component_list(result["elements"])
        
        # Expand components in sections
        if "sections" in result:
            sections = []
            for section in result["sections"]:
                section_copy = dict(section)
                if "elements" in section_copy:
                    section_copy["elements"] = self._expand_component_list(section_copy["elements"])
                sections.append(section_copy)
            result["sections"] = sections
        
        return result
    
    def _expand_component_list(self, elements: List[Dict]) -> List[Dict]:
        """Expand component references in a list of elements."""
        expanded = []
        for elem in elements:
            if elem.get("type") == "component":
                component_elements = self._load_component(elem)
                expanded.extend(component_elements)
            else:
                expanded.append(elem)
        return expanded
    
    def _load_component(self, component_ref: Dict) -> List[Dict]:
        """
        Load a component and return its elements with adjusted positions.
        
        Args:
            component_ref: Component reference dict with 'source' and 'position'.
            
        Returns:
            List of element dicts with positions offset by component position.
        """
        source = component_ref.get("source", "")
        if not source:
            return []
        
        # Resolve component path relative to current template directory
        component_path = self._current_template_dir / source
        if not component_path.exists():
            # Try from templates directory
            component_path = self.project_root / "templates" / "lead_magnets" / "report" / source
        
        if not component_path.exists():
            return []
        
        try:
            with open(component_path, "r", encoding="utf-8") as f:
                component_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
        
        # Get component position offset
        comp_pos = component_ref.get("position", {"x": 0, "y": 0})
        offset_x = comp_pos.get("x", 0)
        offset_y = comp_pos.get("y", 0)
        
        # Get the variant if specified
        variant = component_ref.get("variant", "light")
        variants = component_data.get("variants", {})
        variant_data = variants.get(variant, variants.get("light", {}))
        
        # Extract and offset elements
        elements = component_data.get("elements", [])
        result = []
        
        for elem in elements:
            elem_copy = dict(elem)
            elem_pos = elem_copy.get("position", {"x": 0, "y": 0})
            elem_copy["position"] = {
                "x": elem_pos.get("x", 0) + offset_x,
                "y": elem_pos.get("y", 0) + offset_y
            }
            
            # Apply variant styling if present
            if "color" in elem_copy and elem_copy["color"].startswith("{{variant."):
                color_key = elem_copy["color"].replace("{{variant.", "").replace("}}", "")
                elem_copy["color"] = variant_data.get(color_key, elem_copy["color"])
            
            result.append(elem_copy)
        
        return result
    
    def _parse_template(self, raw: Dict[str, Any]) -> ParsedTemplate:
        """Parse raw template dict into ParsedTemplate object."""
        
        # Resolve all brand references in the template
        resolved = self._resolve_all_references(raw)
        
        # Parse variables
        variables = {}
        for name, var_data in resolved.get("variables", {}).items():
            variables[name] = TemplateVariable(
                name=name,
                var_type=var_data.get("type", "string"),
                required=var_data.get("required", False),
                default=var_data.get("default"),
                description=var_data.get("description", ""),
                max_length=var_data.get("max_length"),
                schema=var_data.get("schema")
            )
        
        # Parse elements
        elements = []
        for elem_data in resolved.get("elements", []):
            elements.append(self._parse_element(elem_data))
        
        # Also parse elements from sections if present
        # Offset element positions by section position
        for section in resolved.get("sections", []):
            section_pos = section.get("position", {"x": 0, "y": 0})
            section_x = section_pos.get("x", 0)
            section_y = section_pos.get("y", 0)
            
            for elem_data in section.get("elements", []):
                # Create a copy to avoid mutating the original
                elem_copy = dict(elem_data)
                elem_pos = elem_copy.get("position", {"x": 0, "y": 0})
                elem_copy["position"] = {
                    "x": elem_pos.get("x", 0) + section_x,
                    "y": elem_pos.get("y", 0) + section_y
                }
                elements.append(self._parse_element(elem_copy))
        
        return ParsedTemplate(
            template_id=resolved.get("template_id", ""),
            template_name=resolved.get("template_name", ""),
            template_type=resolved.get("page_type", resolved.get("template_type", "")),
            dimensions=resolved.get("dimensions", {"width": 816, "height": 1056, "unit": "px"}),
            background=resolved.get("background", {}),
            elements=elements,
            variables=variables,
            raw=resolved
        )
    
    def _parse_element(self, elem_data: Dict) -> TemplateElement:
        """Parse a single element dict into TemplateElement."""
        return TemplateElement(
            id=elem_data.get("id", ""),
            element_type=elem_data.get("type", ""),
            position=elem_data.get("position", {"x": 0, "y": 0}),
            size=elem_data.get("size"),
            content=elem_data.get("content"),
            source=elem_data.get("source"),
            font=elem_data.get("font"),
            font_weight=elem_data.get("font_weight"),
            font_size=elem_data.get("font_size"),
            color=elem_data.get("color"),
            max_width=elem_data.get("max_width"),
            line_height=elem_data.get("line_height"),
            styling=elem_data.get("styling"),
            description=elem_data.get("description"),
            raw=elem_data
        )
    
    def _resolve_all_references(self, obj: Any) -> Any:
        """Recursively resolve all $brand.* references in an object."""
        if isinstance(obj, str):
            return self._resolve_string(obj)
        elif isinstance(obj, dict):
            return {k: self._resolve_all_references(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_all_references(item) for item in obj]
        else:
            return obj
    
    def _resolve_string(self, value: str) -> Any:
        """Resolve brand references in a string value."""
        if not isinstance(value, str):
            return value
            
        # Check if the entire string is a brand reference
        if value.startswith("$") and not "{{" in value:
            resolved = self.brand_config.resolve_reference(value)
            return resolved
        
        # Check for embedded references (less common)
        def replace_ref(match):
            ref = "$" + match.group(1)
            resolved = self.brand_config.resolve_reference(ref)
            return str(resolved) if resolved != ref else match.group(0)
        
        return self.BRAND_REF_PATTERN.sub(replace_ref, value)
    
    def fill_variables(self, template: ParsedTemplate, content: Dict[str, Any]) -> ParsedTemplate:
        """
        Fill template variables with provided content.
        
        Args:
            template: ParsedTemplate to fill.
            content: Dict mapping variable names to values.
            
        Returns:
            New ParsedTemplate with variables substituted.
        """
        # Validate required variables
        missing = []
        for name, var in template.variables.items():
            if var.required and name not in content:
                if var.default is None:
                    missing.append(name)
                else:
                    content[name] = var.default
        
        if missing:
            raise ValueError(f"Missing required variables: {', '.join(missing)}")
        
        # Fill variables in the raw template
        filled_raw = self._fill_variables_in_obj(template.raw, content)
        
        # Re-parse with filled values
        return self._parse_template(filled_raw)
    
    def _fill_variables_in_obj(self, obj: Any, content: Dict[str, Any]) -> Any:
        """Recursively fill {{variable}} placeholders."""
        if isinstance(obj, str):
            return self._fill_variables_in_string(obj, content)
        elif isinstance(obj, dict):
            return {k: self._fill_variables_in_obj(v, content) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._fill_variables_in_obj(item, content) for item in obj]
        else:
            return obj
    
    # Pattern to match a string that is exactly one variable reference
    SINGLE_VARIABLE_PATTERN = re.compile(r'^\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}$')
    
    def _fill_variables_in_string(self, value: str, content: Dict[str, Any]) -> Any:
        """
        Fill {{variable}} placeholders in a string.
        
        If the string is exactly one variable reference (e.g., "{{findings}}"),
        return the actual value from content (preserving arrays/objects).
        
        If the string contains mixed content or multiple variables,
        perform string interpolation.
        """
        # Check if the entire string is a single variable reference
        single_match = self.SINGLE_VARIABLE_PATTERN.match(value)
        if single_match:
            var_name = single_match.group(1)
            if var_name in content:
                # Return the actual value (array, object, string, number, etc.)
                return content[var_name]
            return value  # Keep original if not found
        
        # For mixed strings, do string interpolation
        def replace_var(match):
            var_name = match.group(1)
            if var_name in content:
                return str(content[var_name])
            return match.group(0)  # Keep original if not found
        
        return self.VARIABLE_PATTERN.sub(replace_var, value)
    
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """Resolve a path relative to project root."""
        path = Path(path)
        if path.is_absolute():
            return path
        return self.project_root / path
    
    def get_template_variables(self, template_path: Union[str, Path]) -> Dict[str, TemplateVariable]:
        """
        Get the variables required by a template without fully parsing it.
        
        Useful for knowing what content is needed before filling a template.
        """
        template = self.load_template(template_path)
        return template.variables
    
    def validate_content(self, template: ParsedTemplate, content: Dict[str, Any]) -> List[str]:
        """
        Validate content against template variable requirements.
        
        Returns:
            List of validation error messages (empty if valid).
        """
        errors = []
        
        for name, var in template.variables.items():
            if var.required and name not in content:
                errors.append(f"Missing required variable: {name}")
                continue
            
            if name in content:
                value = content[name]
                
                # Type validation
                if var.var_type == "string" and not isinstance(value, str):
                    errors.append(f"Variable '{name}' must be a string")
                elif var.var_type == "number" and not isinstance(value, (int, float)):
                    errors.append(f"Variable '{name}' must be a number")
                elif var.var_type == "array" and not isinstance(value, list):
                    errors.append(f"Variable '{name}' must be an array")
                elif var.var_type == "object" and not isinstance(value, dict):
                    errors.append(f"Variable '{name}' must be an object")
                
                # Length validation for strings
                if var.max_length and isinstance(value, str) and len(value) > var.max_length:
                    errors.append(f"Variable '{name}' exceeds max length of {var.max_length}")
        
        return errors


# Convenience function
def parse_template(template_path: Union[str, Path], content: Dict[str, Any] = None) -> ParsedTemplate:
    """
    Quick function to parse a template and optionally fill variables.
    
    Args:
        template_path: Path to template JSON file.
        content: Optional dict of variable values to fill.
        
    Returns:
        ParsedTemplate ready for rendering.
    """
    parser = TemplateParser()
    template = parser.load_template(template_path)
    
    if content:
        template = parser.fill_variables(template, content)
    
    return template
