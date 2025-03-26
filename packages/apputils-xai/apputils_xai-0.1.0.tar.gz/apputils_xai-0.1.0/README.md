# AppUtils-XAI

A utility library for no-code app generation in the NoLink platform.

## Installation

```bash
pip install apputils-xai
```

USAGE:
from apputils import parse_text_input, map_features_to_templates, validate_app_structure

# Parse text input

app_structure = parse_text_input("Build a shopping app with payments and user accounts")
print(app_structure)

# Map features to templates

app_type = app_structure["app_type"]
features = app_structure["features"]
template_config = map_features_to_templates(app_type, features)
print(template_config)

# Validate app structure

is_valid, errors = validate_app_structure(template_config)
if not is_valid:
print("Validation errors:", errors)
else:
print("App structure is valid")
