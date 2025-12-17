from helpers import validate_json_files_using_schema, validate_json_files_consistency

def test_indicators_validation():
    """
    Validates all JSON files in the 'indicators/' directory against the
    local JSON Schema file (indicator_validation_schema.json).
    """
    validate_json_files_using_schema(
        schema_file_path="tests/indicator_validation_schema.json",
        json_file_path="indicators",
    )


def test_dimensions_validation():
    """
    Validates all JSON files in the 'dimensions/' directory against the
    local JSON Schema file (dimension_validation_schema.json).
    """
    validate_json_files_using_schema(
        schema_file_path="tests/dimension_validation_schema.json",
        json_file_path="dimensions",
    )


def test_indicators_json_files_consistency():
    """
    Validates that all JSON files in the indicators/ directory follow these guidelines:
    
    - identifier and @id fields have the same value
    - abbreviation field is the same as the identifier and @id suffix (abbreviation = /identifier_suffix)
    - json file is named after the abbreviation field (abbreviation + .json)
    """
    validate_json_files_consistency(json_file_path="indicators")
    
    
def test_dimensions_json_files_consistency():
    """
    Validates that all JSON files in the dimensions/ directory follow these guidelines:
    
    - identifier and @id fields have the same value
    - abbreviation field is the same as the identifier and @id suffix (abbreviation = /identifier_suffix)
    - json file is named after the abbreviation field (abbreviation + .json)
    """
    validate_json_files_consistency(json_file_path="dimensions")