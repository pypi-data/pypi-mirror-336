from apputils import parse_text_input, map_features_to_templates, validate_app_structure, auto_fix_structure

def test_basic_workflow():
    # Test parsing
    print("Testing text parsing...")
    app_structure = parse_text_input("Create a shopping app with payments and user login")
    print(f"App Type: {app_structure['app_type']}")
    print(f"Features: {app_structure['features']}")
    print()
    
    # Test mapping
    print("Testing feature mapping...")
    template_config = map_features_to_templates(app_structure['app_type'], app_structure['features'])
    print(f"Components: {template_config['components']}")
    print(f"Data Models: {list(template_config['data_models'].keys())}")
    print(f"API Endpoints: {template_config['api_endpoints'][:5]}... (and more)")
    print()
    
    # Test validation
    print("Testing validation...")
    is_valid, errors = validate_app_structure(template_config)
    print(f"Is Valid: {is_valid}")
    if not is_valid:
        print(f"Errors: {errors}")
        print("Auto-fixing issues...")
        fixed_template = auto_fix_structure(template_config)
        is_valid, errors = validate_app_structure(fixed_template)
        print(f"After fix - Is Valid: {is_valid}")
    print()
    
    # Test another example
    print("Testing social media app example...")
    social_app = parse_text_input("Build a social media app with messaging and AI recommendations")
    social_template = map_features_to_templates(social_app['app_type'], social_app['features'])
    print(f"App Type: {social_app['app_type']}")
    print(f"Features: {social_app['features']}")
    print(f"Components: {social_template['components']}")
    print(f"Data Models: {list(social_template['data_models'].keys())}")
    
if __name__ == "__main__":
    test_basic_workflow()