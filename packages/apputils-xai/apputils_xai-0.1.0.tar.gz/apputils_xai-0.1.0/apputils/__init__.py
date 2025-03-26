"""
AppUtils: A Python library for no-code app generation.
"""

__version__ = '0.1.0'

from .parser import TextParser
from .mapper import TemplateMapper
from .validator import AppValidator

# Create convenience functions that create and use the class instances
def parse_text_input(text):
    """Parse natural language input to extract app type and features."""
    parser = TextParser()
    return parser.parse_text_input(text)

def map_features_to_templates(app_type, features):
    """Map app features to templates and configurations."""
    mapper = TemplateMapper()
    return mapper.map_features_to_templates(app_type, features)

def validate_app_structure(app_structure):
    """Validate the app structure to ensure it meets requirements."""
    validator = AppValidator()
    return validator.validate_app_structure(app_structure)

def auto_fix_structure(app_structure):
    """Automatically fix common issues in the app structure."""
    validator = AppValidator()
    return validator.auto_fix_structure(app_structure)

