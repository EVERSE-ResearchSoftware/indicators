from helpers import validate_json_files_using_schema

def test_indicators_validation():
    """
    Validates all JSON files in the 'indicators/' directory against the
    local JSON Schema file (indicator_validation_schema.json).
    """
    validate_json_files_using_schema(schema_file_path='tests/indicator_validation_schema.json', json_file_path='indicators')

def test_dimensions_validation():
    """
    Validates all JSON files in the 'dimensions/' directory against the
    local JSON Schema file (dimension_validation_schema.json).
    """
    validate_json_files_using_schema(schema_file_path='tests/dimension_validation_schema.json', json_file_path='dimensions')
