"""
App structure validator for ensuring app configurations are valid and complete.
"""
from typing import Dict, List, Any, Tuple, Optional

class AppValidator:
    """
    Validates app structures and configurations.
    """
    
    def __init__(self):
        pass
    
    def validate_app_structure(self, app_structure: Dict[str, Any]) -> Tuple[bool, Optional[List[str]]]:
        """
        Validate the app structure to ensure it meets requirements.
        
        Args:
            app_structure: The app structure configuration to validate
            
        Returns:
            A tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate required fields
        required_fields = ["app_type", "components", "data_models", "api_endpoints", "features"]
        for field in required_fields:
            if field not in app_structure:
                errors.append(f"Missing required field: {field}")
        
        # If missing required fields, return early
        if errors:
            return False, errors
        
        # Validate app type
        if not app_structure["app_type"]:
            errors.append("App type cannot be empty")
        
        # Validate components
        if not app_structure["components"]:
            errors.append("App must have at least one component")
        
        # Validate data models
        if not app_structure["data_models"]:
            errors.append("App must have at least one data model")
        
        # Validate API endpoints
        if not app_structure["api_endpoints"]:
            errors.append("App must have at least one API endpoint")
        
        # Validate that each data model has required fields
        for model_name, model_schema in app_structure["data_models"].items():
            if "id" not in model_schema:
                errors.append(f"Data model '{model_name}' is missing required 'id' field")
        
        # Check for potential conflicts
        if self._has_conflicts(app_structure):
            errors.append("App structure has conflicts that need to be resolved")
        
        # If there are any errors, validation failed
        if errors:
            return False, errors
            
        return True, None
    
    def _has_conflicts(self, app_structure: Dict[str, Any]) -> bool:
        """
        Check for potential conflicts in the app structure.
        
        Args:
            app_structure: The app structure to check
            
        Returns:
            True if conflicts found, False otherwise
        """
        # Check for duplicate model names with different schemas
        data_models = app_structure["data_models"]
        model_names = set(data_models.keys())
        
        # Example conflict: Having both social and messaging features but no user model
        if ("social" in app_structure["features"] or "messaging" in app_structure["features"]) and "User" not in model_names:
            return True
            
        return False
        
    def auto_fix_structure(self, app_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically fix common issues in the app structure.
        
        Args:
            app_structure: The app structure to fix
            
        Returns:
            The fixed app structure
        """
        # If no app type, set to generic
        if "app_type" not in app_structure or not app_structure["app_type"]:
            app_structure["app_type"] = "generic"
        
        # Ensure components exist
        if "components" not in app_structure or not app_structure["components"]:
            app_structure["components"] = ["ListView", "DetailView", "Form"]
        
        # Ensure data models exist
        if "data_models" not in app_structure or not app_structure["data_models"]:
            app_structure["data_models"] = {
                "Item": {
                    "id": "string",
                    "title": "string",
                    "description": "string",
                    "createdAt": "date"
                }
            }
        
        # Ensure API endpoints exist
        if "api_endpoints" not in app_structure or not app_structure["api_endpoints"]:
            app_structure["api_endpoints"] = ["listItems", "getItem", "createItem", "updateItem", "deleteItem"]
        
        # Ensure features exist
        if "features" not in app_structure or not app_structure["features"]:
            app_structure["features"] = ["crud"]
        
        # Fix model dependencies
        if ("social" in app_structure["features"] or "messaging" in app_structure["features"]) and "User" not in app_structure["data_models"]:
            app_structure["data_models"]["User"] = {
                "id": "string",
                "username": "string",
                "email": "string",
                "createdAt": "date"
            }
        
        return app_structure